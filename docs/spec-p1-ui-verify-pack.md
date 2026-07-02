# P1 — UI-verify pack (spec)

**Goal:** make praxec able to verify a TypeScript/Vite frontend, so the
`flow.add-feature`-style pipeline can build and gate UI work (the base
`cognitive-architectures` pack is cargo/Rust-only). This is the prerequisite
that unblocks every later UX projection in the Grounded-UX Factory program.

## Deliverables
1. **`scripts-library/verify.ui.green.yaml`** — a deterministic bash gate
   mirroring `verify.workspace.green` (cargo). Takes the ui dir as `$1`; runs
   `npm ci` → `npx tsc --noEmit` → `npx vite build`; `stage_fail`s with
   `{"passed":false,"failed_stage":…}` on any failure; emits
   `{"passed":true,"stages":["install","typecheck","build"]}` on success.
   Exits 0 only if all stages pass.
   - **Honest scope:** the target UI (`simuli/ui`) has **no eslint** configured
     (its `npm run build` is `tsc --noEmit && vite build`), so the gate is
     install/typecheck/build. An eslint stage is an opt-in future add once the
     UI project adopts an eslint config.
2. **`capabilities/cap.verify.ui-green.yaml`** — a single-state `verify`
   capability (mirrors `cap.verify.stub-scan`): `kind: script` executor binding
   subject `verify.ui.green`, positional arg `$.workflow.input.ui_path`, outputs
   `passed` + `failed_stage` from `$.output.json.*`.
3. **`orchestrators/flow.add-ui-feature.yaml`** — a full-stack variant of
   `cognitive/flow.add-feature`: same plan→vet→signoff→TDD→gap-track pipeline,
   but the verify phase runs **two** sequential deterministic gates —
   `cognitive/cap.verify.workspace-green` (backend) then
   `cognitive-max/cap.verify.ui-green` (frontend) — both must pass before the
   adversarial review. Adds a `ui_path` input (default `ui`).
4. **`praxec.repo.yaml`** — the repo manifest (schema `praxec.repo/v1`,
   namespace `cognitive-max`, layout mirroring the base repo).

## Verification status
- **Done:** all four files written; YAML parses; shapes mirror the proven base
  templates (`verify.workspace.green`, `cap.verify.stub-scan`, `flow.add-feature`).
- **Pending a live load-test** (requires the gateway configured with BOTH repos):
  1. the gateway loads `cognitive-max/*` without error;
  2. `flow.add-ui-feature`'s **cross-namespace** executor references
     (`cognitive/cap.*` from the base repo + `cognitive-max/cap.verify.ui-green`)
     resolve — this is the one real uncertainty (the base `flow.add-feature` uses
     bare same-namespace ids; cross-repo references are assumed but unproven);
  3. `verify.ui.green` runs green against `simuli/ui` (install/typecheck/build).
- **Risk/fallback:** if cross-namespace executor references do NOT resolve, the
  fix is to either (a) fully-qualify ids per the gateway's actual reference
  syntax, or (b) ship `flow.add-ui-feature` inside the base repo instead. The
  `verify.ui.green` script + `cap.verify.ui-green` (the core prerequisite) are
  independent of this and stand alone.

## Next (P2/P3)
Once the load-test passes, `flow.add-ui-feature` is the build vehicle for SP3's
frontend and every later UX projection. P2 (the atomic-design UI skill) and P3
(the JTBD→UX workflow wiring `intentos`/`elicitation`/`structureos`) build on it.
