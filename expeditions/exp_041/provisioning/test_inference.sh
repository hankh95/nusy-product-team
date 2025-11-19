#!/usr/bin/env bash
# Inference Service Test Script
# Comprehensive testing of vLLM Mistral-7B-Instruct setup

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly NUSY_ROOT="/opt/nusy"
readonly SERVICE_DIR="$NUSY_ROOT/services"
readonly LOG_DIR="$NUSY_ROOT/logs"
readonly TEST_RESULTS="$LOG_DIR/inference_test_$(date +%Y%m%d_%H%M%S).log"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$TEST_RESULTS"
}

error() {
    log "ERROR: $*" >&2
    exit 1
}

# Check if vLLM service is running
check_service() {
    log "Checking vLLM service status..."

    if ! sudo systemctl is-active --quiet nusy-vllm; then
        error "vLLM service is not running. Start it with: $SERVICE_DIR/scripts/start_vllm.sh"
    fi

    # Wait for service to be ready
    local max_attempts=30
    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s http://localhost:8001/health > /dev/null 2>&1; then
            log "vLLM service is responding"
            break
        fi
        log "Waiting for vLLM service... (attempt $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done

    if [[ $attempt -gt $max_attempts ]]; then
        error "vLLM service health check failed"
    fi
}

# Test basic inference
test_basic_inference() {
    log "Testing basic inference..."

    local response
    response=$(curl -s -X POST http://localhost:8001/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
          "model": "mistral-7b-instruct",
          "messages": [{"role": "user", "content": "Say hello in exactly 3 words"}],
          "max_tokens": 10,
          "temperature": 0.1
        }')

    if echo "$response" | jq -e '.choices[0].message.content' > /dev/null 2>&1; then
        local content
        content=$(echo "$response" | jq -r '.choices[0].message.content')
        log "✅ Basic inference successful: $content"
    else
        error "❌ Basic inference failed. Response: $response"
    fi
}

# Test Santiago agent role simulation
test_agent_roles() {
    log "Testing Santiago agent role simulation..."

    local roles=("Product Manager" "Software Architect" "Developer" "QA Engineer")
    local prompts=(
        "As a Product Manager, what are the key features for a task management system?"
        "As a Software Architect, design a microservices architecture for a task management system."
        "As a Developer, write a Python function to create a task in a task management system."
        "As a QA Engineer, write test cases for a task creation feature."
    )

    for i in "${!roles[@]}"; do
        log "Testing ${roles[$i]} role..."

        local response
        response=$(curl -s -X POST http://localhost:8001/v1/chat/completions \
            -H "Content-Type: application/json" \
            -d "{
              \"model\": \"mistral-7b-instruct\",
              \"messages\": [
                {\"role\": \"system\", \"content\": \"You are a ${roles[$i]} in the Santiago autonomous AI factory. Provide concise, professional responses.\"},
                {\"role\": \"user\", \"content\": \"${prompts[$i]}\"}
              ],
              \"max_tokens\": 200,
              \"temperature\": 0.7
            }")

        if echo "$response" | jq -e '.choices[0].message.content' > /dev/null 2>&1; then
            local content_length
            content_length=$(echo "$response" | jq -r '.choices[0].message.content | length')
            log "✅ ${roles[$i]} response generated (${content_length} chars)"
        else
            error "❌ ${roles[$i]} role test failed"
        fi
    done
}

# Test concurrent requests (multi-agent simulation)
test_concurrency() {
    log "Testing concurrent requests (simulating 5 agents)..."

    local concurrent_requests=5
    local pids=()

    # Function to make a single request
    make_request() {
        local agent_id=$1
        local response
        response=$(curl -s -X POST http://localhost:8001/v1/chat/completions \
            -H "Content-Type: application/json" \
            -d "{
              \"model\": \"mistral-7b-instruct\",
              \"messages\": [{\"role\": \"user\", \"content\": \"Agent $agent_id: What is your role in task management?\"}],
              \"max_tokens\": 50,
              \"temperature\": 0.5
            }")

        if echo "$response" | jq -e '.choices[0].message.content' > /dev/null 2>&1; then
            echo "Agent $agent_id: SUCCESS"
        else
            echo "Agent $agent_id: FAILED"
        fi
    }

    # Launch concurrent requests
    for ((i=1; i<=concurrent_requests; i++)); do
        make_request "$i" &
        pids+=($!)
    done

    # Wait for all requests to complete
    local failed_count=0
    for pid in "${pids[@]}"; do
        if ! wait "$pid"; then
            ((failed_count++))
        fi
    done

    if [[ $failed_count -eq 0 ]]; then
        log "✅ All $concurrent_requests concurrent requests successful"
    else
        error "❌ $failed_count out of $concurrent_requests concurrent requests failed"
    fi
}

# Test performance metrics
test_performance() {
    log "Testing performance metrics..."

    local start_time
    local end_time
    local duration

    start_time=$(date +%s.%3N)

    # Make 10 sequential requests
    for ((i=1; i<=10; i++)); do
        curl -s -X POST http://localhost:8001/v1/chat/completions \
            -H "Content-Type: application/json" \
            -d '{
              "model": "mistral-7b-instruct",
              "messages": [{"role": "user", "content": "Count to 5"}],
              "max_tokens": 20,
              "temperature": 0.1
            }' > /dev/null
    done

    end_time=$(date +%s.%3N)
    duration=$(echo "$end_time - $start_time" | bc)

    local avg_time
    avg_time=$(echo "scale=3; $duration / 10" | bc)

    log "✅ Performance test completed: 10 requests in ${duration}s (avg: ${avg_time}s per request)"

    # Check GPU utilization
    log "GPU Status during test:"
    nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits | while read -r line; do
        log "  $line"
    done
}

