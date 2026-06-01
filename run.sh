#!/bin/zsh
set -eu

cd "$(dirname "$0")"
osascript -l JavaScript lyric-island.jxa "$@"
