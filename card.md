# ants-starter

A nano-class Ants policy.

| | |
|---|---|
| Weight class | **nano** — 6,006 of 8,192 bytes (73% of the cap) |
| Parameters | 2,930 (fp16 initializers) |
| Architecture | `Trunk`, receptive field **15 cells** each way (dilations [1, 2, 4, 8]) |
| Method | behaviour cloning, 5 epochs over 250,000 seat-turns, 85.8% held-out agreement, seed 1 |
| Adapter | 245,839 of 1,000,000 operations at its worst reference case |
| Inference | 2.90 ms at the worst reference case — **9%** of a 31.2 ms seat share |
| Operators | Cast, Concat, Constant, Conv, Relu, Slice |
| Engine | `sha256:9ba5d31e171b53ecdc4768941cf9baf8cefe4b4a70b726d7ae8d796c419803d7` |
| Evaluator | `sha256:44cfc91cb1f20f9a4b46d742169c22f970a96801faa843416f4d6776c9b3c505` |
| Model hash | `sha256:17f9dfb7cd6bb1a4746cd5960a05765916bc775f5a37c9900ded0daac0a12f3a` |
| Adapter hash | `sha256:9c022ff50c7210213afa4a88ffb56cd2dee188f99b949335a037bdc60ab2d468` |



Reproduce with `see README.md`.

Inference time is measured on whatever machine ran the check and is **reported, never a gate**:
there is no compute cap (devops decision 46). It is here because the turn deadline is what a graph
too expensive to play runs into, and a seat's share of it is `turn_ms / rows in the call`.
