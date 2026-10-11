#!/usr/bin/env bash
# main2 编译脚本 —— 由本地(有完整 LaTeX 环境)执行，Arena 沙箱无 LaTeX 不编译。
# 用法: cd main2 && bash compile.sh
set -u
cd "$(dirname "$0")"

if ! command -v xelatex >/dev/null 2>&1; then
  echo "ERROR: 未找到 xelatex (TinyTeX?)" >&2
  exit 2
fi

# 第一遍：生成 aux/toc
echo ">> [1/2] xelatex pass 1"
xelatex -interaction=nonstopmode -halt-on-error main2.tex >/tmp/main2_build.log 2>&1 \
  && echo "   pass1 OK" || { echo "   pass1 有错误(见 /tmp/main2_build.log)"; }

# 第二遍：解析交叉引用 / 目录
echo ">> [2/2] xelatex pass 2"
xelatex -interaction=nonstopmode -halt-on-error main2.tex >>/tmp/main2_build.log 2>&1 \
  && echo "   pass2 OK" || echo "   pass2 有错误(见 /tmp/main2_build.log)"

if [ -f main2.pdf ]; then
  echo "BUILD OK -> $(pwd)/main2.pdf ($(stat -f%z main2.pdf) bytes)"
else
  echo "BUILD FAILED: main2.pdf 未生成"
  grep -nE '^!|Emergency stop|File .* not found' /tmp/main2_build.log | head -20
  exit 1
fi
