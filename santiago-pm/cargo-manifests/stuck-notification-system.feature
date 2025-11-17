---
id: pm-artifact-cargo-manifest-stuck-notification-20250130
type: cargo-manifest
status: draft
created_at: 2025-01-30
updated_at: 2025-01-30
assignees: []
labels:
  - type:feature
  - component:orchestration
  - priority:high
  - nautical:cargo-manifest
epic: phase-1-factory-components
domain: orchestration
owners: ["santiago-pm"]
stakeholders: ["developers", "santiago-agents"]
knowledge_scope: lake
skill_level: journeyman
artifact_kinds: ["feature-specification"]
related_artifacts:
  - navigator.py
  - catchfish.py
  - fishnet.py
  - base_proxy.py
---

# 🧭 Cargo Manifest — AI Agent Stuck Notification System
*Feature Specification (Nautical Theme)*

> **Purpose:** A notification system that alerts the user when an AI agent encounters a blocker during autonomous work, providing clear context and actionable next steps.  
> This artifact is read by: Santiago-PM, Santiago-Architect, Developers, QA, and all Proxy Agents.

---

## 1. Summary (The Cargo at a Glance)

**Feature Title:** AI Agent Stuck Notification System  
**Epic:** Phase 1 - Factory Components  
**Primary Owner:** santiago-pm  
**Crew Roles Involved:** All Proxy Agents (PM, Architect, Developer, QA, UX), Navigator, Catchfish, Fishnet  
**Motivation (Why Now):**  
During autonomous development sessions, AI agents may encounter blockers (missing dependencies, API limits, invalid configurations) that require human intervention. Without explicit notifications, these blockers cause silent failures or context drift.

**Expected Impact:**  
- 🔔 Users receive immediate notification when AI encounters blockers
- 📊 Clear context about what failed and why
- 🛠️ Actionable next steps to unblock autonomous work
- ⏱️ Reduced debugging time from hours to minutes
- 🚀 Faster autonomous development cycles

---

## 2. Problem Statement (Waters to Navigate)

During autonomous development, AI agents can hit various blockers:
- **Missing system dependencies** (Redis server, Docker, databases)
- **API rate limits or quota exhaustion** (OpenAI, xAI tokens)
- **Invalid configurations** (missing API keys, wrong paths)
- **External service failures** (network issues, service downtime)
- **Circular dependencies** (Task A needs Task B, but Task B needs Task A)

**Current Condition:**  
Agents either:
1. Continue working with degraded results
2. Move to next task without flagging blocker
3. Fail silently with error buried in logs
4. Retry indefinitely, burning tokens

**Desired Condition:**  
Agent detects blocker → Pauses work → Sends structured notification → User receives clear alert with:
- What was being attempted
- Why it failed
- Exact commands/steps to resolve
- Which tasks are blocked downstream

---

## 3. Hypothesis & Experiments (Charting the Course)

### Primary Hypothesis
**"If we implement a structured notification system for agent blockers, then users will resolve issues 10x faster and autonomous development will proceed with 50% fewer manual check-ins."**

### Experiments to Validate

#### Experiment 1: Redis Server Blocker Notification
**Given:** Agent attempts Redis coordination demo  
**When:** Redis server not installed/running  
**Then:** User receives notification:
```
🚫 BLOCKED: Redis Message Bus Demo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task: demo_redis_coordination.py
Reason: Redis server not running
Impact: 1 demo blocked, message bus coordination untestable

User Action Needed:
1. Install Redis: brew install redis
2. Start server: redis-server
3. Verify: redis-cli ping (should return PONG)
4. Re-run: python demo_redis_coordination.py

Downstream Impact:
- ⏸️ Multi-agent coordination patterns untested
- ⏸️ Real-time message routing unvalidated
```

**Success Metrics:**
- Notification delivered within 5 seconds of blocker detection
- User resolves blocker without needing to read logs
- Agent resumes from exact checkpoint after unblock

