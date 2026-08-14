# Frontend agent instructions

- Read root `DESIGN.md` before changing visual tokens, layout, components or interaction styling.
- Treat `DESIGN.md` as the visual source of truth; do not hardcode one-off brand colors in feature components.
- Put domain work under `src/features/<feature>/`; keep `App.tsx` composition-only.
- Server state belongs to TanStack Query. Form state belongs to React Hook Form. Validate at the boundary with Zod and keep server validation authoritative.
- Use semantic HTML, accessible names, visible focus, keyboard operation and responsive layouts.
- Call APIs only through `src/lib/api.ts` and feature API modules. Surface `request_id` in recoverable support errors.
- Every query UI needs loading, empty, error and success states. Mutation buttons need pending and failure states.
- Tests: `npm test`; full gate: `npm run lint && npm run typecheck && npm test && npm run build`.
