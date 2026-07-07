# APEX + AI LiveLabs Workshop — Task Tracker

Plan: `/home/rickh/.claude/plans/vast-herding-volcano.md` (approved 2026-07-07)

## Phase 1 — Research
- [x] Explore LiveLabs authoring conventions (Rick's developer fork, sample-workshop)
- [x] Deep research: APEX platform + AI capabilities (26.1, sandbox constraints)
- [x] Deep research: APEX developer persona
- [x] Deep research: LiveLabs landscape, gap analysis, sandbox mechanics, publishing process
- [x] Clone oracle-livelabs/apex to ~/GitHub/apex
- [x] Persist research reports to docs/research/

## Phase 2 — Spec
- [x] Write workshop spec to docs/specs/2026-07-07-apex-ai-workshop-spec.md
- [x] Adversarial multi-agent spec review (persona fit / technical accuracy / LiveLabs compliance / timing realism + completeness critic)
- [x] Fix review findings inline
- [x] Commit spec + research on branch apex-ai-workshop-spec

## Phase 3 — Review gate
- [ ] Rick reviews spec (BLOCKING — no lab authoring until approved)

## Phase 4 — Development (future task; inline, strict TDD)
- [ ] Build validation harness first (tests red), then author labs to green
- [ ] Per-lab: manifest entry + validator expectations → lab content → green
- [ ] SQL artifacts tested against real 26ai ADB (idempotent)
- [ ] Repo lint (lintchecker/md-validator) passes
- [ ] Self QA click-through on real sandbox reservation, timed ≤ 90 min
- [ ] WMS submission / PR with WMS ID (Rick, Oracle-internal)
