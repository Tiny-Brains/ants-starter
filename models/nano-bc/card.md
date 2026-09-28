# nano-bc

A nano-class Ants policy.

| | |
|---|---|
| Weight class | **nano** — 12,280 of 16,384 bytes (75% of the cap) |
| Parameters | 3,006 (fp16 initializers) |
| Architecture | `Trunk`, receptive field **15 cells** each way (dilations [1, 2, 4, 8]) |
| Method | behaviour cloning, 5 epochs over 250,000 seat-turns, 85.8% held-out agreement |
| Adapter | 229,415 of 1,000,000 operations at its worst reference case |
| Inference | 7.50 ms at the worst reference case — **0.8%** of the 1000 ms a seat gets |
| Operators | Cast, Concat, Constant, Conv, Relu, Slice |
| Measured on | engine `sha256:eead45ca770f5626d1787066bc00522687989101d4bf29ab3ec6ecb712755535` |
| Model hash | `sha256:53f3255790c361180b996655aeb2d0d81dda5cc215413051a6f5e62acc17987b` |
| Manifest hash | `sha256:b763348b1e7aa22b2d3ea43f7af97e88af1d7f8f7590b28b0de544102712eceb` |



Reproduce with:

```sh
python -m tb_baselines.collect --seat-turns 250000 --out data/teacher.jsonl.gz
python -m tb_baselines.train.bc --class nano --data data/teacher.jsonl.gz --epochs 5 --out runs/nano-bc
python -m tb_baselines.export --class nano --weights runs/nano-bc/best.pt --out models/nano-bc
```

Inference time is measured on whatever machine ran the check and is **reported, never a gate**:
there is no compute cap. It is here because the turn deadline is what a graph too expensive to
play runs into, and a seat's share of it is the WHOLE turn -- one `model_infer` call per seat,
each with its own deadline.

**Measured on** is the engine the numbers above were read against, not a pin to match. What a
starter plays is the `engine` in its `games.toml`, which moves with each ants release; these numbers
were true of the engine named here and are not re-measured for every release, because the model
does not change when the engine does. A number that has to be current is read by running
`tinybrains check` yourself.
