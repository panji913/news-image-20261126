// Entrypoint for "The World in One Day" (news-image-20261126).
//
// Node 22, standard library only. It hands the drawing to draw.py, the
// Python program beside this file, and then checks the picture it made.
// The grader runs this file twice; draw.py takes no clock and no network,
// so both runs write the same bytes to /output/entry.png.

import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const painter = join(here, "draw.py");
const target = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });

const run = spawnSync("python3", [painter, outDir], {
  cwd: here,
  encoding: "utf8",
  env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
});

if (run.stdout) process.stdout.write(run.stdout);
if (run.stderr) process.stderr.write(run.stderr);
if (run.error) throw run.error;
if (run.status !== 0) {
  throw new Error(`draw.py exited with status ${run.status}`);
}
if (!existsSync(target)) {
  throw new Error(`draw.py finished but ${target} is missing`);
}

const bytes = statSync(target).size;
if (bytes === 0 || bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, outside the 1 MiB limit`);
}
console.log(`entry ready: ${target} (${bytes} bytes)`);
