@echo off
REM LichtFeld-Studio build for GTX 1070 (SM 6.1) - ASCII only
call "C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
if errorlevel 1 goto :fail

set "VCPKG_ROOT=E:\vcpkg"
set "VCPKG_MAX_CONCURRENCY=2"
set "NVCC_APPEND_FLAGS=--allow-unsupported-compiler"
set "CUDA_PATH_V12_8=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8"
set "PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin;E:\cmake-3.31.12-windows-x86_64\bin;E:\py\Scripts;%PATH%"

cd /d E:\lichtfeld-src
if errorlevel 1 goto :fail

echo [1/3] CMake configure...
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DENABLE_COMPILER_CACHE=OFF -DBUILD_TESTS=OFF -DCUDNN_ROOT_DIR=E:\cudnn-root -DCMAKE_CUDA_COMPILER="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.8\bin\nvcc.exe" -DCMAKE_CUDA_FLAGS="--allow-unsupported-compiler"
if errorlevel 1 goto :fail

echo [2/3] Build (first vcpkg deps build is slow)...
cmake --build build
if errorlevel 1 goto :fail

echo [3/3] BUILD OK
exit /b 0

:fail
echo BUILD_FAILED
exit /b 1
