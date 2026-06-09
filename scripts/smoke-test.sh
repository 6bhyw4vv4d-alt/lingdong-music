#!/bin/zsh
set -eu

cd "$(dirname "$0")/.."

TEST_DATA_DIR="$(mktemp -d /private/tmp/lingdong-music-smoke.XXXXXX)"
trap 'rm -rf "$TEST_DATA_DIR"' EXIT

LINGDONG_MUSIC_DATA_DIR="$TEST_DATA_DIR" osascript -l JavaScript lyric-island.jxa --self-test
osascript -l JavaScript -e 'ObjC.import("Foundation"); var p = "data/overrides.json"; var s = $.NSString.stringWithContentsOfFileEncodingError($(p), $.NSUTF8StringEncoding, null); JSON.parse(ObjC.unwrap(s)); console.log(p + ": OK")'
osascript -l JavaScript -e 'ObjC.import("Foundation"); var p = "data/settings.json"; var s = $.NSString.stringWithContentsOfFileEncodingError($(p), $.NSUTF8StringEncoding, null); JSON.parse(ObjC.unwrap(s)); console.log(p + ": OK")'
