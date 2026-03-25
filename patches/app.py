import shutil
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

import gradio as gr
import torch
import torchaudio
import os
# ... (ajouts en haut du fichier)
_GRADIO_MAJOR = int(gr.__version__.split(".")[0])

# Dans main(), remplacer le gr.File par :
if _GRADIO_MAJOR >= 5:
    _file_component = gr.File(
        file_count="multiple",
        file_types=[".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"],
        label="Input Audio Files (multiple)",
    )
else:
    _file_component = gr.File(
        type="filepath",
        file_count="multiple",
        file_types=["audio"],
        label="Input Audio Files (multiple)",
    )

# Et remplacer .launch() par :
port = int(os.environ.get("PORT", 7860))
gr.TabbedInterface([...]).launch(server_name="0.0.0.0", server_port=port, share=True)

from resemble_enhance.enhancer.inference import denoise, enhance

device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available()
    else "cpu"
)


def _process_audio(
    path: str, solver: str, nfe: int, tau: float, denoising: bool
) -> Tuple[int, torch.Tensor, torch.Tensor]:
    solver = solver.lower()
    nfe = int(nfe)
    lambd = 0.9 if denoising else 0.1

    dwav, sr = torchaudio.load(path)
    dwav = dwav.mean(dim=0)

    wav1, new_sr = denoise(dwav, sr, device)
    wav2, new_sr = enhance(dwav, sr, device, nfe=nfe, solver=solver, lambd=lambd, tau=tau)

    return new_sr, wav1.cpu(), wav2.cpu()


def _fn(path: Optional[str], solver, nfe, tau, denoising):
    if not path:
        return None, None

    sr, wav1, wav2 = _process_audio(path, solver, nfe, tau, denoising)
    return (sr, wav1.numpy()), (sr, wav2.numpy())


def _fn_batch(paths: Optional[List[str]], solver, nfe, tau, denoising):
    if not paths:
        return None, []

    normalized_paths = [
        p if isinstance(p, str) else getattr(p, "name", None) for p in paths
    ]
    normalized_paths = [p for p in normalized_paths if p]

    if not normalized_paths:
        return None, []

    output_dir = Path(tempfile.mkdtemp(prefix="resemble-enhance-batch-"))
    summary: List[List[str]] = []

    try:
        for path in normalized_paths:
            sr, wav1, wav2 = _process_audio(path, solver, nfe, tau, denoising)
            src = Path(path)
            denoised_path = output_dir / f"{src.stem}_denoised.wav"
            enhanced_path = output_dir / f"{src.stem}_enhanced.wav"

            try:
                import soundfile as sf

                sf.write(denoised_path, wav1.clamp(-1, 1).numpy(), sr, subtype="PCM_16")
                sf.write(enhanced_path, wav2.clamp(-1, 1).numpy(), sr, subtype="PCM_16")
            except Exception:
                torchaudio.save(
                    denoised_path,
                    torch.as_tensor(wav1).clamp(-1, 1).unsqueeze(0).float(),
                    sr,
                )
                torchaudio.save(
                    enhanced_path,
                    torch.as_tensor(wav2).clamp(-1, 1).unsqueeze(0).float(),
                    sr,
                )

            summary.append([src.name, denoised_path.name, enhanced_path.name])

        archive_path = shutil.make_archive(str(output_dir), "zip", output_dir)
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)

    return archive_path, summary


def main():
    single_inputs: list = [
        gr.Audio(type="filepath", label="Input Audio"),
        gr.Dropdown(choices=["Midpoint", "RK4", "Euler"], value="Midpoint", label="CFM ODE Solver"),
        gr.Slider(minimum=1, maximum=128, value=64, step=1, label="CFM Number of Function Evaluations"),
        gr.Slider(minimum=0, maximum=1, value=0.5, step=0.01, label="CFM Prior Temperature"),
        gr.Checkbox(value=False, label="Denoise Before Enhancement"),
    ]

    single_outputs: list = [
        gr.Audio(label="Output Denoised Audio"),
        gr.Audio(label="Output Enhanced Audio"),
    ]

    batch_inputs: list = [
        gr.File(
            type="filepath",
            file_count="multiple",
            file_types=["audio"],
            label="Input Audio Files (multiple)",
        ),
        gr.Dropdown(choices=["Midpoint", "RK4", "Euler"], value="Midpoint", label="CFM ODE Solver"),
        gr.Slider(minimum=1, maximum=128, value=64, step=1, label="CFM Number of Function Evaluations"),
        gr.Slider(minimum=0, maximum=1, value=0.5, step=0.01, label="CFM Prior Temperature"),
        gr.Checkbox(value=False, label="Denoise Before Enhancement"),
    ]

    batch_outputs: list = [
        gr.File(label="Download Zipped Results"),
        gr.Dataframe(
            headers=["Input File", "Denoised Output", "Enhanced Output"],
            datatype=["str", "str", "str"],
            interactive=False,
            label="Output File Map",
        ),
    ]

    single_interface = gr.Interface(
        fn=_fn,
        title="Resemble Enhance",
        description="AI-driven audio enhancement for your audio files, powered by Resemble AI.",
        inputs=single_inputs,
        outputs=single_outputs,
    )

    batch_interface = gr.Interface(
        fn=_fn_batch,
        title="Resemble Enhance (Batch)",
        description="Upload multiple audio files and download a zip containing denoised and enhanced results.",
        inputs=batch_inputs,
        outputs=batch_outputs,
    )

    gr.TabbedInterface(
        [single_interface, batch_interface], ["Single File", "Batch"]
    ).launch()


if __name__ == "__main__":
    main()
