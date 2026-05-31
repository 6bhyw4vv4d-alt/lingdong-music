#!/bin/zsh
set -eu

cd "$(dirname "$0")/.."

osascript -l JavaScript lyric-island.jxa --self-test
osascript -l JavaScript -e 'ObjC.import("Foundation"); var p = "data/overrides.json"; var s = $.NSString.stringWithContentsOfFileEncodingError($(p), $.NSUTF8StringEncoding, null); JSON.parse(ObjC.unwrap(s)); console.log(p + ": OK")'