#### Experiment 2: API Quota Exhaustion Notification
**Given:** Agent making LLM calls during Navigator orchestration  
**When:** OpenAI quota exhausted (429 rate limit)  
**Then:** User receives notification:
```
🚫 BLOCKED: OpenAI API Quota Exhausted
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task: Navigator Step 3 - Design Validation
Reason: Rate limit reached (429 Too Many Requests)
Impact: Phase 1 orchestration paused

User Action Needed:
1. Check quota: https://platform.openai.com/usage
2. Either:
   a. Wait 60 seconds for rate limit reset
   b. Upgrade plan for higher limits
   c. Switch to xAI (Grok) as fallback
3. Continue: Agent will auto-retry in 60s

Fallback Options:
- ✅ Switch Architect to Grok-4-fast (available)
- ✅ Use GPT-5-nano for simple tasks (lower rate)
```

**Success Metrics:**
- Clear distinction between temporary (rate limit) vs permanent (quota) blocks
- Fallback options presented with one-click switches
- Auto-retry after cooldown period

#### Experiment 3: Circular Dependency Detection
**Given:** Navigator orchestrating factory components  
**When:** Catchfish needs Fishnet output, but Fishnet needs Catchfish input  
**Then:** User receives notification:
```
🚫 BLOCKED: Circular Dependency Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task: Phase 1 Factory Integration
Dependency Chain:
  Catchfish.extract() requires Fishnet.contracts
    └─> Fishnet.generate() requires Catchfish.entities
        └─> Creates circular dependency

User Action Needed:
1. Review architecture: docs/ARCHITECTURE.md
2. Choose resolution:
   a. Catchfish extracts raw entities first
   b. Fishnet uses mock contracts for bootstrap
   c. Add intermediate adapter layer
3. Update: santiago_builder/navigator.py orchestration

Suggested Resolution:
Two-phase approach:
  Phase 1a: Catchfish extracts without contracts
  Phase 1b: Fishnet generates contracts from raw entities
```

**Success Metrics:**
- Circular dependencies detected before execution
- Visual dependency graph shown in notification
- Multiple resolution strategies suggested

---

## 4. Feature Behaviors (Behavioral Patterns)

### Core Behaviors

**Behavior 1: Blocker Detection**
```gherkin
Feature: Detect Agent Blockers
  As an AI agent
  I want to detect when I'm blocked
  So that I can notify the user instead of failing silently

  Scenario: System Dependency Missing
    Given I am attempting to start Redis message bus
    When redis-server command not found
    Then I should detect "SYSTEM_DEPENDENCY_MISSING" blocker
    And capture dependency name "redis-server"
    And capture installation command "brew install redis"

  Scenario: API Error Threshold
    Given I am making LLM API calls
    When I receive 3 consecutive 5xx errors
    Then I should detect "API_UNAVAILABLE" blocker
    And capture provider name and error details
    And suggest fallback provider if available

  Scenario: Circular Dependency
    Given I am orchestrating task graph
    When Task A depends on Task B output
    And Task B depends on Task A output
    Then I should detect "CIRCULAR_DEPENDENCY" blocker
    And capture full dependency chain
    And suggest resolution strategies
```

**Behavior 2: Notification Formatting**
```gherkin
Feature: Format Blocker Notifications
  As a user
  I want blockers formatted clearly
  So that I can resolve them quickly

  Scenario: Rich Terminal Notification
    Given agent detects blocker
    When formatting notification for terminal
    Then include:
      | element            | requirement                          |
      | header             | 🚫 BLOCKED: [task name]             |
      | separator          | ━━━ visual divider                   |
      | context            | What was being attempted             |
      | reason             | Why it failed                        |
      | impact             | How many tasks blocked               |
      | action_steps       | Numbered resolution steps            |
      | commands           | Copy-pastable commands               |
      | downstream_impact  | What else is blocked                 |
      | fallback_options   | Alternative approaches               |

  Scenario: Structured JSON Notification
    Given agent detects blocker
    When serializing for API/logs
    Then format as:
      ```json
      {
        "blocker_id": "uuid",
        "timestamp": "2025-01-30T10:30:00Z",
        "severity": "high|medium|low",
        "category": "SYSTEM_DEPENDENCY|API_ERROR|CIRCULAR_DEPENDENCY",
        "task": {"id": "task-5", "name": "Navigator"},
        "reason": "Redis server not running",
        "resolution_steps": ["brew install redis", "redis-server"],
        "blocked_tasks": ["demo_redis_coordination.py"],
        "fallback_available": false,
        "auto_retry_after": null
      }
      ```
```

