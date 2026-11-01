#!/usr/bin/env bash
# 把 GitHub 上最新一次 CI 构建的产物同步到本机 nginx 根目录。
# 只做下载与安装，不构建、不跑测试。
set -euo pipefail

REPO="hanlinlibham/lihanlin.com"
WEB="/var/www/html"
BACKUP_DIR="/var/www/backups"
TAG="build-latest"

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "→ 查询最新构建"
ASSET="$(curl -fsSL -H 'accept: application/vnd.github+json' \
  "https://api.github.com/repos/${REPO}/releases/tags/${TAG}" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print([a["browser_download_url"] for a in d["assets"] if a["name"]=="dist.zip"][0])')"
PUBLISHED="$(curl -fsSL -H 'accept: application/vnd.github+json' \
  "https://api.github.com/repos/${REPO}/releases/tags/${TAG}" \
  | python3 -c 'import json,sys; print(json.load(sys.stdin)["published_at"])')"
echo "  $PUBLISHED"

echo "→ 下载"
curl -fsSL "$ASSET" -o "$TMP/dist.zip"
unzip -q "$TMP/dist.zip" -d "$TMP/dist"
[ -f "$TMP/dist/index.html" ] || { echo "✗ 产物里没有 index.html"; exit 1; }

echo "→ 备份当前站点"
sudo mkdir -p "$BACKUP_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
sudo tar -czf "$BACKUP_DIR/site-${STAMP}.tar.gz" -C "$WEB" . 2>/dev/null || true
sudo ls -1t "$BACKUP_DIR"/site-*.tar.gz 2>/dev/null | tail -n +6 | xargs -r sudo rm -f

echo "→ 安装"
sudo rm -rf "$WEB/_astro"
# 只覆盖构建产物里的条目，保留 /ableflow/ /ablemind/ /iran-timeline/ 等非本站目录
sudo cp -a "$TMP/dist/." "$WEB/"
sudo chown -R www-data:www-data "$WEB" 2>/dev/null || true
sudo chmod -R a+rX "$WEB"

echo "→ 冒烟"
for path in / /daily/ /progress/ /og.png /404.html; do
  code="$(curl -s -o /dev/null -w '%{http_code}' -H 'Host: lihanlin.com' "http://127.0.0.1${path}")"
  echo "  ${code}  ${path}"
  [ "$code" = "200" ] || [ "$path" = "/404.html" ]
done

echo "✓ 完成（备份：$BACKUP_DIR/site-${STAMP}.tar.gz）"
