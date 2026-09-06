# God-file refactor acceptance and continuation

The refactor is successful only after the real Cargo verifier reports a passing
build. Human acknowledgement of an unresolved build terminates with a failure
outcome; it cannot silently convert the result to verified success.

A failed check without usable diagnostics routes to human investigation. The
paired cognitive-architectures change adds `diagnostics_available` to
`verify.cargo.cwd`; merge/deploy that contract before this workflow change.

The `fixing` state opts into Praxec `continuation.reads` over `build_issues`.
An identical diagnostic set on the next auto-driven repair is quarantined before
another model call, even if the retry counter changed. This deliberately favors
stopping over speculative retries; a changed source file with identical errors
can also stop. The existing retry cap remains in place. A future artifact-digest
slice can permit useful partial progress once the verifier supplies that evidence.

This control requires the Praxec commodity-model-harness change; the old v0.0.48
CI engine may load unknown state metadata without enforcing it. Do not treat an
old-engine config check as proof that continuation is active. Update the CI engine
pin to the released version containing that change before promoting this PR.
Until then this PR is a dependency-gated draft. Other workflow controls use the
existing runtime and remain independently checkable.
