# Resemble Enhance — Pinokio one‑click installer

This repo is a **Pinokio script** that installs and runs **Resemble Enhance** (speech denoising + enhancement) locally.

Upstream project: https://github.com/resemble-ai/resemble-enhance

## What this Pinokio app does

- Clones the upstream repo into `app/`
- Creates/uses a venv at `app/env` (via Pinokio `venv` support)
- Installs PyTorch in a cross-platform way (`torch.js`), then installs Python deps with `uv pip`
- Installs the package in editable mode (`uv pip install -e .`) so the `resemble-enhance` CLI is available
- Starts the **Gradio web demo** (`python app.py`) and captures the live URL so Pinokio can show an **Open Web UI** button

## Usage in Pinokio

1. Open Pinokio → **Download from URL** → paste this repo URL.
2. Open the app page. It should **auto-run**:
   - `install.json` if not installed
   - `start.json` if installed (Pinokio v2 “default: true” menu behavior)

## CLI usage (inside Pinokio terminal)

Once installed:

```bash
# From `app/` (common if you open the "Terminal" tab)
./env/bin/resemble-enhance in_dir out_dir
./env/bin/resemble-enhance in_dir out_dir --denoise_only

# From project root
./app/env/bin/resemble-enhance in_dir out_dir
```

Upstream CLI reference is in the Resemble Enhance README.

## Programmatic usage (API-ish)

Resemble Enhance is primarily a **local CLI + Python package**. The Gradio UI is convenient, but the most stable “API” is the CLI or importing the library.

### JavaScript (spawn the CLI)

```js
import { spawn } from "node:child_process";

const proc = spawn("./app/env/bin/resemble-enhance", ["in_dir", "out_dir"], {
  stdio: "inherit",
});

proc.on("exit", (code) => process.exit(code ?? 1));
```

### Python (import + run inference)

```py
import torchaudio
from resemble_enhance.enhancer.inference import denoise, enhance

dwav, sr = torchaudio.load("input.wav")
dwav = dwav.mean(0)

wav_d, sr_d = denoise(dwav, sr, device="cpu")
wav_e, sr_e = enhance(dwav, sr, device="cpu")

torchaudio.save("denoised.wav", wav_d[None], sr_d)
torchaudio.save("enhanced.wav", wav_e[None], sr_e)
```

### Curl (check the local web UI + discover endpoints)

```bash
# Replace with the URL shown in Pinokio (for example: http://127.0.0.1:7860)
URL="http://127.0.0.1:7860"

# Basic health check (should return HTML headers)
curl -I "$URL/"

# Gradio usually exposes a config endpoint that describes routes/functions
curl -s "$URL/config" | head
```

## Notes / Caveats

- First run can take a while (torch + audio deps).
- On some Windows setups, Python version constraints can bite (common for ML stacks). If you hit build issues, try Python 3.10/3.11.

## Troubleshooting

- Check the Pinokio logs folder first:
  - `pinokio/logs/` if your project has a `pinokio/` directory
  - otherwise `logs/` at project root

## Files

- `pinokio.js` — menu + “autostart” logic
- `pinokio.json` — project metadata (title, icon, links)
- `install.json` — clone + venv + dependency install
- `start.json` — start Gradio app
- `update.json` — git pull + re-install deps
- `reset.json` — wipe `app/`
- `torch.js` — cross-platform PyTorch installer helper (used by `install.json`)
- `ENVIRONMENT` — app-scoped env vars (currently just `PORT`)
- `.gitignore` — ignores runtime state like `app/` and `logs/`
