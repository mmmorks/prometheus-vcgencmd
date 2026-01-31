---
# prometheus-vcgencmd-dj9l
title: Fix Memory OOM Metrics panel height mismatch
status: completed
type: bug
priority: normal
created_at: 2026-01-31T09:06:07Z
updated_at: 2026-01-31T09:07:38Z
blocked_by:
    - prometheus-vcgencmd-fyb8
---

Memory OOM Metrics panel has height 6 while Ring Oscillator Speed has height 8. They sit at the same Y position (20) but different heights, causing visual inconsistency. Align heights after fixing the positioning issue.

## Summary of Changes\n\nChanged Memory OOM Metrics panel from `size=(6, 12)` to `Size.HALF` (8, 12) in `generate-dashboard.py:300` to match the Ring Oscillator Speed panel height.
