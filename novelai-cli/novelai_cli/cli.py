"""NovelAI 画像生成 CLI のエントリーポイント。"""

import argparse
import sys
import time

from novelai_cli.api import MODELS, SAMPLERS, generate_image, save_images
from novelai_cli.config import CONFIG_FILE, init_config, load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="novelai-cli",
        description="NovelAI で画像を生成する CLI ツール",
    )
    sub = parser.add_subparsers(dest="command")

    # --- init ---
    sub.add_parser("init", help="初期設定（トークン等）を行う")

    # --- generate ---
    gen = sub.add_parser("generate", aliases=["gen"], help="画像を生成する")
    gen.add_argument("prompt", help="生成プロンプト")
    gen.add_argument("-n", "--negative-prompt", help="ネガティブプロンプト")
    gen.add_argument("-m", "--model", choices=MODELS, help="モデル名")
    gen.add_argument("-W", "--width", type=int, help="画像の幅")
    gen.add_argument("-H", "--height", type=int, help="画像の高さ")
    gen.add_argument("--steps", type=int, help="ステップ数")
    gen.add_argument("--scale", type=float, help="プロンプトガイダンス強度")
    gen.add_argument("--sampler", choices=SAMPLERS, help="サンプラー")
    gen.add_argument("--seed", type=int, help="シード値 (0=ランダム)")
    gen.add_argument("--samples", type=int, default=1, help="生成枚数 (デフォルト: 1)")
    gen.add_argument("-o", "--output-dir", help="出力ディレクトリ")
    gen.add_argument("--prefix", default="output", help="ファイル名のプレフィックス (デフォルト: output)")

    # --- config ---
    sub.add_parser("config", help="現在の設定を表示する")

    return parser


def cmd_init() -> None:
    init_config()


def cmd_config() -> None:
    config = load_config()
    masked = {**config}
    if masked.get("token"):
        t = masked["token"]
        masked["token"] = t[:8] + "..." + t[-4:] if len(t) > 12 else "***"
    for k, v in masked.items():
        print(f"  {k}: {v}")
    print(f"\n設定ファイル: {CONFIG_FILE}")


def cmd_generate(args: argparse.Namespace) -> None:
    config = load_config()
    token = config.get("token", "")
    if not token:
        print("エラー: トークンが設定されていません。先に `novelai-cli init` を実行してください。", file=sys.stderr)
        sys.exit(1)

    # CLI 引数で上書き（指定されたもののみ）
    model = args.model or config["model"]
    width = args.width or config["width"]
    height = args.height or config["height"]
    steps = args.steps or config["steps"]
    scale = args.scale if args.scale is not None else config["scale"]
    sampler = args.sampler or config["sampler"]
    seed = args.seed if args.seed is not None else 0
    negative_prompt = args.negative_prompt if args.negative_prompt is not None else config["negative_prompt"]
    output_dir = args.output_dir or config.get("output_dir", ".")

    print(f"モデル: {model}")
    print(f"サイズ: {width}x{height}")
    print(f"プロンプト: {args.prompt}")
    print("生成中...")

    start = time.time()
    try:
        images = generate_image(
            token=token,
            prompt=args.prompt,
            model=model,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            steps=steps,
            scale=scale,
            sampler=sampler,
            seed=seed,
            n_samples=args.samples,
        )
    except Exception as e:
        print(f"エラー: {e}", file=sys.stderr)
        sys.exit(1)

    elapsed = time.time() - start
    saved = save_images(images, output_dir, prefix=args.prefix)

    for p in saved:
        print(f"保存: {p}")
    print(f"完了 ({elapsed:.1f}秒, {len(saved)}枚)")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command in ("generate", "gen"):
        cmd_generate(args)
    elif args.command == "config":
        cmd_config()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
