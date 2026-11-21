// news-image-20261121 entry (Node 22, standard library only): the image
// is entry.png beside this file, and the program copies it to
// /output/entry.png, then verifies the copy byte for byte by length and
// sha256, so both grading runs write identical bytes. The gate takes a
// whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(source, dest);

const original = readFileSync(source);
const copied = readFileSync(dest);
if (original.length !== copied.length) {
  throw new Error(`length mismatch: ${original.length} vs ${copied.length}`);
}
const digest = (buf) => createHash('sha256').update(buf).digest('hex');
if (digest(original) !== digest(copied)) {
  throw new Error('sha256 mismatch after copy');
}
console.log(`wrote ${dest} (${copied.length} bytes, sha256 ${digest(copied)})`);