**Behavior 3: Notification Delivery**
```gherkin
Feature: Deliver Notifications
  As an AI agent
  I want to deliver notifications reliably
  So that users are always informed of blockers

  Scenario: Terminal Output (Primary)
    Given agent detects blocker during terminal session
    When delivering notification
    Then print to stdout with ANSI colors
    And ensure notification visible above other output
    And play system alert sound (optional)

  Scenario: Log File (Secondary)
    Given agent detects blocker
    When delivering notification
    Then append to test_workspace/blockers.jsonl
    And include full context for later analysis
    And timestamp for tracking blocker frequency

  Scenario: Provenance Log (Tertiary)
    Given agent detects blocker
    When logging to ships-logs
    Then create blocker_detected event
    And link to current task provenance
    And capture full agent state at blocker time
```

**Behavior 4: Blocker Resolution Tracking**
```gherkin
Feature: Track Blocker Resolution
  As a system
  I want to track how users resolve blockers
  So that I can improve detection and suggestions

  Scenario: User Resolves Blocker
    Given user receives blocker notification
    When user executes resolution steps
    And agent detects blocker cleared
    Then log resolution_time_seconds
    And log resolution_method (which suggestion used)
    And resume from checkpoint

  Scenario: User Skips Blocked Task
    Given user receives blocker notification
    When user says "skip this for now"
    Then mark task as "blocked_pending_user"
    And continue with non-dependent tasks
    And remind user at end of session

  Scenario: Blocker Auto-Resolves
    Given agent detects temporary blocker (rate limit)
    When cooldown period elapses
    And agent retries successfully
    Then log auto_resolution_success
    And continue without user intervention
```

---

## 5. Technical Design (Rigging & Tools)

### Architecture Components

**1. BlockerDetector Class**
```python
# Location: santiago_core/orchestration/blocker_detector.py

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

class BlockerCategory(Enum):
    SYSTEM_DEPENDENCY = "system_dependency"
    API_ERROR = "api_error"
    CIRCULAR_DEPENDENCY = "circular_dependency"
    CONFIGURATION_ERROR = "configuration_error"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    EXTERNAL_SERVICE = "external_service"

class BlockerSeverity(Enum):
    CRITICAL = "critical"  # Stops all work
    HIGH = "high"          # Blocks current task
    MEDIUM = "medium"      # Degraded performance
    LOW = "low"            # Warning only

@dataclass
class Blocker:
    blocker_id: str
    timestamp: datetime
    severity: BlockerSeverity
    category: BlockerCategory
    task_name: str
    task_id: Optional[str]
    reason: str
    resolution_steps: List[str]
    blocked_tasks: List[str]
    fallback_available: bool
    auto_retry_after: Optional[int]  # seconds
    metadata: Dict[str, Any]

class BlockerDetector:
    """Detects and classifies agent blockers"""
    
    def detect_system_dependency(self, command: str) -> Optional[Blocker]:
        """Detect missing system dependencies"""
        # Check if command exists
        # Return blocker with installation steps
        
    def detect_api_error(self, error: Exception, provider: str) -> Optional[Blocker]:
        """Detect API failures (rate limits, outages)"""
        # Parse error type
        # Determine if temporary or permanent
        # Return blocker with fallback options
        
    def detect_circular_dependency(self, task_graph: Dict) -> Optional[Blocker]:
        """Detect circular dependencies in task graph"""
        # Build dependency chain
        # Detect cycles using DFS
        # Return blocker with suggested resolutions
```

**2. NotificationFormatter Class**
```python
# Location: santiago_core/orchestration/notification_formatter.py

class NotificationFormatter:
    """Format blockers for different output channels"""
    
    def format_terminal(self, blocker: Blocker) -> str:
        """Format for terminal output with ANSI colors"""
        
    def format_json(self, blocker: Blocker) -> str:
        """Format as JSON for structured logging"""
        
    def format_markdown(self, blocker: Blocker) -> str:
        """Format as Markdown for documentation"""
```

