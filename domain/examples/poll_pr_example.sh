#!/bin/bash
# Example: Poll PR until ready and auto-merge
# 
# This demonstrates Phase 5 polling functionality added to F-030

# Poll PR #14 with these settings:
# - Check every 60 seconds
# - Maximum wait time: 120 minutes (2 hours)
# - Auto-merge when ready (approved + checks passing + mergeable)

python -m src.nusy_pm_core.adapters.pr_workflow_manager poll-pr 14 \
  --interval 60 \
  --max-duration 120 \
  --auto-merge

# Example output when PR becomes ready:
# 🔄 Starting PR #14 polling...
#    Interval: 60s
#    Max duration: 120 minutes
#    Auto-merge: enabled
#
# [Check #1 at 0.0m]
#   State: OPEN
#   Approved: ❌
#   Mergeable: ✅
#   Checks: ⏳
#   ⏳ Next check in 60s...
#
# [Check #2 at 1.0m]
#   State: OPEN
#   Approved: ✅
#   Mergeable: ✅
#   Checks: ✅
#
# ✅ PR #14 is READY!
# 🚀 Auto-merging PR #14...
# ✅ Auto-merge successful!
#
# Polling Summary:
#   Checks performed: 2
#   Time elapsed: 1.0 minutes
