# micro-percell

A micro-class Ants policy.

| | |
|---|---|
| Weight class | **micro** — 52,732 of 131,072 bytes (40% of the cap) |
| Parameters | 24,993 (fp16 initializers) |
| Architecture | `PerCell`, receptive field **0 cells** each way |
| Method | behaviour cloning, same data as micro-bc; the reach-0 control, 40.7% held-out agreement |
| Adapter | 229,415 of 1,000,000 operations at its worst reference case |
| Inference | 5.71 ms at the worst reference case — **0.6%** of the 1000 ms a seat gets |
| Operators | Cast, Conv, Relu |
| Measured on | engine `sha256:eead45ca770f5626d1787066bc00522687989101d4bf29ab3ec6ecb712755535` |
| Model hash | `sha256:85713895274b6d1040ab14205c6f9e00eaf3657c6ed61c10444d6acabfcae193` |
| Manifest hash | `sha256:e05d1bcd4af176911b83558fac6c89584cc1bf09f4d277850ef661fc780a51c3` |



Reproduce with:

```sh
python -m tb_baselines.collect --seat-turns 250000 --out data/teacher.jsonl.gz
python -m tb_baselines.train.bc --class micro --arch percell --channels 108 --blocks 2 --data data/teacher.jsonl.gz --epochs 5 --out runs/micro-percell
python -m tb_baselines.export --class micro --arch percell --channels 108 --blocks 2 --weights runs/micro-percell/best.pt --out models/micro-percell
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
