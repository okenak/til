"""設定ファイルの読み書きを管理する。"""

import json
import os
from pathlib import Path

CONFIG_DIR = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "novelai-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "token": "",
    "model": "nai-diffusion-4-5-curated",
    "width": 832,
    "height": 1216,
    "steps": 28,
    "scale": 5.0,
    "sampler": "k_euler_ancestral",
    "negative_prompt": "lowres, bad anatomy, bad hands, missing fingers, extra digits",
    "output_dir": ".",
}


def load_config() -> dict:
    """設定ファイルを読み込む。存在しなければデフォルト値を返す。"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            saved = json.load(f)
        merged = {**DEFAULT_CONFIG, **saved}
        return merged
    return dict(DEFAULT_CONFIG)


def save_config(config: dict) -> None:
    """設定をファイルに書き込む。"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def init_config() -> dict:
    """対話的に初期設定を行い、設定ファイルを作成する。"""
    config = dict(DEFAULT_CONFIG)
    token = input("NovelAI API トークンを入力してください: ").strip()
    if not token:
        print("トークンが空です。後で設定ファイルを編集してください:")
        print(f"  {CONFIG_FILE}")
    config["token"] = token
    save_config(config)
    print(f"設定を保存しました: {CONFIG_FILE}")
    return config
