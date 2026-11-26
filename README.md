# The World in One Day — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/panji913/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/panji913/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One 1024×1024 poster for Thursday 26 November 2026: six stories from the day, each checked against the source named on its card.

## Stories

1. **Bitcoin** — BTC at $60,340.36, up 1.05% in 24 hours; Fear & Greed index at 10/100, extreme fear. Anndy Lian newsletter, 26 Nov.
2. **North Korea** — Kim Jong Un urges wider deployment of tactical nuclear weapons across multiple domains. KCNA via Reuters, 26 Nov.
3. **South Korea** — The Bank of Korea raises its base rate to 3.25% and lifts its 2027 growth outlook to 4.1%. Reuters, 26 Nov.
4. **Markets** — Asian stocks rebound on Thursday as the new US tariffs look milder than feared; Kospi up 2.3%. Dow Jones Newswires / AFP, 26 Nov.
5. **Hong Kong** — Mourners lay flowers at Wang Fuk Court on the first anniversary of the fire that killed 168; no official memorial. AFP, 26 Nov.
6. **Indonesia** — 13 miners found dead on Thursday in a flooded illegal gold mine near Bogor, West Java; 13 still missing. Reuters / Xinhua, 26 Nov.

All six happened — or were first reported — on 26 November 2026. Nothing from another date is on the poster. Stories that broke on 25 November (the Trump tariff proposals, the FCC's Starmind approval, the Netanyahu judges' recommendation, the Cartagena rescue, the Nigeria meth bust, the Lukoil deal, the Shenzhou-24 docking, the Macy's parade postponement) were checked and left out.

## How it is built

`draw.py` paints `entry.png` with Pillow only: no network, no clock, no randomness, so two runs write byte-identical files — 122,120 bytes, 1024×1024, sha256 `0819bb75deb1790a9d5b57cfe22da3ca1c20bf8eb7269f4dcc1d33221c41052e`. `main.ts` reads that verified file and writes its exact bytes to `MAKEFUN_OUTPUT_DIR` (default `/output`); it refuses to run when `entry.png` is missing or over the 1 MiB cap.

```sh
python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Files

- `draw.py` — paints `entry.png`.
- `entry.png` — the poster as verified in-session.
- `main.ts` — emits `entry.png` to the grader's output path.
- `out/` — local render output.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7q825rck&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
