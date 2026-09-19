# ants-starter

A nano-class Ants policy.

| | |
|---|---|
| Weight class | **nano** — 12,280 of 16,384 bytes (75% of the cap) |
| Parameters | 3,006 (fp16 initializers) |
| Architecture | `Trunk`, receptive field **15 cells** each way (dilations [1, 2, 4, 8]) |
| Method | behaviour cloning, 5 epochs over 250,000 seat-turns, 85.8% held-out agreement, seed 1 |
| Adapter | 229,415 of 1,000,000 operations at its worst reference case |
| Inference | 8.08 ms at the worst reference case — **0.8%** of the 1000 ms a seat gets |
| Operators | Cast, Concat, Constant, Conv, Relu, Slice |
| Engine | `sha256:eead45ca770f5626d1787066bc00522687989101d4bf29ab3ec6ecb712755535` |
| Model hash | `sha256:17f9dfb7cd6bb1a4746cd5960a05765916bc775f5a37c9900ded0daac0a12f3a` |
| Manifest hash | `sha256:58425bd6ee6a0cc7bd529c04eb36d62a09ff7e29f5ad38b3f06cb300f94c1db4` |



Reproduce with `see README.md`.

Inference time is measured on whatever machine ran the check and is **reported, never a gate**:
there is no compute cap. It is here because the turn deadline is what a graph too expensive to
play runs into, and a seat's share of it is the WHOLE turn -- one `model_infer` call per seat,
each with its own deadline.
