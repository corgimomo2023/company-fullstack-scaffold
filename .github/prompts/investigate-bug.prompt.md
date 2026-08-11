---
description: Reproduce and diagnose a bug before changing production code
---
# Bug investigation

## Observed and expected behaviour
[Exact difference]

## Reproduction evidence
[Sanitized request ID, input, logs, screenshot or failing test]

## Required method
Read the nearest AGENTS.md. Reproduce with the smallest failing automated test. Trace the request across UI/API/service/repository boundaries. State the root cause with file:line evidence. Fix only after the test fails for the expected reason, then run the narrow test and `make check`. Report unresolved operational or data risks.
