---
# prometheus-vcgencmd-fyb8
title: Fix Ring Oscillator Speed panel positioning
status: completed
type: bug
priority: normal
created_at: 2026-01-31T09:06:07Z
updated_at: 2026-01-31T09:07:24Z
---

The Ring Oscillator Speed panel at row 20 has `x: 12` with `w: 24`, which overflows the 24-unit grid. Should be `x: 0` for full width, or `w: 12` to sit beside Memory OOM Metrics panel.

## Summary of Changes\n\nChanged Ring Oscillator Speed panel from `Size.FULL` (24 units wide) to `Size.HALF` (12 units wide) in `generate-dashboard.py:311` so it sits beside the Memory OOM Metrics panel without overflowing the grid.
