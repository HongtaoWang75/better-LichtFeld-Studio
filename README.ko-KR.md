# better-LichtFeld-Studio

> **LichtFeld Studio v0.4.2 — 멀티 아키텍처 빌드 (GTX 10 시리즈 ~ RTX 50 시리즈 지원)**

[![License: GPL-3.0-or-later](https://img.shields.io/badge/License-GPL--3.0--or--later-blue.svg)](LICENSE)

**언어:** [English](README.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja-JP.md) · [한국어](README.ko-KR.md)

[LichtFeld Studio](https://github.com/MrNeRF/LichtFeld-Studio)(3D Gaussian Splatting)의 자체 컴파일 멀티 아키텍처 Windows 빌드입니다. **Pascal(GTX 10 시리즈, SM 6.1)부터 Blackwell(RTX 50 시리즈, SM 12.0)까지 모든 NVIDIA GPU 세대를 지원**합니다.

공식 바이너리는 `sm_75+`(Turing 이상) CUDA 커널만 포함하고 있어, Pascal(GTX 10 시리즈)에서는 커널 로딩에 실패하고 조용히 종료됩니다. 이 빌드는 6개 아키텍처의 팻 바이너리를 컴파일하여 전 라인의 NVIDIA GPU에서 트레이닝·렌더링·Vulkan 비주얼라이제이션이 모두 작동합니다.

## 라이선스 및 준수 사항 (GPL-3.0)

- 본 소프트웨어는 **GPL-3.0 오픈소스 프로젝트 [MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio)(v0.4.2)의 파생 저작물**이며, GPL-3.0-or-later 라이선스로 배포됩니다.
- **대응 소스코드**:
  - 업스트림: [MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio)(tag `v0.4.2`)
  - 로컬 수정: 이 저장소의 `patches/` 디렉토리에 모든 변경 사항 포함(재현 가능한 빌드용)
- 전체 라이선스: [LICENSE](LICENSE), 서드파티 라이선스: [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).
- 저작권은 LichtFeld Studio Authors에 있으며, 이 저장소의 저자는 수정 부분에 대해 책임을 집니다.

## 다운로드

[Releases](https://github.com/HongtaoWang75/better-LichtFeld-Studio/releases) 페이지의 `LichtFeld-Studio-MultiArch.zip`(약 1.2GB, 전체 런타임 DLL 및 10개 언어팩 포함).

**요구 사항**: Windows 10/11 64비트, NVIDIA 드라이버 ≥ 570 (CUDA 12.8+).

## 빠른 시작

```bash
unzip LichtFeld-Studio-MultiArch.zip
cd LichtFeld-Studio-MultiArch
./LichtFeld-Studio.exe
```

## 지원 GPU

| SM | 아키텍처 | GPU | 점유율 (Steam 2026-07) |
|----|---------|-----|------------------------|
| 61 | Pascal | GTX 1060/1070/1080 | ~4.8% |
| 75 | Turing | GTX 1650/1660S, RTX 2060 | ~10.4% |
| 80 | Ampere | RTX 3090/3080 | ~3% |
| 86 | Ampere | RTX 3060/3050 | ~7% |
| 89 | Ada Lovelace | RTX 4060/4070/4090 | ~19-20% |
| 120 | Blackwell | RTX 5070/5060 시리즈 | ~16.6% |

**Steam NVIDIA 사용자의 약 62%**와 3DGS 실무자 전원의 GPU를 커버합니다. 런타임이 자동으로 최적 커널을 선택하므로 사용자 개입이 필요 없습니다.

> **참고**: AMD·Intel GPU는 **미지원**입니다. 소스가 CUDA 전용이며, AMD(HIP) 이식에는 1주 이상, Intel에는 완전한 3DGS 트레이닝 구현이 현재 없습니다.

## 다국어 UI

UI에는 **10개 언어의 완전한 번역**(각 2,049키)이 포함: 中文(zh)、日本語(ja)、한국어(ko)、English(en)、Deutsch(de)、Español(es)、Français(fr)、Italiano(it)、Nederlands(nl)、Polski(pl).

**다른 언어가 필요하신가요?** `resources/locales/` 디렉토리에 새 JSON 파일을 넣기만 하면 됩니다. 키 형식은 [docs/TRANSLATIONS.md](docs/TRANSLATIONS.md) 참조.

## 소스에서 빌드

요구 사항: Windows + VS Build Tools(C++ 및 Clang 포함), CUDA Toolkit 12.8, CMake 3.31+, vcpkg(전체 클론).

환경 요점(`build_multi_arch.bat`에 모두 포함):
```bat
rem 1. VS 18 (14.50) vcvars 사용 — vcpkg 빌드 의존 라이브러리와 ABI 일치
call "...\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
rem 2. nvcc 12.8은 MSVC 14.50을 거부하므로 허용
set NVCC_APPEND_FLAGS=--allow-unsupported-compiler
rem 3. 무인 설치 CUDA는 이 변수를 설정하지 않음 — MSBuild 통합에 필요
set CUDA_PATH_V12_8=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8
rem 4. vcpkg는 전체 클론 필수(얕은 클론은 실패)
rem 5. meson은 패치 미적용 1.9.0 사용(vcpkg 패치는 Python 3.14에서 크래시)
```

아키텍처 목록은 `build_multi_arch.bat` 내부:
```bat
-DCMAKE_CUDA_ARCHITECTURES=61;75;80;86;89;120
```

```bash
python auto_build.py   # 자동 빌드(실패 시 재시도/미러 보충)
# 또는:
build_multi_arch.bat
```

산출물: `build/LichtFeld-Studio.exe`(약 150-250MB 팻 바이너리).

## 검증 완료

- ✅ sm_61 커널 컴파일 및 실행(GTX 1070, 드라이버 582.66)
- ✅ Vulkan 1.4 렌더링, MCP 서버, Python 플러그인 시스템 모두 정상
- ⚠️ Pascal 성능: Tensor Core 미탑재, 트레이닝 속도는 RTX 40 시리즈의 약 1/10~1/20

## 감사의 글

[MrNeRF/LichtFeld-Studio](https://github.com/MrNeRF/LichtFeld-Studio) — 업스트림 GPL-3.0 프로젝트
