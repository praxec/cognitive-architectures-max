# cognitive-architectures-max

The **max-tier UX factory** layered on [`cognitive-architectures`](../cognitive-architectures).

Where the base repo ships the SWE lifecycle (`flow.add-feature` and the `cap.*`
it depends on), this repo ships the capabilities, skills, and workflows that turn
**JTBD core-job research into superior, grounded user experiences** — built and
verified through praxec, dogfooding praxec and its tools.

## Leverages
- **intentos** (`intentos-mcp`) — intent / JTBD modeling → `connections/intentos.yaml` *(P3)*
- **structureos** (`structureos-mcp`) — structural hygiene (god files, complexity, cycles)
- **elicitation** (`elicitation`) — falsification-based structured discovery

## Wiring
Reference **both** repos from your gateway config (this one layers on the base):

```yaml
repos:
  - path: /path/to/cognitive-architectures      # base SWE pack
  - path: /path/to/cognitive-architectures-max   # this — UX factory
```

Every loaded definitionId is namespace-prefixed `cognitive-max/<id>`.

## Contents (by sub-project)
- **P1 — UI-verify pack** *(this)*: `scripts-library/verify.ui.green.yaml`,
  `capabilities/cap.verify.ui-green.yaml`, `orchestrators/flow.add-ui-feature.yaml`.
  Makes praxec able to verify a TypeScript/Vite frontend (the base pack is
  cargo-only) and to run a full-stack feature with both `cargo-green` and
  `ui-green` gates. See `docs/spec-p1-ui-verify-pack.md`.
- **P2** — PhD atomic-design UI skill *(planned)*
- **P3** — JTBD→UX projection workflow (wires `intentos` + `elicitation` + `structureos`) *(planned)*
- **P4** — praxec-management capability *(planned)*

This repo is part of the **Grounded-UX Factory** program: a configuration that
generates every backend-IA projection as a JTBD-grounded user experience.
