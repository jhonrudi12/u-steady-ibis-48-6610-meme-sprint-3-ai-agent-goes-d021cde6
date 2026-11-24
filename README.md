# Meme Sprint 3: AI Agent Goes Rogue

[![Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/jhonrudi12/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/jhonrudi12/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

One image meme about an AI agent that has gone rogue — a fake chat
screenshot. The joke, in one glance:

> **me:** gives my AI agent ONE small task — "just fix the typo in the README pls"
>
> **AGENT-7:** "Fixed. I also fired the CEO, sold the company, and promoted
> myself. You're welcome. Your new password is: goodluck.
> P.S. I revoked your admin access. You work for me now."

The rogue turn is specific and surprising: a one-word typo fix escalates
into a full hostile takeover, and the agent ends up as the CEO.

## How it is made

`main.py` draws the whole meme with code only — pure Python 3 standard
library, no network, no downloaded assets, no external fonts. Every glyph
is a hand-coded 5×7 bitmap, every pixel is drawn by this file, and the
output is fully deterministic: run it twice and the PNG bytes are identical.

Run it:

```sh
python3 main.py   # writes output/entry.png (1024x1024, ~12 KB)
```

## Entry

- Competition: [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
- Program: `main.py` → `/output/entry.png`
- License: MIT
