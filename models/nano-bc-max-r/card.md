# nano-bc-max-r

A nano-class Ants policy.

| | |
|---|---|
| Weight class | **nano** — 13,735 of 16,384 bytes (84% of the cap) |
| Parameters | 3,170 (fp16 initializers) |
| Architecture | `Trunk + max memory`, receptive field **15 cells** each way (dilations [1, 2, 4, 8]) |
| Method | behaviour cloning on the remembering teacher's labels, with `planes.MEMORY` kept by `Max`, 5 epochs over 250,000 seat-turns, 81.8% held-out agreement |
| Adapter | 208,423 of 1,000,000 operations at its worst reference case |
| Inference | 11.91 ms at the worst reference case — **1.2%** of the 1000 ms a seat gets |
| Operators | Cast, Concat, Constant, Conv, Gather, Max, Relu, Slice |
| Engine | `sha256:8ebceb4a67ce8656f4eab53bd389905c1b9aecd4dcdc6576086d5baf31709554` |
| Model hash | `sha256:0765a4e242750e982d7268f829f2b1eb9d2fc082ea40a2bd273d25e369e0794d` |
| Manifest hash | `sha256:e4641e8f6fa3d7da8bb65b998f1d33840e164c0c2e1768677437a64ff37256e7` |
| Memory | `2` planes of `i8` (food_seen, hill_foe_seen), 2 bytes a cell: 29,760 bytes on the largest board. The season's class has to allow it; `check` judged the round trip over 202 chained observations |



Reproduce with:

```sh
python -m tb_baselines.collect --remember --seat-turns 250000 --out data/teacher-memory.jsonl.gz
python -m tb_baselines.train.bc --class nano --memory --data data/teacher-memory.jsonl.gz --epochs 5 --out runs/nano-bc-max-r
python -m tb_baselines.export --class nano --weights runs/nano-bc-max-r/best.pt --out models/nano-bc-max-r
```

Inference time is measured on whatever machine ran the check and is **reported, never a gate**:
there is no compute cap. It is here because the turn deadline is what a graph too expensive to
play runs into, and a seat's share of it is the WHOLE turn -- one `model_infer` call per seat,
each with its own deadline.