**3. NotificationDelivery Class**
```python
# Location: santiago_core/orchestration/notification_delivery.py

class NotificationDelivery:
    """Deliver notifications via multiple channels"""
    
    def deliver_to_terminal(self, blocker: Blocker):
        """Print to stdout with formatting"""
        
    def deliver_to_log(self, blocker: Blocker):
        """Append to blockers.jsonl"""
        
    def deliver_to_provenance(self, blocker: Blocker):
        """Log to ships-logs with full context"""
```

**4. Integration with Base Proxy**
```python
# Location: santiago_core/agents/_proxy/base_proxy.py
# Add blocker detection to existing error handling

class BaseProxyAgent:
    def __init__(self, ...):
        self.blocker_detector = BlockerDetector()
        self.notification_delivery = NotificationDelivery()
    
    async def invoke_tool(self, tool_name: str, params: Dict[str, Any]):
        try:
            # Existing logic...
        except Exception as e:
            # Detect if this is a blocker
            blocker = self.blocker_detector.detect_api_error(e, provider)
            if blocker:
                self.notification_delivery.deliver_all(blocker)
                # Decide: retry, fallback, or raise
```

### Integration Points

**Navigator Orchestration**
```python
# Navigator detects circular dependencies before execution
# Validates all dependencies can be satisfied
# Notifies user if orchestration blocked

async def orchestrate_phase_1(self):
    # Build task graph
    task_graph = self._build_task_graph()
    
    # Check for circular dependencies
    blocker = self.blocker_detector.detect_circular_dependency(task_graph)
    if blocker:
        self.notification_delivery.deliver_all(blocker)
        return "BLOCKED"
    
    # Continue orchestration...
```

**Catchfish/Fishnet Integration**
```python
# Detect missing system dependencies
# Notify if external tools not available

async def extract_entities(self, source_path: Path):
    # Check for spaCy model
    if not self._has_spacy_model():
        blocker = Blocker(
            category=BlockerCategory.SYSTEM_DEPENDENCY,
            task_name="Catchfish Entity Extraction",
            reason="spaCy model 'en_core_web_lg' not installed",
            resolution_steps=[
                "python -m spacy download en_core_web_lg"
            ],
            ...
        )
        self.notification_delivery.deliver_all(blocker)
        return None
```

---

## 6. Acceptance Criteria (Proof of Seaworthiness)

### Must Have (Ship-Critical)

- [ ] **Blocker Detection**: All 6 blocker categories detectable
  - System dependencies (Redis, spaCy, Docker)
  - API errors (rate limits, outages)
  - Circular dependencies
  - Configuration errors (missing keys, wrong paths)
  - Resource exhaustion (disk, memory, tokens)
  - External service failures

- [ ] **Terminal Notifications**: Rich formatted output with:
  - 🚫 Visual header with blocker category
  - Clear reason and impact description
  - Numbered resolution steps
  - Copy-pastable commands
  - Downstream impact summary

- [ ] **Structured Logging**: JSON log to `test_workspace/blockers.jsonl`:
  - All blocker metadata
  - Timestamp and severity
  - Task context and dependencies
  - Resolution tracking

- [ ] **Provenance Integration**: Blocker events in ships-logs:
  - Linked to current task provenance
  - Agent state at blocker time
  - Full error context

- [ ] **Base Proxy Integration**: All proxy agents detect blockers:
  - PM, Architect, Developer, QA, UX
  - API errors caught and classified
  - User notified before retry/fallback

### Should Have (Valuable Cargo)

- [ ] **Auto-Retry**: Temporary blockers retry automatically:
  - Rate limits wait cooldown period
  - Network errors retry with exponential backoff
  - Success logged to analytics

- [ ] **Fallback Suggestions**: When alternative available:
  - Switch xAI ↔ OpenAI providers
  - Use lower-tier models (GPT-5.1 → gpt-5-nano)
  - Mock mode for testing

- [ ] **Resolution Tracking**: Measure blocker metrics:
  - Time to resolution (user action)
  - Resolution method (which suggestion)
  - Blocker frequency by category
  - Auto-resolution success rate

