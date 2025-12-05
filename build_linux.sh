#!/usr/bin/env bash
# Build single-file executable for Linux using PyInstaller.
# Prerequisites: python3, python3-venv, pip, ffmpeg available in PATH.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="VideoClipper_v1.3.2_linux"
DIST_PATH="$ROOT/dist/$APP_NAME"
VENV_PATH="$ROOT/.venv-linux"

echo "==> Checking python3 ..."
command -v python3 >/dev/null 2>&1 || { echo "python3 not found"; exit 1; }

echo "==> Checking ffmpeg ..."
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found in PATH"; exit 1; }

if [ ! -d "$VENV_PATH" ]; then
  echo "==> Creating virtual env ..."
  python3 -m venv "$VENV_PATH"
fi

echo "==> Activating virtual env ..."
# shellcheck disable=SC1090
source "$VENV_PATH/bin/activate"

echo "==> Upgrading pip and installing requirements ..."
pip install --upgrade pip
pip install -r "$ROOT/requirements.txt"

echo "==> Building with PyInstaller ..."
pyinstaller \
  --noconfirm \
  --onefile \
  --name "$APP_NAME" \
  "$ROOT/video_clipper.py"

echo "==> Build finished."
echo "Output: $DIST_PATH"
echo "Make sure the file is executable: chmod +x \"$DIST_PATH\""