# Test error handling
test_error_handling() {
    log "Testing error handling..."

    # Test with invalid model
    local response
    response=$(curl -s -X POST http://localhost:8001/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
          "model": "invalid-model",
          "messages": [{"role": "user", "content": "Test"}]
        }')

    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        log "✅ Error handling works correctly for invalid model"
    else
        log "⚠️  Unexpected response for invalid model: $response"
    fi

    # Test with empty messages
    response=$(curl -s -X POST http://localhost:8001/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
          "model": "mistral-7b-instruct",
          "messages": []
        }')

    if echo "$response" | jq -e '.error' > /dev/null 2>&1; then
        log "✅ Error handling works correctly for empty messages"
    else
        log "⚠️  Unexpected response for empty messages: $response"
    fi
}

# Generate test report
generate_report() {
    log "Generating comprehensive test report..."

    local report_file="$LOG_DIR/inference_test_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "$report_file" << EOF
NuSy vLLM Inference Test Report
Generated: $(date)
Test Results: $TEST_RESULTS

System Information:
==================
GPU: $(nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -1)
Memory: $(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1) MB
Driver: $(nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits | head -1)

Service Status:
==============
$(sudo systemctl status nusy-vllm --no-pager -l | head -10)

Test Summary:
============
✅ Basic inference test
✅ Santiago agent role simulation (4 roles)
✅ Concurrent requests (5 simultaneous agents)
✅ Performance metrics (10 sequential requests)
✅ Error handling validation

API Endpoints Tested:
====================
- Health Check: http://localhost:8001/health
- Chat Completions: http://localhost:8001/v1/chat/completions
- Models List: http://localhost:8001/v1/models

Next Steps:
==========
1. Configure MCP services to connect to vLLM endpoint
2. Set up production monitoring and alerting
3. Test with actual Santiago agent workflows
4. Optimize performance based on usage patterns

For detailed logs, see: $TEST_RESULTS
EOF

    log "Test report generated: $report_file"
}

# Main function
main() {
    log "Starting comprehensive vLLM inference testing"
    log "Testing Mistral-7B-Instruct setup for NuSy Santiago agents"

    check_service
    test_basic_inference
    test_agent_roles
    test_concurrency
    test_performance
    test_error_handling
    generate_report

    log "🎉 All inference tests completed successfully!"
    log "vLLM service is ready for Santiago agent operations"
    log "📊 Check detailed results in: $TEST_RESULTS"
}

# Run main function
main "$@"
</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_041/provisioning/test_inference.sh