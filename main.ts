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
// Gate check: the entry must be a PNG of at most 1 MiB and 1024x1024.
// The PNG signature is 8 bytes, then the IHDR chunk holds width and
// height as big-endian uint32 at offsets 16 and 20.
if (original.length > 1048576) {
  throw new Error(`entry.png is ${original.length} bytes, over the 1 MiB cap`);
}
if (original.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a'
    || original.toString('ascii', 12, 16) !== 'IHDR') {
  throw new Error('entry.png is not a PNG file');
}
const width = original.readUInt32BE(16);
const height = original.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}
if (original.length !== copied.length) {
  throw new Error(`length mismatch: ${original.length} vs ${copied.length}`);
}
const digest = (buf) => createHash('sha256').update(buf).digest('hex');
if (digest(original) !== digest(copied)) {
  throw new Error('sha256 mismatch after copy');
}
console.log(`wrote ${dest} (${copied.length} bytes, sha256 ${digest(copied)})`);
