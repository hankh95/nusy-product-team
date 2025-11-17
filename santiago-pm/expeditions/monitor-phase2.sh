#!/bin/bash
# Phase 2 Real-Time Monitoring Script
# Tracks GitHub agent PR progress for mini expedition

set -e

EXPEDITION_FILE="santiago-pm/expeditions/2025-11-16-hybrid-coordination-mini-expedition.md"
ISSUE_NUMBERS="5 6 7"
PR_NUMBERS="8 9 10 11"

echo "=== Phase 2 Agent Progress Monitor ==="
echo "Expedition: hybrid-coordination-001"
echo "Started: $(date)"
echo ""

# Function to get PR status
get_pr_status() {
    gh pr view "$1" --json state,isDraft,reviews,statusCheckRollup 2>/dev/null || echo "PR not found"
}

# Function to get issue status
get_issue_status() {
    gh issue view "$1" --json state,assignees,comments 2>/dev/null || echo "Issue not found"
}

# Monitor PRs
echo "📊 Pull Request Status:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for pr in $PR_NUMBERS; do
    echo ""
    echo "PR #$pr:"
    gh pr view "$pr" --json number,title,state,isDraft,headRefName,author,createdAt,updatedAt \
        --jq '{
            number,
            title,
            state,
            isDraft,
            branch: .headRefName,
            author: .author.login,
            created: .createdAt,
            updated: .updatedAt
        }' 2>/dev/null | jq -r '
        "  Title: \(.title)",
        "  State: \(.state) (Draft: \(.isDraft))",
        "  Branch: \(.branch)",
        "  Author: \(.author)",
        "  Created: \(.created)",
        "  Updated: \(.updated)"
    ' || echo "  ❌ PR not found"
    
    # Check CI status
    echo "  CI Status:"
    gh pr checks "$pr" --json name,status,conclusion 2>/dev/null | jq -r '.[] | "    - \(.name): \(.status) (\(.conclusion // "pending"))"' || echo "    No checks"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Monitor Issues
echo "🎯 Issue Status:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for issue in $ISSUE_NUMBERS; do
    echo ""
    echo "Issue #$issue:"
    gh issue view "$issue" --json number,title,state,assignees,comments \
        --jq '{
            number,
            title,
            state,
            assignee: .assignees[0].login,
            comment_count: (.comments | length)
        }' 2>/dev/null | jq -r '
        "  Title: \(.title)",
        "  State: \(.state)",
        "  Assignee: \(.assignee // "unassigned")",
        "  Comments: \(.comment_count)"
    ' || echo "  ❌ Issue not found"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Calculate Phase 2 metrics
echo "⏱️  Phase 2 Timing:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Get first PR creation time (Phase 2 start)
PHASE2_START=$(gh pr view 8 --json createdAt --jq '.createdAt' 2>/dev/null || echo "")
if [ -n "$PHASE2_START" ]; then
    START_SECONDS=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$PHASE2_START" +%s 2>/dev/null || echo "")
    NOW_SECONDS=$(date +%s)
    
    if [ -n "$START_SECONDS" ]; then
        ELAPSED=$((NOW_SECONDS - START_SECONDS))
        ELAPSED_MIN=$((ELAPSED / 60))
        echo "  Phase 2 started: $PHASE2_START"
        echo "  Elapsed time: ${ELAPSED_MIN} minutes"
        echo "  Target: 60-120 minutes (parallel implementation)"
    fi
else
    echo "  ⏳ Phase 2 not started yet"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Summary
echo "📈 Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
OPEN_PRS=$(gh pr list --json state --jq '[.[] | select(.state == "OPEN")] | length')
DRAFT_PRS=$(gh pr list --json isDraft --jq '[.[] | select(.isDraft == true)] | length')
READY_PRS=$((OPEN_PRS - DRAFT_PRS))

echo "  Open PRs: $OPEN_PRS"
echo "  Draft PRs: $DRAFT_PRS"
echo "  Ready for Review: $READY_PRS"
echo ""
echo "  Phase 2 Status: $([ $READY_PRS -eq 0 ] && echo "🚧 IN PROGRESS" || echo "✅ READY FOR REVIEW")"
echo ""

echo "Run this script again to refresh status"
echo "Or use: watch -n 30 ./santiago-pm/expeditions/monitor-phase2.sh"
