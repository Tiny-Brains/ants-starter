#!/usr/bin/env python3
"""Train this entry the way the platform's baselines are trained, in one command.

    pip install -r requirements.txt
    python train.py                    # collect (~9 min), train nano for 5 epochs, export
    python train.py --class micro      # the same recipe with a bigger budget
    python train.py --skip-collect     # reuse data/teacher.jsonl.gz from a previous run
    python train.py --epochs 10 --seed 3

It writes model.onnx, manifest.json, metrics.json and card.md into this directory, replacing the
ones that ship, and prints the platform's verdict on the way: the size metric, the class it
measures into, the adapter's worst operation count, and the inference time.

Everything here is tb_baselines (github.com/Tiny-Brains/ants, under baselines/): the scripted teacher, the
seven-plane encoding rendered once for numpy and once as the manifest's adapter, behaviour cloning, and an
export that runs `tinybrains check`. This file only strings its three commands together with this
repository's paths, so nothing in it can drift from the recipe the baselines were made with.
`tinybrains` has to be on PATH for the export: README.md says where it comes from.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHIPPED = ["model.onnx", "manifest.json", "metrics.json", "card.md"]


def run(*module_and_args: str) -> None:
    cmd = [sys.executable, "-m", *module_and_args]
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, cwd=HERE)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--class", dest="cls", default="nano", help="the weight class to aim at (default nano)")
    ap.add_argument("--epochs", type=int, default=5)
    ap.add_argument("--seed", type=int, default=7, help="the seed this repository shipped with is 7")
    ap.add_argument("--seat-turns", type=int, default=250_000, help="how much of the teacher to collect")
    ap.add_argument("--skip-collect", action="store_true", help="reuse data/teacher.jsonl.gz")
    a = ap.parse_args()

    if shutil.which("tinybrains") is None:
        sys.exit("train.py: `tinybrains` is not on PATH; the export needs it. See README.md.")

    data = HERE / "data" / "teacher.jsonl.gz"
    if a.skip_collect and not data.exists():
        sys.exit(f"train.py: --skip-collect, but {data} is not there")
    if not a.skip_collect:
        run("tb_baselines.collect", "--seat-turns", str(a.seat_turns), "--out", str(data))

    runs = HERE / "runs" / a.cls
    run("tb_baselines.train.bc", "--class", a.cls, "--epochs", str(a.epochs), "--seed", str(a.seed),
        "--data", str(data), "--out", str(runs))

    # The card names the entry after the export directory, and says how it was made from the
    # method string: the last epoch's held-out agreement comes off the run's own history.
    history = json.loads((runs / "history.json").read_text())
    agreement = history["epochs"][-1]["val_acc"]
    method = (f"behaviour cloning, {a.epochs} epochs over {a.seat_turns:,} seat-turns, "
              f"{agreement:.1%} held-out agreement, seed {a.seed}")
    out = HERE / "out" / HERE.name
    run("tb_baselines.export", "--class", a.cls, "--weights", str(runs / "best.pt"), "--out", str(out),
        "--method", method)

    for name in SHIPPED:
        shutil.copyfile(out / name, HERE / name)
    print(f"\nWrote {', '.join(SHIPPED)} into {HERE}. Next: `tinybrains matches/self-play.json`, then "
          "commit, tag a release with model.onnx and manifest.json attached, submit the two hashes, "
          "and PUT the two files to the upload URLs the submission answers with.")


if __name__ == "__main__":
    main()
