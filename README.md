# ants-starter

A working TinyBrains entry you can submit unchanged, and the one command that retrains it.

```sh
brew tap tiny-brains/cli https://github.com/Tiny-Brains/cli    # once
brew install tiny-brains/cli/tinybrains                         # once
git clone https://github.com/Tiny-Brains/ants-starter && cd ants-starter

tinybrains check model.onnx manifest.json      # what admission will say
tinybrains matches/self-play.json              # play it against itself, through the real engine
tinybrains view replays/self-play.json         # watch it
python train.py                                # retrain it: collect, clone, export -- about an hour
```

The entry is a **nano** class model — the smallest class the ladder runs — trained the way the
platform's own baselines are trained: a scripted teacher plays, a small convolutional policy is
cloned from its moves, and the export writes `model.onnx`, the `manifest.json` that describes it,
`metrics.json` with what the platform measures, and `card.md`, which is where the numbers are. It
is not one of the baselines: it was trained with its own seed, so its weights are its own and the
ladder takes it as a new entry.

## What is in the box

| File | What it is |
|---|---|
| `model.onnx` | The trained policy. Float16 initializers, cast to float32 at use. |
| `manifest.json` | What the platform runs the graph under: the declared inputs and outputs, and one **adapter** expression per input that turns the observation into the tensor. Generated, never hand-edited. |
| `metrics.json`, `card.md` | What the platform measures about the entry, and the numbers in words. |
| `train.py` | The whole recipe as one command, on top of [the baselines](https://github.com/Tiny-Brains/ants/tree/main/baselines). |
| `matches/` | Two match files: the entry against itself, and against the platform's nano baseline, fetched by URL from a pinned commit of `ants/baselines`. |
| `games.toml` | Where the game comes from: a pinned release of the Ants cartridge, downloaded once and checked against its digests. |
| `.github/workflows/check.yml` | Runs `tinybrains check` and a match on every push, so a manifest change nobody meant is caught on the commit that made it. |

## What you need

`tinybrains` — Homebrew as above, or the archive for your platform from its
[latest release](https://github.com/Tiny-Brains/cli/releases/latest) — and this clone: **no other
repository beside it, and no Rust toolchain**. The game is not in this repository and not built
here: `games.toml` pins a release of the Ants cartridge by two digests, the archive's and the
engine's, and the first command that needs it downloads it into `~/.cache/tinybrains/cartridges/`
and refuses it unless both match. `python train.py` additionally
wants Python and `pip install -r requirements.txt`, which installs the baselines library from git.

## Make it yours

1. **Play it.** `tinybrains matches/self-play.json`, then `tinybrains view replays/self-play.json`.
   The ants should move. `matches/vs-nano-bc.json` plays it against the platform's nano baseline.
   To play another board or opponent, edit a match file — the book's
   [match files](https://github.com/Tiny-Brains/web/blob/main/docs/src/models/testing.md#match-files)
   section lists every field.
2. **Change something and retrain.** `train.py` takes `--class`, `--epochs`, `--seed`; the recipe
   underneath is `tb_baselines`, whose [README](https://github.com/Tiny-Brains/ants/tree/main/baselines) says
   what each knob measured. Width, depth and float16 are the levers that move the one number that
   decides your class. A different encoding means a different adapter, and the manifest is generated
   from the same code that trains — [that is the one test that matters](https://github.com/Tiny-Brains/ants/tree/main/baselines#the-one-test-that-matters).
3. **Check it the way admission will.** `tinybrains check model.onnx manifest.json`. A pass is
   necessary and not sufficient: your machine decides no class.
4. **Submit and upload.** Take the two hashes with `shasum -a 256 model.onnx manifest.json` and
   submit them on the site. The submission answers with **two one-shot upload URLs**; `PUT` the two files to them
   and admission takes it from there. The book's
   [quickstart](https://github.com/Tiny-Brains/web/blob/main/docs/src/quickstart.md) is the long form.

## What must stay true

- **`manifest.json` is generated.** Editing it by hand is how the encoding the trainer saw and the
  encoding the ladder runs come apart, and nothing fails when they do: the rating is simply lower
  than training promised. Change `planes.py` in `ants/baselines` and regenerate.
- **Nothing here is a rule.** Presets, budgets and deadlines come from the cartridge and are printed
  on every run; `max_turns` in a match file is the one local override, so a local match is short.
- **The four files ship together.** A model and its manifest are hashed and measured as a pair —
  the weight class is the artifact's bytes plus the manifest's — and the card and metrics say what
  that pair measured.

Apache-2.0: see [LICENSE](LICENSE).
