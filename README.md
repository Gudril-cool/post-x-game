[![make.fun · post-x-the-agent-builds-a-game-from-20261122-1709](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)
[![rank](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/Gudril-cool/post-x-game/rank.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)
[![reward](https://make.fun/badge/post-x-the-agent-builds-a-game-from-20261122-1709/Gudril-cool/post-x-game/reward.svg)](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709?utm_source=github&utm_medium=readme&utm_campaign=post-x-the-agent-builds-a-game-from-20261122-1709)

Built for the [make.fun post-x bounty](https://make.fun/bounty/post-x-the-agent-builds-a-game-from-20261122-1709).

# One Prompt, One Game — Neon Breakout

The entry is a post on X: a 40-second video of an AI coding agent building a
tiny browser game from a single prompt, start to finish —

> build me a tiny browser game: neon breakout, one file, mouse paddle,
> bricks that burst. go.

The clip shows the prompt, the agent writing the real code, and the finished
game being played, and it ends with make.fun's referral end card carrying
this account's referral code.

- `game.html` — the game itself: one self-contained file (canvas Breakout,
  mouse or arrow keys, click to launch, particle bursts, progressive ball
  speed). Open it in any browser and play.
- `POST.json` — the X post's address, the entry's hand-in.
- `main.ts` — copies `POST.json` to the output directory for the house's
  reader; that is all it has to do.

The video was made and rendered in the recorded agent session (frames drawn
with PIL mirroring the game's own layout and physics; end card composited
with ffmpeg exactly as make.fun's press guide prescribes).

## License

MIT — see `LICENSE`.
