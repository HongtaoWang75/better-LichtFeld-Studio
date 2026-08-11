# -*- coding: utf-8 -*-
"""自动构建循环：vcpkg 下载失败时自动通过镜像补缓存后重试"""
import os
import re
import shutil
import subprocess
import sys
import urllib.request

BUILD_LOG = r'C:\tmp\lf_build.log'
DOWNLOADS = r'E:\vcpkg\downloads'
BUILD_BAT = r'E:\lichtfeld-src\build_sm61.bat'

# 域名 → 国内镜像替换（vcpkg 直连不稳定的源）
MIRROR_MAP = [
    ('https://mirror.msys2.org/msys', 'https://mirrors.ustc.edu.cn/msys2/msys'),
    ('https://repo.msys2.org/msys', 'https://mirrors.ustc.edu.cn/msys2/msys'),
]
GHPROXY = 'https://ghproxy.net/'


def read_log():
    try:
        with open(BUILD_LOG, encoding='utf-8', errors='replace') as f:
            return f.read()
    except FileNotFoundError:
        return ''


def extract_failed_downloads(log):
    """从日志提取: {url: filename} 下载失败的项"""
    # 所有 Downloading <url> -> <name> 记录
    dl_map = {}
    for m in re.finditer(r'Downloading (\S+) -> (\S+)', log):
        dl_map[m.group(1)] = m.group(2)
    # 失败标记的 URL
    failed = set()
    for m in re.finditer(r"won't retry download from (\S+)", log):
        failed.add(m.group(1))
    return {u: dl_map.get(u, os.path.basename(u)) for u in failed}


def mirror_url(url):
    for src, dst in MIRROR_MAP:
        if url.startswith(src):
            return url.replace(src, dst, 1)
    return GHPROXY + url


def download(url, name):
    target = os.path.join(DOWNLOADS, name)
    if os.path.exists(target) and os.path.getsize(target) > 0:
        print(f'  [skip] {name} 已在缓存')
        return True
    src = mirror_url(url)
    print(f'  [dl] {src} -> {name}')
    try:
        req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=300) as r, open(target, 'wb') as f:
            f.write(r.read())
        size = os.path.getsize(target)
        if size < 1000:
            os.remove(target)
            print(f'  [fail] {name} 太小({size}B)，疑似错误页')
            return False
        print(f'  [ok] {name} ({size} bytes)')
        return True
    except Exception as e:
        print(f'  [fail] {name}: {e}')
        if os.path.exists(target):
            os.remove(target)
        return False


def main():
    max_rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    for rnd in range(1, max_rounds + 1):
        print(f'\n===== 第 {rnd} 轮构建 =====')
        # 清理 build 目录（避免坏缓存），重跑
        shutil.rmtree(r'E:\lichtfeld-src\build', ignore_errors=True)
        with open(BUILD_LOG, 'wb') as f:
            p = subprocess.run(
                ['powershell', '-NoProfile', '-Command', f"& '{BUILD_BAT}'"],
                stdout=f, stderr=subprocess.STDOUT)
        log = read_log()
        if 'BUILD OK' in log:
            print('🎉 构建成功！')
            return 0
        if 'BUILD_FAILED' not in log:
            print('⚠️ 异常退出，日志尾部:')
            print('\n'.join(log.strip().splitlines()[-10:]))
            return 1
        # 提取下载失败项
        failed = extract_failed_downloads(log)
        if not failed:
            print('❌ 非下载类失败，日志尾部:')
            print('\n'.join(log.strip().splitlines()[-30:]))
            return 1
        print(f'发现 {len(failed)} 个下载失败项:')
        all_ok = True
        for url, name in failed.items():
            if not download(url, name):
                all_ok = False
        if not all_ok:
            print('⚠️ 部分下载仍失败，重试')
        # 错误详情打印（非下载失败时有用）
        for line in log.strip().splitlines():
            if 'CMake Error at' in line or 'error: building' in line:
                print('  LOG:', line.strip())
    print('达到最大轮次，放弃。')
    return 1


if __name__ == '__main__':
    sys.exit(main())
