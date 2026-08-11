# better-LichtFeld-Studio

> **LichtFeld Studio v0.4.2 — 多架构版，支持 GTX 10 系列到 RTX 50 系列**

[![License: GPL-3.0-or-later](https://img.shields.io/badge/License-GPL--3.0--or--later-blue.svg)](LICENSE)

**🌐 语言:** [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

[LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio)（3D 高斯泼溅）的自编译多架构 Windows 版，**支持从 Pascal（GTX 10 系列，SM 6.1）到 Blackwell（RTX 50 系列，SM 12.0）的全部 NVIDIA 显卡世代**。

官方二进制只内置 `sm_75+`（Turing 及以上）的 CUDA 内核，Pascal 显卡（GTX 10 系列）加载内核即失败并静默退出。本版本编译了 6 个架构的胖二进制，让全线 NVIDIA 显卡都能运行——训练、渲染、Vulkan 可视化全部可用。

## ⚠️ 许可证与合规声明（GPL-3.0）

- 本软件是 **GPL-3.0 开源项目 [MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio)（v0.4.2）的衍生作品**，依据 GPL-3.0-or-later 许可分发。
- **对应源码**：
  - 上游：[MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio)（tag `v0.4.2`）
  - 本地修改：本仓库 `patches/` 目录包含全部修改，可复现构建。
- 完整许可证见 [LICENSE](LICENSE)，第三方依赖许可见 [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md)。
- 版权归 LichtFeld Studio Authors 所有，本仓库作者对修改部分负责。

## 📥 下载

见 [Releases](https://github.com/HongtaoWang75/better-LichtFeld-Studio/releases) 页面：`LichtFeld-Studio-MultiArch.zip`（约 1.2GB，含全部运行时 DLL 和 10 种语言包）。

**运行要求**：Windows 10/11 64 位、NVIDIA 驱动 ≥ 570（CUDA 12.8+）。

## 🚀 快速开始

```bash
unzip LichtFeld-Studio-MultiArch.zip
cd LichtFeld-Studio-MultiArch
./LichtFeld-Studio.exe
```

## 🎮 支持的显卡

| SM | 架构 | 代表显卡 | 份额（Steam 2026-07） |
|----|------|---------|----------------------|
| 61 | Pascal | GTX 1060/1070/1080 | ~4.8% |
| 75 | Turing | GTX 1650/1660S, RTX 2060 | ~10.4% |
| 80 | Ampere | RTX 3090/3080 | ~3% |
| 86 | Ampere | RTX 3060/3050 | ~7% |
| 89 | Ada Lovelace | RTX 4060/4070/4090 | ~19-20% |
| 120 | Blackwell | RTX 5070/5060 系列 | ~16.6% |

覆盖 **约 62% 的 Steam NVIDIA 用户**和全部 3DGS 从业者的显卡。运行时自动选择最匹配的内核，无需用户干预。

> **注意**：AMD 和 Intel 显卡**不支持**。源码是 CUDA-only；移植到 AMD（HIP）需要 1 周以上工作量，Intel 目前没有完整的 3DGS 训练实现。

## 🌍 多语言界面

界面内置 **10 种完整语言**（每种 2049 个翻译键）：中文(zh)、日本語(ja)、한국어(ko)、English(en)、Deutsch(de)、Español(es)、Français(fr)、Italiano(it)、Nederlands(nl)、Polski(pl)。

**想要更多语言？** 只需在 `resources/locales/` 目录放一个新的 JSON 文件即可——格式见 [docs/TRANSLATIONS.md](docs/TRANSLATIONS.md)。

## 🛠️ 源码构建

要求：Windows + VS Build Tools（含 C++ 和 Clang）、CUDA Toolkit 12.8、CMake 3.31+、vcpkg（完整克隆）。

环境要点（`build_multi_arch.bat` 已全部包含）：
```bat
rem 1. 必须用 VS 18 (14.50) 的 vcvars —— 与 vcpkg 编译的依赖库 ABI 一致
call "...\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
rem 2. nvcc 12.8 不认 MSVC 14.50，需放行
set NVCC_APPEND_FLAGS=--allow-unsupported-compiler
rem 3. 静默安装的 CUDA 不设置此变量，MSBuild CUDA 集成会报错
set CUDA_PATH_V12_8=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8
rem 4. vcpkg 必须完整克隆（浅克隆会失败）
rem 5. meson 用原始未打补丁 1.9.0（vcpkg patches 在 Python 3.14 下崩溃）
```

架构列表在 `build_multi_arch.bat` 中：
```bat
-DCMAKE_CUDA_ARCHITECTURES=61;75;80;86;89;120
```

```bash
python auto_build.py   # 自动构建（失败重试/镜像补缓存）
# 或：
build_multi_arch.bat
```

产物：`build/LichtFeld-Studio.exe`（约 150-250MB 胖二进制）。

## 📋 已验证

- ✅ sm_61 内核编译并运行（GTX 1070，驱动 582.66）
- ✅ Vulkan 1.4 渲染、MCP 服务器、Python 插件系统全部正常
- ⚠️ Pascal 性能：无 Tensor Core，训练速度约为 RTX 40 系的 1/10~1/20

## 🙏 致谢

[MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio) — 上游 GPL-3.0 项目
