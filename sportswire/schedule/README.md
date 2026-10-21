# How the SportsWire schedule works

Fresh cloud sessions started by a recurring scheduled task can't reach GitHub (no `add_repo`, git denied; checked 21 Oct 2026), so the desks don't run there. They run inside Geoffry's SportsWire session, which has `plymakes/ply-media` attached with push access, Metricool, web search and the render tools.

Each desk run is a **one-off message into that session**, created with `send_later`. Those can't repeat on their own, so every run tops the schedule up (RUNBOOK section 0, step 7): it keeps the next **48 hours** of desks queued, plus the next Sunday weekly desk.

| Desk | Time (Beirut/Cyprus) | Name of the scheduled task | Message |
|---|---|---|---|
| Morning | 08:51 daily | `SportsWire morning desk · <Ddd DD Mon>` | `morning.txt` |
| Afternoon | 15:50 daily | `SportsWire afternoon desk · <Ddd DD Mon>` | `afternoon.txt` |
| Evening | 22:15 daily | `SportsWire evening desk · <Ddd DD Mon>` | `evening.txt` |
| Weekly | Sunday 11:52 | `SportsWire weekly desk · <Ddd DD Mon>` | `weekly.txt` |
| Result | expected end + 35 min | `SportsWire result · <date> <event>` | `result.txt` with DATE, EVENT_ID, ATTEMPT filled in |

`send_later` takes UTC: Cyprus/Lebanon are UTC+3 until 25 Oct 2026 (Cyprus) and UTC+2 after the clocks change; Lebanon follows the same change. Always convert with the `Asia/Nicosia` timezone, never by hand.

Pass the file's text **verbatim** as the message. Never use `create_trigger` for SportsWire work.
