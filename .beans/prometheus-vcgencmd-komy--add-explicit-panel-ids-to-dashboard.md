---
# prometheus-vcgencmd-komy
title: Add explicit panel IDs to dashboard
status: completed
type: task
priority: normal
created_at: 2026-01-31T09:06:07Z
updated_at: 2026-01-31T09:07:58Z
---

Panels are missing `id` fields. Grafana auto-generates these, but explicit IDs provide stability for panel linking and references. Add sequential IDs to all 15 panels.

## Summary of Changes\n\nAdded explicit sequential panel IDs (1-15) in the post-processing section at `generate-dashboard.py:374`. IDs are assigned during JSON generation to ensure stability for panel linking.
