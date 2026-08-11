# better-LichtFeld-Studio

> **LichtFeld Studio v0.4.2 — マルチアーキテクチャ版（GTX 10 系〜RTX 50 系対応）**

[![License: GPL-3.0-or-later](https://img.shields.io/badge/License-GPL--3.0--or--later-blue.svg)](LICENSE)

**言語:** [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

[LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio)（3D Gaussian Splatting）の自作マルチアーキテクチャ Windows ビルド。**Pascal（GTX 10 系、SM 6.1）から Blackwell（RTX 50 系、SM 12.0）までの全 NVIDIA GPU 世代に対応**しています。

公式バイナリは `sm_75+`（Turing 以降）の CUDA カーネルのみを内蔵しているため、Pascal（GTX 10 系）ではカーネルの読み込みに失敗し、静かに終了してしまいます。このビルドは 6 つのアーキテクチャのファットバイナリをコンパイルしており、全ラインの NVIDIA GPU でトレーニング・レンダリング・Vulkan ビジュアライゼーションが動作します。

## ライセンスと遵守事項（GPL-3.0）

- 本ソフトウェアは **GPL-3.0 プロジェクト [MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio)（v0.4.2）の派生作品**であり、GPL-3.0-or-later に基づき配布されます。
- **対応ソースコード**：
  - 上流：[MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio)（tag `v0.4.2`）
  - ローカル変更：本リポジトリの `patches/` ディレクトリに全変更を収録（再現可能なビルド用）
- 完全なライセンス文は [LICENSE](LICENSE)、サードパーティライセンスは [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) を参照。
- 著作権は LichtFeld Studio Authors に帰属し、本リポジトリの作者は変更部分について責任を負います。

## ダウンロード

[Releases](https://github.com/HongtaoWang75/better-LichtFeld-Studio/releases) ページの `LichtFeld-Studio-MultiArch.zip`（約 1.2GB、全ランタイム DLL と 10 言語パックを含む）。

**動作要件**：Windows 10/11 64bit、NVIDIA ドライバ ≥ 570（CUDA 12.8+）。

## クイックスタート

```bash
unzip LichtFeld-Studio-MultiArch.zip
cd LichtFeld-Studio-MultiArch
./LichtFeld-Studio.exe
```

## 対応 GPU

| SM | アーキテクチャ | GPU | シェア（Steam 2026-07） |
|----|--------------|-----|------------------------|
| 61 | Pascal | GTX 1060/1070/1080 | ~4.8% |
| 75 | Turing | GTX 1650/1660S, RTX 2060 | ~10.4% |
| 80 | Ampere | RTX 3090/3080 | ~3% |
| 86 | Ampere | RTX 3060/3050 | ~7% |
| 89 | Ada Lovelace | RTX 4060/4070/4090 | ~19-20% |
| 120 | Blackwell | RTX 5070/5060 シリーズ | ~16.6% |

**Steam の NVIDIA ユーザーの約 62%** と 3DGS 実務者全員の GPU をカバー。実行時に最適なカーネルが自動選択されるため、ユーザー操作は不要です。

> **注意**：AMD・Intel GPU には**非対応**です。ソースは CUDA 専用であり、AMD（HIP）への移植には 1 週間以上、Intel には完全な 3DGS トレーニング実装が現状ありません。

## 多言語 UI

UI には **10 言語の完全な翻訳**（各 2,049 キー）が同梱：中文(zh)、日本語(ja)、한국어(ko)、English(en)、Deutsch(de)、Español(es)、Français(fr)、Italiano(it)、Nederlands(nl)、Polski(pl)。

**言語を追加したい？** `resources/locales/` に新しい JSON ファイルを置くだけです。キー形式は [docs/TRANSLATIONS.md](docs/TRANSLATIONS.md) を参照。

## ソースからのビルド

要件：Windows + VS Build Tools（C++ と Clang 含む）、CUDA Toolkit 12.8、CMake 3.31+、vcpkg（フルクローン）。

環境の要点（`build_multi_arch.bat` に全て含む）：
```bat
rem 1. VS 18 (14.50) の vcvars を使用 — vcpkg 製依存ライブラリと ABI 一致させるため
call "...\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
rem 2. nvcc 12.8 は MSVC 14.50 を拒否するため許可
set NVCC_APPEND_FLAGS=--allow-unsupported-compiler
rem 3. サイレントインストールの CUDA はこの変数を設定しない — MSBuild 統合に必要
set CUDA_PATH_V12_8=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8
rem 4. vcpkg はフルクローン必須（シャロークローンは失敗）
rem 5. meson はパッチ未適用の 1.9.0 を使用（vcpkg パッチは Python 3.14 でクラッシュ）
```

アーキテクチャリストは `build_multi_arch.bat` 内：
```bat
-DCMAKE_CUDA_ARCHITECTURES=61;75;80;86;89;120
```

```bash
python auto_build.py   # 自動ビルド（失敗時リトライ/ミラー補完）
# または：
build_multi_arch.bat
```

出力：`build/LichtFeld-Studio.exe`（約 150-250MB のファットバイナリ）。

## 動作確認済み

- ✅ sm_61 カーネルのコンパイルと実行（GTX 1070、ドライバ 582.66）
- ✅ Vulkan 1.4 レンダリング、MCP サーバー、Python プラグインシステム全て正常
- ⚠️ Pascal の性能：Tensor Core 非搭載のため、トレーニング速度は RTX 40 系の約 1/10〜1/20

## 謝辞

[MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio) — 上流の GPL-3.0 プロジェクト
