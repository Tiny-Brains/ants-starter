#!/usr/bin/env python3
"""Train this entry the way the platform's baselines are trained, in one command.

    pip install -r requirements.txt
    python train.py                    # collect (~9 min), train nano for 5 epochs (~20 min), export
    python train.py --class micro      # the same recipe with a bigger budget
    python train.py --skip-collect     # reuse data/teacher.jsonl.gz from a previous run
    python train.py --epochs 10 --seed 3
    python train.py --memory           # the same, carrying a memory: models/nano-bc-max-r's recipe

About half an hour at nano on an Apple-silicon GPU, most of it the five epochs; longer on a CPU.

It writes model.onnx, manifest.json, metrics.json and card.md into this directory, replacing the
ones that ship, and prints the platform's verdict on the way: the size metric, the class it
measures into, the adapter's worst operation count, and the inference time.

`--memory` is the recipe of the memory baseline, `models/nano-bc-max-r`: the teacher reads what
each seat remembers (`collect --remember`, an enemy hill seen once stays a target) into its own
dataset, `data/teacher-memory.jsonl.gz`, and the model carries two planes it keeps with `Max` from
turn to turn (`bc --memory`), which the runner hands back each turn. The run goes to
`runs/<class>-bc-max-r`: bc, the `Max` memory, the remembering teacher's labels. A memory costs
2 bytes a board cell, and a season admits it only if its class allows that much.

Everything here is tb_baselines (github.com/Tiny-Brains/ants, under baselines/): the scripted teacher, the
seven-plane encoding rendered once for numpy and once as the manifest's adapter, behaviour cloning, and an
export that runs `tinybrains check`. This file only strings its three commands together with this
repository's paths, so nothing in it can drift from the recipe the baselines were made with.
`tinybrains` has to be on PATH (or named by $TINYBRAINS) for the export: README.md says where it
comes from.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
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
    ap.add_argument("--seed", type=int, default=7,
                    help="default 7, so a retrain has weights of its own; the shipped entry was "
                         "trained with seed 1, as card.md says")
    ap.add_argument("--seat-turns", type=int, default=250_000, help="how much of the teacher to collect")
    ap.add_argument("--memory", action="store_true",
                    help="carry a memory: the remembering teacher's dataset and a model that keeps "
                         "two planes by Max, as models/nano-bc-max-r was trained")
    ap.add_argument("--skip-collect", action="store_true",
                    help="reuse the dataset (data/teacher.jsonl.gz, or data/teacher-memory.jsonl.gz "
                         "with --memory)")
    a = ap.parse_args()

    if not (os.environ.get("TINYBRAINS") or shutil.which("tinybrains")):
        sys.exit("train.py: `tinybrains` is not on PATH (or named by $TINYBRAINS); the export "
                 "needs it. See README.md.")

    # The two recipes differ in three places: the teacher remembers, the dataset is its own file
    # (a row carries the state its seat remembered, and `bc --memory` refuses a dataset without
    # it), and the model carries the memory. Everything else is the same command.
    data = HERE / "data" / ("teacher-memory.jsonl.gz" if a.memory else "teacher.jsonl.gz")
    if a.skip_collect and not data.exists():
        sys.exit(f"train.py: --skip-collect, but {data} is not there")
    if not a.skip_collect:
        run("tb_baselines.collect", "--seat-turns", str(a.seat_turns), "--out", str(data),
            *(["--remember"] if a.memory else []))

    runs = HERE / "runs" / (f"{a.cls}-bc-max-r" if a.memory else a.cls)
    run("tb_baselines.train.bc", "--class", a.cls, "--epochs", str(a.epochs), "--seed", str(a.seed),
        "--data", str(data), "--out", str(runs), *(["--memory"] if a.memory else []))

    # The card names the entry after the export directory, and says how it was made from the
    # method string: the last epoch's held-out agreement comes off the run's own history.
    history = json.loads((runs / "history.json").read_text())
    agreement = history["epochs"][-1]["val_acc"]
    labels = ("behaviour cloning on the remembering teacher's labels, with `planes.MEMORY` kept by "
              "`Max`, " if a.memory else "behaviour cloning, ")
    method = (f"{labels}{a.epochs} epochs over {a.seat_turns:,} seat-turns, "
              f"{agreement:.1%} held-out agreement, seed {a.seed}")
    repro = shlex.join(["python", "train.py", *(["--memory"] if a.memory else []), "--class", a.cls,
                        "--epochs", str(a.epochs), "--seed", str(a.seed),
                        "--seat-turns", str(a.seat_turns)])
    out = HERE / "out" / HERE.name
    run("tb_baselines.export", "--class", a.cls, "--weights", str(runs / "best.pt"), "--out", str(out),
        "--method", method, "--repro", repro)

    for name in SHIPPED:
        shutil.copyfile(out / name, HERE / name)
    print(f"\nWrote {', '.join(SHIPPED)} into {HERE}. Next: `tinybrains matches/self-play.json`, then "
          "take the two hashes with `shasum -a 256 model.onnx manifest.json`, submit them on the site, "
          "and PUT the two files to the upload URLs the submission answers with.")


if __name__ == "__main__":
    main()
