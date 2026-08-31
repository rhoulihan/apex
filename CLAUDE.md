# Project directives — APEX AI Help Desk workshop

## End-to-end validation runs: do not stop between labs

When validating the workshop end to end — walking the labs against a live environment, capturing
screenshots, or re-running after a teardown — **keep going until every remaining lab is done.** Do not
stop and wait to be prompted between labs or between tasks.

Move straight to the next lab when you finish one. Report progress as you go rather than pausing for
permission to continue.

**The only reasons to stop are things a human must actually do:**

- A password, private key, or other credential must be entered.
- A file must be chosen in a native file picker the extension cannot reach (for example the APEX
  *Upload Script* dialog, which renders inside a modal iframe).
- An irreversible or outward-facing action needs approval that has not already been given — deleting
  something in the live tenancy, opening a pull request, sending anything.
- A decision genuinely changes the work and cannot be resolved from the labs, the repo, or a sensible
  default.
- The environment is broken in a way that blocks progress (session dead, service returning errors after
  a couple of retries).

When you do stop, say precisely what you need and what is already done, so the human can unblock it in
one step.

## Fix defects, do not just record them

Every behaviour that contradicts the lab text gets **fixed in the lab** in the same pass that found it,
not filed for later. Recording alone is not done. Where a fix is testable, test it — prefer an A/B
against the live environment over an assumption, and revert changes that fail the test rather than
shipping them hopefully.

## Verify before claiming

Check the DOM, the database, or the rendered page rather than judging from a screenshot. Several
corrections in this project came from a control that *looked* enabled, or a script that *looked* current
but was a stale upload. Byte counts, `disabled` flags and row counts settle these; pixels do not.