- [ ] **Checkpoint Resume**: After blocker resolved:
  - Agent resumes from exact state
  - No duplicate work
  - Task graph updated with completion status

### Could Have (Nice Additions)

- [ ] **Web Dashboard**: Real-time blocker monitoring
  - Current blockers with status
  - Historical blocker frequency
  - Resolution time trends

- [ ] **Slack/Email Notifications**: For long-running sessions
  - Send alert to user's preferred channel
  - Include resolution link

- [ ] **Blocker Analytics**: ML-powered insights
  - Predict blockers before they occur
  - Suggest proactive fixes
  - Identify blocker patterns

---

## 7. Non-Functional Requirements (Seaworthy Conditions)

### Performance
- Blocker detection: <100ms overhead
- Notification delivery: <1s to terminal
- Log append: Non-blocking async write

### Reliability
- 100% of critical blockers detected
- 0% false positives on auto-retry
- Notifications never lost (fallback to log if terminal unavailable)

### Usability
- Notifications readable at a glance (<5s comprehension)
- Resolution steps actionable (no debugging required)
- Copy-pastable commands work first try

### Observability
- All blockers logged with full context
- Blocker frequency tracked per category
- Resolution times measured

---

## 8. Implementation Plan (Voyage Itinerary)

### Phase 1: Core Detection (30 min)
1. Create `santiago_core/orchestration/blocker_detector.py`
2. Implement `Blocker` dataclass and enums
3. Implement `BlockerDetector` with 3 detection methods:
   - `detect_system_dependency()`
   - `detect_api_error()`
   - `detect_circular_dependency()`

### Phase 2: Formatting & Delivery (20 min)
1. Create `notification_formatter.py` with terminal/JSON/Markdown formats
2. Create `notification_delivery.py` with stdout/log/provenance channels
3. Add ANSI color support for rich terminal output

### Phase 3: Base Proxy Integration (15 min)
1. Update `base_proxy.py` to use `BlockerDetector`
2. Add blocker detection in `invoke_tool()` error handling
3. Add blocker detection in `_call_openai_api()` / `_call_xai_api()`

### Phase 4: Navigator Integration (10 min)
1. Add circular dependency detection to Navigator
2. Integrate blocker notifications in orchestration
3. Add checkpoint/resume logic

### Phase 5: Testing & Validation (15 min)
1. Create `tests/test_blocker_system.py`
2. Test all 6 blocker categories
3. Validate notification formats
4. Test Redis blocker (use as example)

### Total Estimate: 90 minutes (1.5 hours)

---

## 9. Success Metrics (Treasure Indicators)

### Quantitative
- **Blocker Detection Rate**: 100% of critical blockers detected
- **False Positive Rate**: <1% (no unnecessary notifications)
- **Time to Resolution**: <5 minutes average (vs 30+ minutes debugging logs)
- **Auto-Resolution Rate**: >80% of temporary blockers (rate limits, network)
- **Notification Delivery**: <1 second to terminal

### Qualitative
- **User Satisfaction**: "I knew exactly what to do to fix it"
- **Context Clarity**: "Didn't need to read logs or search docs"
- **Action Success**: "Commands worked first try"

### Adoption
- 100% of proxy agents using blocker detection
- Navigator orchestration validates dependencies before execution
- All autonomous sessions log blockers to analytics

---

## 10. Risks & Mitigations (Storm Warnings)

### Risk 1: Notification Fatigue
**Description:** Too many low-severity notifications annoy users  
**Impact:** Users ignore critical blockers  
**Mitigation:**
- Only notify on HIGH/CRITICAL severity
- Group similar blockers (5 rate limits → 1 notification)
- Add "suppress low-severity" config option

### Risk 2: False Positive Detection
**Description:** Agent detects blocker when work could continue  
**Impact:** Unnecessary interruptions, slower autonomous work  
**Mitigation:**
- Strict detection thresholds (3 consecutive errors before API blocker)
- Test detection logic thoroughly
- Add user feedback: "Was this a real blocker?" (yes/no)

