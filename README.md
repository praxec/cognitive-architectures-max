# cognitive-architectures-max

The **max-tier UX factory** layered on [`cognitive-architectures`](../cognitive-architectures).

Where the base repo ships the SWE lifecycle (`flow.add-feature` and the `cap.*`
it depends on), this repo ships the capabilities, skills, and workflows that turn
**JTBD core-job research into superior, grounded user experiences** — built and
verified through praxec, dogfooding praxec and its tools.

## Leverages
- **structureos** (`structureos-mcp`) — structural hygiene (god files, complexity, cycles). Reference connection ships **in this repo** → `connections/structureos.yaml`.
- **elicitation** (`elicitation`) — falsification-based structured discovery (base-repo connection; consumed by `flow.ux.discovery`).
- **intentos** (`intentos-mcp`) — intent / JTBD modeling *(P4-planned; `connections/intentos.yaml` not yet shipped)*.

## Wiring
Reference **both** repos from your gateway config (this one layers on the base):

```yaml
repos:
  - path: /path/to/cognitive-architectures      # base SWE pack
  - path: /path/to/cognitive-architectures-max   # this — UX factory

# The flows here have agent-driven steps (`actor: agent`) and declare
# `outcomes` for headless auto-drive, so a models file is required to actually
# run them (the transition chooser needs a model). On praxec 0.0.14 a config
# that additionally declares a `kind: agent` step or `auto_drive: true` also
# fails `praxec check` up front with AGENT_MODELS_YAML_REQUIRED.
gateway:
  models_yaml: .praxec/models.yaml   # canonical path (NOT the legacy agents.yaml)

# Governance state must be durable — `serve` refuses store.kind file/memory:
store:
  kind: sqlite
  path: .praxec/state.db

# Audit events stream to stderr (stdout is the MCP transport).
```

Every loaded definitionId is namespace-prefixed `cognitive-max/<id>`.

## Contents (by sub-project)
- **P1 — UI-verify pack** *(shipped)*: `scripts-library/verify.ui.green.yaml`,
  `capabilities/cap.verify.ui-green.yaml`, `orchestrators/flow.add-ui-feature.yaml`.
  Makes praxec able to verify a TypeScript/Vite frontend (the base pack is
  cargo-only) and to run a full-stack feature with both `cargo-green` and
  `ui-green` gates. See `docs/spec-p1-ui-verify-pack.md`.
- **P2 — UX craft library** *(shipped)*: the design-science skills
  (`skills/plan.hci.*`, `plan.bff.*`, `plan.sdui.*`, `plan.nfr.*`,
  `plan.spec.incose-ears`, `implement.atomic.*`, `implement.storybook.*`,
  `implement.tdd.*`, `review.react.*`, `review.fmeca.*`, `diagnose.debug.*`)
  plus the caps that surface them (`cap.plan.ui-design`,
  `cap.review.react-antipatterns`, `cap.diagnose.root-cause`).
- **P3 — optimal UX flows** *(shipped)*: `orchestrators/flow.ui.optimal.yaml`
  (HCI+JTBD-grounded design → FMECA → build → verify → review → PR),
  `flow.ux.discovery.yaml` (elicitation-gated discovery front-stage),
  `flow.debug.systematic.yaml`, `flow.refactor.to-atomic-design.yaml`, and
  `flow.refactor.god-file.yaml` (StructureOS-driven god-file split).
  See `docs/spec-flow-ui-optimal.md` / `docs/spec-elicit-front-stage.md`.
- **P4 — intentos measurement loop** *(partial)*: `cap.run.ux-simulation` +
  `scripts-library/run.preveti.ux-study.yaml` measure a built UI against the
  intended users' JTBD; the `intentos` connection wiring is still to come.

This repo is part of the **Grounded-UX Factory** program: a configuration that
generates every backend-IA projection as a JTBD-grounded user experience.
