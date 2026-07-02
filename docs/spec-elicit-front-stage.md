# Spec — the discovery (elicit) front-stage of the UX factory

The UX factory builds grounded user experiences from a brief. But a brief is a
*hypothesis*, not a spec. The **discovery front-stage** turns a vague brief into
an **aligned spec that has survived falsification** before any UI is designed —
so the factory builds the right thing, not just a well-built wrong thing.

It is backed by **elicitation** — a deterministic, offline, pure-compute
discovery-interview engine. Every claim is a hypothesis; standing
(`open → challenged → withstood / disproven`) is *computed*, never stored;
contradictions and coverage gaps are surfaced structurally; a readiness gate
reports whether the spec has *survived falsification* — never "is true". The
calling LLM does the fuzzy work (conversation → claims, voicing questions); the
server owns structure and state.

This realizes the falsification-first tenet: the factory's front door is a
falsification mechanism, not a rubber stamp.

## The full loop

```
ELICIT  (aligned spec, falsification-survived)
  -> flow.ui.optimal  (design -> customer-alignment FMECA -> signoff
                       -> TDD/story build -> ui-green verify
                       -> React + adversarial review -> PR)
  -> MEASURE  (cap.run.ux-simulation: real UX study via the Preveti API)
  -> REFINE   (findings -> new claims/evidence -> re-elicit) --+
  ^------------------------------------------------------------+
```

The exported spec is `flow.ui.optimal`'s `feature_brief` input. The two stages
chain at the operator level (the front-stage emits the spec; the operator
launches the build with it) rather than as one mega-flow — `flow.ui.optimal` is
a long, human-gated pipeline and the orchestrators here surface outputs through
`use:` maps, not a top-level `outputs:` block, so operator-level hand-off is the
clean, proven composition.

## Two drive paths (same engine)

The elicitation engine is the single source of structure/state for both.

### (a) Claude-driven — the default

When Claude is the running operator, Claude drives the elicitation tools
**directly** (the `elicitation` MCP server, wired in `simuli/.mcp.json`):
`session.open → question.next → append (add_claim | add_evidence | remediate)
→ readiness.assess → spec.export`. Claude asks the user one question at a time,
turns answers into candidate claims, and relays assent/refutation as evidence.

Operating procedure: the **`ux-discovery-front-stage`** Claude Code skill
(`simuli/.claude/skills/ux-discovery-front-stage/SKILL.md`).

### (b) Headless / auto-drive

When Claude is not the interactive operator, the praxec flow
**`cognitive-max/flow.ux.discovery`** runs the front-stage through the gateway:

1. `eliciting` — nests `cognitive/cap.plan.elicit-spec` (agent interview →
   structured spec → `feature_brief`).
2. `readiness_gate` — nests `cognitive/cap.verify.spec-readiness`, the
   **deterministic** `readiness.assess` call to elicitation via the gateway
   `elicitation` connection.
3. `gate` — `ready == true` → `aligned` (outcome `spec_ready`); else
   `not_ready` (fail-closed; read `blockers` and keep interviewing).

`flow.ux.discovery` declares `outcomes` + an `outcome: success` terminal, so it
is orchestrate-drivable (ADR-0009), and validates under
`praxec check` with the gateway loading both repos + the elicitation
connection.

## Status & runtime-dogfood follow-up

- **Wired + load-validated.** elicitation is available to Claude
  (`simuli/.mcp.json`); the headless flow composes the existing base-CA
  elicitation caps and passes `praxec check`.
- **Runtime-dogfood refinement (path b).** The deterministic gate reads the
  elicitation session named by `session_id`. For the gate to pass, that
  session must be populated with the falsification ledger. The base-CA agent
  elicit leaf (`cap.plan.elicit-spec`) is guidance-driven today; making it drive
  `session.open`/`append`/`spec.export` against `session_id` through the gateway
  connection (so the agent's interview lands in the same session the gate reads)
  is the next refinement. Until then the gate is correctly fail-closed: an
  unpopulated session reports not-ready. Path (a) has no such gap — Claude drives
  the tools directly.
- **Live run** of either path needs the provider env sourced
  (`~/.config/praxec/providers.env` + `simuli/.env`; never print key values)
  and, for path (a), a Claude restart so the `elicitation` MCP server loads.
