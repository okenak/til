# novelai-cli

NovelAI の画像生成 API を利用するシンプルな CLI ツール。

## セットアップ

```bash
cd novelai-cli
pip install -e .
```

## 初期設定

NovelAI の API トークンを設定する。トークンは NovelAI のアカウント設定画面から「Get Persistent API Token」で取得できる。

```bash
novelai-cli init
```

設定は `~/.config/novelai-cli/config.json` に保存される。

## 使い方

### 画像生成

```bash
# 基本的な使い方
novelai-cli generate "1girl, beautiful scenery, sunset"

# オプション指定
novelai-cli gen "1girl, school uniform" \
  -m nai-diffusion-4-5-full \
  -W 1024 -H 1024 \
  --steps 28 \
  --scale 5.0 \
  --seed 42 \
  -n "lowres, bad anatomy" \
  -o ./images \
  --prefix my_image

# 複数枚生成
novelai-cli gen "landscape, fantasy" --samples 4
```

### 設定確認

```bash
novelai-cli config
```

## オプション一覧

| オプション | 短縮 | 説明 | デフォルト |
|---|---|---|---|
| `--model` | `-m` | モデル名 | `nai-diffusion-4-5-curated` |
| `--width` | `-W` | 画像の幅 | `832` |
| `--height` | `-H` | 画像の高さ | `1216` |
| `--steps` | | ステップ数 | `28` |
| `--scale` | | ガイダンス強度 | `5.0` |
| `--sampler` | | サンプラー | `k_euler_ancestral` |
| `--seed` | | シード値 (0=ランダム) | `0` |
| `--samples` | | 生成枚数 | `1` |
| `--negative-prompt` | `-n` | ネガティブプロンプト | 設定ファイルの値 |
| `--output-dir` | `-o` | 出力先ディレクトリ | `.` |
| `--prefix` | | ファイル名プレフィックス | `output` |

## 利用可能なモデル

- `nai-diffusion-4-5-full` - NAI Diffusion V4.5 Full
- `nai-diffusion-4-5-curated` - NAI Diffusion V4.5 Curated
- `nai-diffusion-4-curated-preview` - NAI Diffusion V4 Curated Preview
- `nai-diffusion-3` - NAI Diffusion V3

## 設定ファイル

`~/.config/novelai-cli/config.json` でデフォルト値を変更可能:

```json
{
  "token": "your-api-token",
  "model": "nai-diffusion-4-5-curated",
  "width": 832,
  "height": 1216,
  "steps": 28,
  "scale": 5.0,
  "sampler": "k_euler_ancestral",
  "negative_prompt": "lowres, bad anatomy, bad hands, missing fingers, extra digits",
  "output_dir": "."
}
```
