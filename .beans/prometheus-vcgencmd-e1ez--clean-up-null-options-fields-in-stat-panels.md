---
# prometheus-vcgencmd-e1ez
title: Clean up null options fields in stat panels
status: completed
type: task
priority: normal
created_at: 2026-01-31T09:06:07Z
updated_at: 2026-01-31T09:08:52Z
---

Several stat panels have `"options": null` which is redundant. Either omit the field entirely or use an empty object `{}` for cleaner JSON.

## Summary of Changes\n\nAdded post-processing step at `generate-dashboard.py:377-378` to remove null options fields from the generated JSON. Null options are now deleted rather than serialized.
