# Resemble Enhance — Pinokio one‑click installer

This repo is a **Pinokio script** that installs and runs **Resemble Enhance** (speech denoising + enhancement) locally.

Upstream project: https://github.com/resemble-ai/resemble-enhance

## What this Pinokio app does

- Clones the upstream repo into `app/resemble-enhance`
- Creates a venv at `app/env`
- Installs dependencies + installs the package in editable mode (`pip install -e`) so the `resemble-enhance` CLI is available
- Starts the **Gradio web demo** (`python resemble-enhance/app.py`)

## Usage in Pinokio

1. Open Pinokio → **Download from URL** → paste this repo URL.
2. Open the app page. It should **auto-run**:
   - `install.json` if not installed
   - `start.json` if installed (Pinokio v2 “default: true” menu behavior)

## CLI usage (inside Pinokio terminal)

Once installed:

```bash
# From app root (Pinokio sets working dir)
./env/bin/resemble-enhance in_dir out_dir
./env/bin/resemble-enhance in_dir out_dir --denoise_only
```

Upstream CLI reference is in the Resemble Enhance README.

## Notes / Caveats

- First run can take a while (torch + audio deps).
- On some Windows setups, Python version constraints can bite (common for ML stacks). If you hit build issues, try Python 3.10/3.11.

## Files

- `pinokio.js` — menu + “autostart” logic
- `install.json` — clone + venv + pip install
- `start.json` — start Gradio app
- `update.json` — git pull + re-install deps
- `reset.json` — wipe `app/env` and `app/resemble-enhance`
- `ENVIRONMENT` — app-scoped env vars (currently just `PORT`)
