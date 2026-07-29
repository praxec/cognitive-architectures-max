# Migrate -max UI flows onto the `flow.change` atom

Worktree: `/home/mc/working/cog-arch-max-ui`, branch `feat/migrate-max-ui-changeatom` (off -max dev).
Base pack used for validation currency: `/home/mc/working/cog-arch-dev-base` (cog-arch dev, carries
`flow.change`'s `build_mode`/`verify_mode`/`build_skills`). The repo's own `examples/praxec-cognitive-max.yaml`
still points at the stale `../../cognitive-architectures` checkout — untouched, per instructions (not committed).

## Migration 1 — `flow.refactor.to-atomic-design` — MIGRATED

**Before:** `signoff_received` → `refactoring` (`cap.implement.tdd-loop` direct, `plan: decomposition_plan`,
`scope_paths: target_path`) → `verifying_ui` (`hop_slot: verify` → `cognitive-max/cap.verify.ts`) →
`ui_verified` (guard `$.context.verify.status == 'pass'`) → `reviewing`.

**After:** `signoff_received` → `changing` (`kind: workflow` → `cognitive/flow.change`, `build_mode: "tdd"`,
`deliverable: $.context.decomposition_plan`, `backstop_cwd: $.run.repo_root`) → `change_gate` (guards
`impl_files_changed >= 1` AND `ws_verify.status == 'pass'`) → `reviewing`. `reviewing`/`reviewed` tail and
the `planning_decomposition`→`awaiting_signoff`→`signoff_received` prefix are byte-identical.

**Deliverable mapping:** `deliverable` = the same `decomposition_plan` object `refactoring` used to pass
tdd-loop as `plan`. `target_path` (previously threaded as `scope_paths`) is no longer threaded explicitly —
flow.change's `building_tdd` arm always binds the WHOLE `deliverable` as `scope_paths` for every TDD-mode
caller (a convention already baked into the atom, shared with `flow.add-feature`); this is an atom-design
choice, not a regression introduced by this migration. `backstop_cwd: $.run.repo_root` — this flow operates
on one repo (no multi-repo re-root needed), the same value every existing base-pack `flow.change` caller
(`flow.implement.deliverable`, `flow.shared.mini-vee`, `flow.behavioral-coverage`) passes. ts stack is
auto-detected by flow.change's `inspect.stack` (deliverable.stack, else repo filesystem sniff).

**Dropped slot:** `refactor_result` (write-only — grepped, never read by any guard/template in the flow) is
dropped because flow.change does not surface the inner builder's raw `result` object as a top-level output
(its `outputs:` are `base_commit` / `impl_files_changed` / `ws_verify` only). Replaced by those three
DoD-evidence slots, seeded in `initialContext` exactly as `flow.implement.deliverable` (the canonical wrap
pattern) does.

## Migration 2 — `flow.ui.optimal` — MIGRATED (faithful)

**Before:** `signoff_gate` → `building` (`scope.skills: [implement.tdd.behavioral-discipline,
implement.atomic.component-design, implement.storybook.author, review.react.best-practices]`,
`cap.implement.tdd-loop` direct, `plan: design_plan`, `scope_paths: ui_path`) → `verifying_ui`
(`hop_slot: verify`) → `ui_gate` (guard `$.context.verify.status == 'pass'`) → `reviewing_react`.

**After:** `signoff_gate` → `changing` (`kind: workflow` → `cognitive/flow.change`, `build_mode: "tdd"`,
`deliverable: $.context.design_plan`, `backstop_cwd: $.run.repo_root`, `build_skills: <the 4 skills' bodies,
verbatim>`) → `change_gate` (same two guards as migration 1) → `reviewing_react`. `designing` → FMECA
converge-loop → `awaiting_signoff`/`signoff_gate` prefix and the `reviewing_react` → `react_gate` →
`reviewing_adversarial` → `adversarial_gate` → `opening_pr` tail are byte-identical.

### The skills-faithfulness question — verdict: **MIGRATED-FAITHFUL**

Investigated the engine mechanism directly (mcp-flowgate source):

- `scope.skills` on a state is collected by `collect_in_scope_skill_subjects`
  (`crates/praxec-core/src/runtime/runtime_links.rs:232-247`), resolved against the workflow's own
  `_skillsLibrary` snapshot, and each skill's `body` is injected **verbatim** into the agent's **system
  prompt** — formatted `## {verb}.{subject}\n\n{body}` (`crates/praxec-core/src/skills.rs:29-64`), composed
  in `crates/praxec-agents/src/rig_runner.rs:181-195` behind the always-on completion/coding protocol text.
- A state's `goal:` field is a **separate channel** — rendered via the templating engine
  (`crates/praxec-core/src/templating.rs:29`) into the **user prompt** (`crates/praxec-agents/src/executor.rs:704-724`).
- `scope.skills` is **strictly per-definition**: `assemble_system_message` is always called against
  `request.workflow.definition` — the *currently executing* workflow's own JSON. A `kind: workflow`
  transition starts a **fresh** child mission (`crates/praxec-executors/src/workflow.rs:334-338`) that loads
  its own definition/`_skillsLibrary` from scratch; only `use.inputs` values cross the boundary. There is no
  mechanism that copies a parent's `skills:` array into a child. So `building`'s `scope.skills` NEVER reached
  `cap.implement.tdd-loop`'s own agent state even *before* this migration — the sub-mission boundary already
  cut it off. (`cap.implement.tdd-loop`'s own header names this exact gap and names `flow.ui.optimal` as the
  caller it was built to fix: "*A workflow-state `scope.skills` list cannot reach a nested sub-mission's own
  agent state, which is what this replaces/supplements for a caller like flow.ui.optimal that invokes this
  cap as a sub-workflow.*")
- `craft_guidance` (the cap's own input) is templated into the `iterating` state's `goal:` — i.e. it rides
  the **same user-prompt channel** `goal:` always used, not a new one.

**Conclusion:** the mechanism changes — system-prompt-via-ID-resolution → inline text in the templated
user-goal — but (a) this input was purpose-built by the base pack for exactly this caller, (b) the
substantive guidance content is preserved **verbatim** (the four skill bodies, copied byte-for-byte from
`skills/implement.tdd.behavioral-discipline.yaml`, `implement.atomic.component-design.yaml`,
`implement.storybook.author.yaml`, `review.react.best-practices.yaml`, in the same order, headed
`## <skill-id>` for traceability back to the library), and (c) both channels land in the same LLM call to
the same model. Nothing is dropped, summarized, or paraphrased. This is a documented mechanism swap, not a
lossy shortcut — migrated.

**Dropped slot:** `implementation_result` (write-only, same reasoning as migration 1) → replaced by
`base_commit`/`impl_files_changed`/`ws_verify`.

## hop_slot / strict-blackboard-mode handling

Both flows declared a `hop_slot: verify` transition and a non-empty `blackboard:` block, with a comment
claiming "hop_slot injection puts this flow in strict-blackboard mode." Investigated the validator directly
(`crates/praxec-core/src/validate.rs`): strict-blackboard enforcement (`check_use_before_def`, the SPEC §11
guard/template use-before-def check) is triggered by the **presence of the `blackboard:` block itself**
(`declared_blackboard_slots`, `validate.rs:1544-1555`, checked at `validate.rs:1392`) — **not** by `hop_slot`.
`hop_slot` only auto-injects a typed slot shape (e.g. `verify`) into that block while it exists
(`HOP_SLOT_BLACKBOARD_SHAPE`, `config.rs:1004-1021`); it doesn't gate whether strict mode runs at all.

Consequence for this migration: removing the sole `hop_slot: verify` transition does **not** relax strict
mode, since the `blackboard:` block itself was kept (not emptied) in both flows. I declared the new slots
(`base_commit`, `impl_files_changed`, `ws_verify`) the remaining guards (`change_gate`) actually read, and
dropped the old auto-injected `verify` slot reference since no guard reads it anymore. Had I instead deleted
the whole `blackboard:` block (reasoning "hop_slot is gone, so is the reason for strict mode"), that would
have silently relaxed §11 enforcement for every other guard in the flow — the real risk flagged by the
investigation. Both flows keep their `blackboard:` blocks fully declared; strict mode is unchanged.

## Verify

`praxec check` run against a temp config (not committed) at
`/tmp/claude-1000/.../scratchpad/praxec-cognitive-max-ui.TEMP.yaml`, repointing the base-pack `repos:` entry
from `../../cognitive-architectures` to the absolute `/home/mc/working/cog-arch-dev-base` (current base with
`flow.change`'s `build_mode`/`verify_mode`/`build_skills`), overlay at `/home/mc/working/cog-arch-max-ui`
(priority 10, unchanged from the shipped example). Result:

```
validation: 0 error(s), 5 warning(s), 0 soft warning(s)
```

Both migrated flows (`cognitive-max/flow.refactor.to-atomic-design`, `cognitive-max/flow.ui.optimal`)
registered and loaded cleanly. The 5 warnings are pre-existing and unrelated to this migration
(ELICITATION_INCOMPATIBLE_GATE on `flow.refactor.god-file` / `cap.implement.build-loop` /
`cap.implement.build-loop-pkg`, plus the standing dev-mode EPHEMERAL_STORAGE warning) — verified by grepping
the output for the two migrated flow names alongside `error`: zero errors, both flows present.

The binary used was the locally-installed `praxec 0.0.40` (`~/.cargo/bin/praxec`); no rebuild was required —
it already resolved flow.change's new inputs cleanly against the current base checkout.

## Commit

Both flows migrated and committed together on `feat/migrate-max-ui-changeatom`.
