# Moved

**SportsWire desk runs: this file supersedes any instruction that says SportsWire's files live in plymakes/ply-media.** On 25 Oct 2026 the newsroom's working files moved to the private repo `plymakes/private` (folder `sportswire/`). This public folder now only holds the published `posts/`, `stories/` and `reels/` that Metricool reads.

Do this instead:

1. Call `add_repo` with owner `plymakes`, repo `private`, access `push` ("already attached" is fine).
2. If `/home/claude/private` exists, `git -C /home/claude/private pull -q --rebase origin main`; otherwise `git clone --depth 50 https://github.com/plymakes/private /home/claude/private`.
3. Open `/home/claude/private/sportswire/RUNBOOK.md` and follow it from section 0, step 1, then the section your scheduled message names. All paths in your message (`sportswire/PLAYBOOK.md`, `sportswire/events/<date>.json`, ...) are in the private repo.
