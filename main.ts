// news-image-20261126 — poster for Thursday 26 November 2026.
// Entry for @panji913. The poster is entry.png, painted in-session
// by draw.py with Pillow: six stories from the 26 November 2026
// news cycle — Bitcoin at $60,340 with extreme fear, Kim Jong Un's
// tactical nuclear push, the Bank of Korea's hike to 3.25%, the
// Asian stock rebound, Hong Kong's year since the Wang Fuk Court
// fire, and the 13 miners found dead in a flooded Bogor mine.
//
// main.ts does one job: it reads the verified entry.png beside it
// and writes those exact bytes to the grader's output folder. The
// entrypoint draws nothing at grade time, so the graded image is
// byte-for-byte the image that was checked in-session (see the
// render log for the sha256).
//
// Why read-and-write instead of a copy call: the guardrails below
// are the point. The script bails out when entry.png is missing
// rather than emitting an empty file, bails out when the file is
// over the competition's 1 MiB cap, makes the output folder itself,
// and touches nothing else — no network, no clock, no environment
// besides MAKEFUN_OUTPUT_DIR — so every run emits identical bytes.
//
// Run locally:  python3 draw.py && mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import * as fs from 'node:fs';
import * as path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

if (!fs.existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (${here})`);
}
const bytes = fs.readFileSync(src);
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
}

fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'entry.png'), bytes);
console.log(`wrote entry.png (${bytes.length} bytes) to ${outDir}`);
