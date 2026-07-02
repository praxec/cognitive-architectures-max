# flow.ui.optimal — the optimal UI-build workflow (spec)

**Goal:** a praxec workflow that builds user interfaces grounded in *all* the
scientific knowledge of HCI **and** the intended users' researched JTBD core
job — and that is iterated, via grounded measurement, until it builds better
UIs than any other approach.

## Composition (what makes it "optimal")
One pipeline that injects the right expertise at each phase:

| Phase | Cap (base CA) | Skills injected (cognitive-max) |
|---|---|---|
| **designing** | `cap.plan.draft` | `hci.science.foundations`, `atomic.component.design`, `bff.pattern.api`, `sdui.server-driven-ui`, `spec.incose-ears`, `nfr.ilities-and-distributed` |
| **design_qa** | `cap.review.fmeca` (+fmeca-mcp) | `review.fmeca.customer-alignment` |
| **awaiting_signoff** | `cap.gate.human-signoff` | — (human) |
| **building** | `cap.implement.tdd-loop` | `tdd.behavioral.discipline`, `atomic.component.design`, `author.storybook`, `review.react.best-practices` |
| **verifying_ui** | `cognitive-max/cap.verify.ui-green` | — |
| **reviewing_react** | `cognitive-max/cap.review.react-antipatterns` | (binds `review.react.best-practices`) |
| **reviewing_adversarial** | `cap.review.adversarial` | — |
| **opening_pr** | `cap.coordinate.pr-open` | — |

Design science + JTBD ground the design; a customer-alignment FMECA gates it on
"does it serve the job?"; the build injects TDD + atomic + story-driven + React
best-practices so quality is authored in, not just reviewed; two review gates
(React-specific + general adversarial) catch what's left.

## Iterate-to-perfection loop (the goal's "iterate until perfected")
The workflow is a dogfood target, refined by evidence, not opinion:
1. **Run** it to build a real projection (P0 = the SP3 Study Convergence Board).
2. **Measure** the resulting UX with the product's own research/simulation
   engine — a `feature_need_discovery` / customer-alignment study simulated
   against the intended-user archetype (the same method that grounded SP3),
   plus real usability signal (task success, time-on-task, SUS) when available.
3. **Diagnose** where the built UX failed the JTBD (the FMECA failure classes:
   job-miss, trust-failure, honest-state, decision-readiness, cut-list).
4. **Refine** the responsible skill(s) or the flow; commit the delta.
5. Repeat. "Better than any other approach" is **corroborated by surviving
   repeated grounded evaluation**, never declared. Track the flip/defect rate
   across iterations as the anti-theatre measure.

## Status
- **v1 composed** (all skills + caps wired). YAML valid.
- **Pending live load-test** (gateway configured with base CA + cognitive-max;
  cross-namespace references; the design caps actually consuming the injected
  skills). Same caveat as `flow.add-ui-feature`.
- **Next:** P3 wires `intentos` (`connections/intentos.yaml`) + `elicitation`
  into a `grounding_jtbd` front-stage so the workflow pulls the researched job
  in automatically rather than via the brief; then run iteration 1 on SP3.
