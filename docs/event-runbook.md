# Large-Event Delivery Runbook — AI Help Desk Workshop

For instructor-led deliveries of `ai-helpdesk-agent`, especially **Track B events (hundreds of seats)** per spec §5. Green button handles ≤30 concurrent; everything bigger runs through this checklist. Copy the table into the event doc and fill the Owner/Date columns per event.

## T-minus 3 weeks — capacity and environment

| # | Item | Owner | Notes |
|---|---|---|---|
| 1 | Confirm seat count and delivery track | Rick | ≤30 → green button, stop here; >30 → continue |
| 2 | Secure the event tenancy | Event team | Bootcamp pattern (`tenancy-special`): either N attendee compartments where each creates an Always Free ADB, or pre-provisioned shared ADB instances with per-attendee APEX workspaces |
| 3 | Check event-tenancy service limits | Event team | ADB instance count ≥ N (or shared-instance sizing: ~50 workspaces per 2-OCPU instance is comfortable for this workload) |
| 4 | Pre-negotiate OCI GenAI throughput | Rick | On-demand inference is dynamically throttled per tenancy; hundreds of concurrent users WILL hit 429s without raised limits. Options: limit raise for the event tenancy, or shard attendees across 2-3 compartments/regions (Chicago + Ashburn + Frankfurt all carry chat models) |
| 5 | Request the Event Code in WMS | Rick | ≥1 week before the event (2-day review + 1-day creation). Point it at `workshops/event/`; set active window from 1 day before to 1 day after |

## T-minus 1 week — content and fallback

| # | Item | Owner | Notes |
|---|---|---|---|
| 6 | Week-of validation | Rick | `python3 tools/validate_workshop.py --online --final`; verify current chat models exist in the target region(s); re-run Lab 7's ONNX download link |
| 7 | Issue the OpenAI relief-valve key | Rick | One per-event key, hard spend cap (e.g. $100), distributed on-screen or via the Event Code page — never in lab content or chat logs |
| 8 | Re-cut `workshops/event/manifest.json` if needed | Rick | e.g. drop optional labs for a 60-min slot; validator must stay green |
| 9 | Dry-run the full workshop on the event tenancy | Rick / co-instructor | Timed; confirms GenAI limits, model IDs, and the Lab 7 grants work under the event tenancy's policies |

## Day of event

| # | Item | Owner | Notes |
|---|---|---|---|
| 10 | Attendees start reservations/logins at t-0 | Instructor | ADB provisioning wait is absorbed by the instructor demo of the finished app (plants the wow before minute 10) |
| 11 | 429 protocol | Instructor | Announce once: "rate-limit error = wait 30 seconds and retry"; if sustained, switch affected rows of the room to the OpenAI track (Lab 1 page selector) |
| 12 | Minute-60 checkpoint | Instructor | Room behind? Drive Lab 5 Tasks 5-6 from the podium (attendees follow); never cut the confirmation-dialog payoff or Take It Home |
| 13 | Minute-80 call | Instructor | Point fast finishers at Labs 6-7; remind everyone to export (Take It Home) before leaving |

## Post-event

| # | Item | Owner | Notes |
|---|---|---|---|
| 14 | Revoke the OpenAI event key | Rick | Same day |
| 15 | Tear down event-tenancy resources | Event team | Pre-provisioned ADBs, compartments, IAM artifacts |
| 16 | Log attendance + issues | Rick | Feed real timings back into lab Estimated Time headers; file validator rules for anything QA-able |
