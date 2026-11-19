#!/usr/bin/env python3
"""
Replace one character at a fixed column, only within a line range, for every
file in a folder. Defaults match your case: chain A -> L on lines 7596-11076.

Usage:
  python3 replace_chain.py INPUT_DIR [-o OUTPUT_DIR] [--old A] [--new L]
                           [--start 7596] [--end 11076] [--col 22] [--ext .pdb]

--col is 1-based (PDB chain ID is column 22). Originals are never touched;
results go to OUTPUT_DIR (default: INPUT_DIR/modified).
"""
import argparse
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("input_dir")
p.add_argument("-o", "--output_dir")
p.add_argument("--old", default="A")
p.add_argument("--new", default="L")
p.add_argument("--start", type=int, default=7596)   # 1-based, inclusive
p.add_argument("--end", type=int, default=11076)    # 1-based, inclusive
p.add_argument("--col", type=int, default=22)       # 1-based column
p.add_argument("--ext", default=".pdb")
a = p.parse_args()

assert len(a.old) == 1 and len(a.new) == 1, "--old/--new must be single characters"
src = Path(a.input_dir)
out = Path(a.output_dir) if a.output_dir else src / "modified"
out.mkdir(parents=True, exist_ok=True)
i = a.col - 1

for f in sorted(src.glob(f"*{a.ext}")):
    changed = 0
    with open(f) as fin, open(out / f.name, "w", newline="") as fout:
        for n, line in enumerate(fin, 1):
            if a.start <= n <= a.end and len(line) > i and line[i] == a.old:
                line = line[:i] + a.new + line[i + 1:]
                changed += 1
            fout.write(line)
    print(f"{f.name}: {changed} lines changed")
