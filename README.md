# The World in One Day

A poster that sums up the world's news of **Thursday 26 November 2026** in
one 1024 × 1024 picture, made for the make.fun competition
`news-image-20261126`. Six stories, each checked against what was first
reported that day:

1. **Bitcoin** — BTC $60,340.36, up 1.05%; Fear & Greed 10/100, extreme fear.
2. **North Korea** — Kim Jong Un urges a wider spread of tactical nuclear weapons.
3. **South Korea** — Bank of Korea raises its rate to 3.25% and lifts the 2027 growth forecast to 4.1%.
4. **Asia markets** — Stocks rebound as new US tariffs look lighter than feared; Kospi +2.3%.
5. **Hong Kong** — Mourners lay flowers at Wang Fuk Court, one year after the fire that killed 168; no official memorial.
6. **Indonesia** — 13 miners found dead in a flooded illegal gold mine near Bogor; 13 still missing.

## How it runs

`main.ts` (Node 22, standard library only) calls `draw.py`, which draws the
poster with Pillow and the DejaVu fonts and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The drawing takes no
network and no clock, so repeated runs are byte-identical.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Requirements: Python 3 with Pillow, and DejaVu fonts (present on most Linux
systems; the program falls back to Pillow's built-in font if they are absent).

## License

MIT — see `LICENSE`.