### Risk 3: Performance Overhead
**Description:** Blocker detection slows down normal execution  
**Impact:** Agent performance degrades  
**Mitigation:**
- Keep detection logic lightweight (<100ms)
- Use async logging (non-blocking)
- Cache dependency checks (don't re-check Redis every call)

### Risk 4: Missing Blocker Categories
**Description:** New blocker types emerge that aren't detected  
**Impact:** Silent failures continue  
**Mitigation:**
- Generic "UNKNOWN" blocker category with raw error
- Analytics to identify frequent unclassified errors
- Iterative expansion of detection rules

---

## 11. Related Work & References (Charts & Maps)

### Internal References
- `ARCHITECTURE.md` - Phase 1 factory components
- `PHASE0_PROGRESS.md` - Proxy agent implementation patterns
- `base_proxy.py` - Error handling integration point
- `llm_router.py` - API provider fallback logic

### External Inspiration
- **GitHub Actions**: Error annotations with line numbers and suggestions
- **Terraform**: Clear "Error: ..." messages with resolution docs
- **Kubernetes**: kubectl describe shows events with reasons and messages
- **Railway.app**: Deployment failure notifications with logs and next steps

### Technical References
- Python subprocess error handling (CalledProcessError)
- OpenAI API error codes (429, 503, etc.)
- Graph cycle detection algorithms (DFS)
- ANSI terminal color codes (rich library)

---

## 12. Appendix (Navigation Notes)

### Example Blocker Notification (Redis)

```
🚫 BLOCKED: Redis Message Bus Demo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Task:     demo_redis_coordination.py
Category: SYSTEM_DEPENDENCY
Severity: HIGH

What Happened:
  Attempted to connect to Redis message bus for multi-agent 
  coordination patterns. Connection failed because Redis 
  server is not running.

Why It Failed:
  redis-server command not found in PATH
  Python redis client (7.0.1) is installed ✅
  Redis server is NOT installed ❌

Impact:
  • 1 demo script blocked: demo_redis_coordination.py
  • Message bus coordination untestable
  • Real-time agent communication patterns not validated

User Action Needed:
  1. Install Redis server:
     $ brew install redis

  2. Start Redis server:
     $ redis-server
     
  3. Verify server running:
     $ redis-cli ping
     # Should return: PONG

  4. Re-run demo:
     $ python demo_redis_coordination.py

Downstream Impact:
  ⏸️  Multi-agent coordination patterns untested
  ⏸️  Real-time message routing unvalidated
  ⏸️  Pub/sub architecture not demonstrated

Alternatives:
  • Continue without Redis (direct function calls only)
  • Mock message bus for demo purposes
  • Use Docker: docker run -d redis

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Logged to: test_workspace/blockers.jsonl
Timestamp: 2025-01-30T10:30:45Z
Blocker ID: blk_redis_20250130_103045
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Example Structured Log (blockers.jsonl)

```json
{
  "blocker_id": "blk_redis_20250130_103045",
  "timestamp": "2025-01-30T10:30:45Z",
  "severity": "high",
  "category": "SYSTEM_DEPENDENCY",
  "task": {
    "id": "demo-redis",
    "name": "Redis Coordination Demo",
    "file": "demo_redis_coordination.py"
  },
  "reason": "Redis server not running (redis-server command not found)",
  "resolution_steps": [
    "brew install redis",
    "redis-server",
    "redis-cli ping",
    "python demo_redis_coordination.py"
  ],
  "blocked_tasks": ["demo_redis_coordination.py"],
  "fallback_available": true,
  "fallback_options": [
    "Continue without Redis (direct function calls)",
    "Use Docker: docker run -d redis"
  ],
  "auto_retry_after": null,
  "metadata": {
    "python_redis_version": "7.0.1",
    "redis_server_installed": false,
    "agent": "autonomous-dev-session",
    "phase": "sprint-1-task-1"
  },
  "resolution": null,
  "resolved_at": null,
  "resolution_time_seconds": null
}
```

---

**Status:** Ready for Implementation  
**Next Steps:** 
1. Create BlockerDetector class
2. Integrate with base_proxy error handling
3. Test with Redis blocker example
4. Expand to all 6 categories
5. Add to Navigator orchestration
