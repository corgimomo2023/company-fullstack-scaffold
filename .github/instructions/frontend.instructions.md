---
applyTo: "frontend/src/**/*.{ts,tsx},frontend/*.{ts,js,json}"
---
Follow `frontend/AGENTS.md`. Keep `shared → features → app` dependencies one-way. Use MSW at the network boundary in integration tests; do not add per-test global fetch mocks. Verify loading, empty, error, success and keyboard behavior.
