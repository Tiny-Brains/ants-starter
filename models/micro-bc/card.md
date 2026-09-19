# micro-bc

A micro-class Ants policy.

| | |
|---|---|
| Weight class | **micro** — 54,426 of 131,072 bytes (42% of the cap) |
| Parameters | 24,077 (fp16 initializers) |
| Architecture | `Trunk`, receptive field **15 cells** each way (dilations [1, 2, 4, 8]) |
| Method | behaviour cloning, 5 epochs over 250,000 seat-turns, 93.8% held-out agreement |
| Adapter | 229,415 of 1,000,000 operations at its worst reference case |
| Inference | 34.58 ms at the worst reference case — **3.5%** of the 1000 ms a seat gets |
| Operators | Cast, Concat, Constant, Conv, Relu, Slice |
| Engine | `sha256:eead45ca770f5626d1787066bc00522687989101d4bf29ab3ec6ecb712755535` |
| Model hash | `sha256:1e51646a3987eb7844a7cd8e9c3f12f36d2a5d5a678286d856ac1c1be9801268` |
| Manifest hash | `sha256:4085e3b697ca43d90d54ae18510ab88090df8f363dc4e59a5c85edc166aa640b` |



Reproduce with `see README.md`.

Inference time is measured on whatever machine ran the check and is **reported, never a gate**:
there is no compute cap (devops decision 46). It is here because the turn deadline is what a graph
too expensive to play runs into, and a seat's share of it is the WHOLE turn -- one `model_infer`
call per seat, each with its own deadline (decision R7).
