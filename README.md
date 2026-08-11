# better-LichtFeld-Studio

> **LichtFeld Studio v0.4.2 — multi-architecture build for GTX 10 series through RTX 50 series**

[![License: GPL-3.0-or-later](https://img.shields.io/badge/License-GPL--3.0--or--later-blue.svg)](LICENSE)

**🌐 Languages:** [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

A self-compiled multi-architecture Windows build of [LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio) (3D Gaussian Splatting), **supporting every NVIDIA GPU generation from Pascal (GTX 10 series, SM 6.1) to Blackwell (RTX 50 series, SM 12.0)**.

The official binaries only ship `sm_75+` (Turing and newer) CUDA kernels, so Pascal cards (GTX 10 series) fail to load them and exit silently. This build compiles fat binaries for 6 architectures so the full range of NVIDIA GPUs can run it — training, rendering, and Vulkan visualization all work.

## ⚠️ License & compliance (GPL-3.0)

- This software is a **derivative work of the GPL-3.0 project [MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio) (v0.4.2)**, distributed under GPL-3.0-or-later.
- **Corresponding source:**
  - Upstream: [MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio) (tag `v0.4.2`)
  - Local modifications: every change is in `patches/` in this repository, for reproducible builds.
- Full license text: [LICENSE](LICENSE). Third-party licenses: [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
- Copyright belongs to the LichtFeld Studio Authors; the author of this repository is responsible for the modifications.

## 📥 Download

See the [Releases](https://github.com/HongtaoWang75/better-LichtFeld-Studio/releases) page: `LichtFeld-Studio-MultiArch.zip` (~1.2GB, includes all runtime DLLs and 10 language packs).

**Requirements:** Windows 10/11 64-bit, NVIDIA driver ≥ 570 (CUDA 12.8+).

## 🚀 Quick start

```bash
unzip LichtFeld-Studio-MultiArch.zip
cd LichtFeld-Studio-MultiArch
./LichtFeld-Studio.exe
```

## 🎮 Supported GPUs

| SM | Architecture | GPUs | Share (Steam 2026-07) |
|----|--------------|------|-----------------------|
| 61 | Pascal | GTX 1060/1070/1080 | ~4.8% |
| 75 | Turing | GTX 1650/1660S, RTX 2060 | ~10.4% |
| 80 | Ampere | RTX 3090/3080 | ~3% |
| 86 | Ampere | RTX 3060/3050 | ~7% |
| 89 | Ada Lovelace | RTX 4060/4070/4090 | ~19-20% |
| 120 | Blackwell | RTX 5070/5060 series | ~16.6% |

Covers **~62% of Steam NVIDIA users** and 100% of 3DGS practitioners' cards. The runtime automatically picks the best-matching kernel — no user intervention needed.

> **Note:** AMD and Intel GPUs are **not** supported. The source is CUDA-only; porting to AMD (HIP) is a 1-week+ effort and Intel lacks a complete 3DGS training implementation.

## 🌍 Multi-language UI

The UI ships with **10 complete languages** (2,049 keys each): 中文(zh), 日本語(ja), 한국어(ko), English(en), Deutsch(de), Español(es), Français(fr), Italiano(it), Nederlands(nl), Polski(pl).

**Want another language?** Just drop a new JSON file into `resources/locales/` next to the others — see [docs/TRANSLATIONS.md](docs/TRANSLATIONS.md) for the key format.

## 🛠️ Building from source

Requirements: Windows + VS Build Tools (with C++ + Clang), CUDA Toolkit 12.8, CMake 3.31+, vcpkg (full clone).

Environment essentials (all in `build_multi_arch.bat`):
```bat
rem 1. Use VS 18 (14.50) vcvars — must match the ABI of vcpkg-built deps
call "...\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
rem 2. nvcc 12.8 rejects MSVC 14.50 — allow it
set NVCC_APPEND_FLAGS=--allow-unsupported-compiler
rem 3. Silent CUDA installs omit this — MSBuild CUDA integration needs it
set CUDA_PATH_V12_8=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8
rem 4. vcpkg must be a FULL clone (shallow clones fail)
rem 5. Use pristine meson 1.9.0 (vcpkg patches crash under Python 3.14)
```

The architecture list lives in `build_multi_arch.bat`:
```bat
-DCMAKE_CUDA_ARCHITECTURES=61;75;80;86;89;120
```

```bash
python auto_build.py   # automatic build with retry/mirror fallback
# or:
build_multi_arch.bat
```

Output: `build/LichtFeld-Studio.exe` (~150-250MB fat binary).

## 📋 Verified

- ✅ sm_61 kernels compile and run (GTX 1070, driver 582.66)
- ✅ Vulkan 1.4 rendering, MCP server, Python plugin system all work
- ⚠️ Pascal performance: no Tensor Cores — expect 1/10~1/20 of RTX 40-series training speed

## 🙏 Credits

[MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio) — upstream GPL-3.0 project
