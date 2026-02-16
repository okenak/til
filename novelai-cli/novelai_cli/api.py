"""NovelAI 画像生成 API クライアント。"""

import io
import zipfile
from pathlib import Path

import requests

API_URL = "https://image.novelai.net/ai/generate-image"

MODELS = [
    "nai-diffusion-4-5-full",
    "nai-diffusion-4-5-curated",
    "nai-diffusion-4-curated-preview",
    "nai-diffusion-3",
]

SAMPLERS = [
    "k_euler_ancestral",
    "k_euler",
    "k_dpmpp_2s_ancestral",
    "k_dpmpp_2m",
    "k_dpmpp_sde",
    "k_dpmpp_2m_sde",
]


def generate_image(
    token: str,
    prompt: str,
    *,
    model: str = "nai-diffusion-4-5-curated",
    negative_prompt: str = "",
    width: int = 832,
    height: int = 1216,
    steps: int = 28,
    scale: float = 5.0,
    sampler: str = "k_euler_ancestral",
    seed: int = 0,
    n_samples: int = 1,
) -> list[bytes]:
    """NovelAI API で画像を生成し、PNG バイト列のリストを返す。"""
    payload = {
        "input": prompt,
        "model": model,
        "action": "generate",
        "parameters": {
            "width": width,
            "height": height,
            "steps": steps,
            "scale": scale,
            "sampler": sampler,
            "seed": seed,
            "n_samples": n_samples,
            "negative_prompt": negative_prompt,
            "ucPreset": 0,
            "qualityToggle": True,
            "dynamic_thresholding": False,
            "sm": False,
            "sm_dyn": False,
        },
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=120)
    resp.raise_for_status()

    images = []
    with zipfile.ZipFile(io.BytesIO(resp.content)) as zf:
        for name in zf.namelist():
            if name.endswith(".png"):
                images.append(zf.read(name))

    return images


def save_images(images: list[bytes], output_dir: str, prefix: str = "output") -> list[Path]:
    """画像を保存し、保存先パスのリストを返す。"""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    saved = []
    for i, data in enumerate(images):
        suffix = f"_{i}" if len(images) > 1 else ""
        path = out / f"{prefix}{suffix}.png"
        # 同名ファイルがあれば番号を付ける
        counter = 1
        while path.exists():
            path = out / f"{prefix}{suffix}_{counter}.png"
            counter += 1
        path.write_bytes(data)
        saved.append(path)

    return saved
