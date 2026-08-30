#!/bin/zsh
set -e

cd "${0:A:h}"

if [ ! -d node_modules ]; then
  echo "首次启动，正在准备图片工坊…"
  npm install
fi

echo "图片工坊已启动：http://127.0.0.1:4173/"
open "http://127.0.0.1:4173/"
npm run dev -- --port 4173
