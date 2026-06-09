#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="${1:-0.2.0-beta.1}"
BUILD_NUMBER="${BUILD_NUMBER:-1}"
PRODUCT_NAME="灵动音乐"
BUNDLE_ID="com.lingdongmusic.desktop"
BUILD_DIR="$ROOT/build/release"
DIST_DIR="$ROOT/dist"
APP_PATH="$BUILD_DIR/$PRODUCT_NAME.app"
STAGING_DIR="$BUILD_DIR/dmg"
DMG_NAME="$PRODUCT_NAME-v$VERSION-macos-universal.dmg"
DMG_PATH="$DIST_DIR/$DMG_NAME"
PLIST="$APP_PATH/Contents/Info.plist"
RESOURCES="$APP_PATH/Contents/Resources"
ICON_PATH="$ROOT/assets/AppIcon.icns"

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR" "$DIST_DIR"
rm -f "$DMG_PATH" "$DMG_PATH.sha256"

"$ROOT/scripts/smoke-test.sh"

osacompile -l JavaScript -o "$APP_PATH" "$ROOT/lyric-island.jxa"
cp "$ICON_PATH" "$RESOURCES/AppIcon.icns"

set_plist_string() {
  /usr/libexec/PlistBuddy -c "Set :$1 $2" "$PLIST" >/dev/null 2>&1 ||
    /usr/libexec/PlistBuddy -c "Add :$1 string $2" "$PLIST"
}

set_plist_bool() {
  /usr/libexec/PlistBuddy -c "Set :$1 $2" "$PLIST" >/dev/null 2>&1 ||
    /usr/libexec/PlistBuddy -c "Add :$1 bool $2" "$PLIST"
}

set_plist_string CFBundleIdentifier "$BUNDLE_ID"
set_plist_string CFBundleName "$PRODUCT_NAME"
set_plist_string CFBundleDisplayName "$PRODUCT_NAME"
set_plist_string CFBundleShortVersionString "$VERSION"
set_plist_string CFBundleVersion "$BUILD_NUMBER"
set_plist_string CFBundleIconFile "AppIcon.icns"
set_plist_string LSMinimumSystemVersion "13.0"
set_plist_string NSAppleEventsUsageDescription "灵动音乐需要读取 Music.app 的当前歌曲、播放状态和播放进度，以显示同步歌词。"
set_plist_bool LSUIElement true

for key in \
  CFBundleIconName \
  LSMinimumSystemVersionByArchitecture \
  NSAppleMusicUsageDescription \
  NSCalendarsUsageDescription \
  NSCameraUsageDescription \
  NSContactsUsageDescription \
  NSHomeKitUsageDescription \
  NSMicrophoneUsageDescription \
  NSPhotoLibraryUsageDescription \
  NSRemindersUsageDescription \
  NSSiriUsageDescription \
  NSSystemAdministrationUsageDescription; do
  /usr/libexec/PlistBuddy -c "Delete :$key" "$PLIST" >/dev/null 2>&1 || true
done

rm -f "$RESOURCES/applet.icns"

codesign --force --deep --sign - --identifier "$BUNDLE_ID" "$APP_PATH"
codesign --verify --deep --strict --verbose=2 "$APP_PATH"

COMPILED_TEST_DATA="$BUILD_DIR/compiled-test-data"
LINGDONG_MUSIC_DATA_DIR="$COMPILED_TEST_DATA" \
  osascript "$RESOURCES/Scripts/main.scpt" --self-test

actual_bundle_id="$(/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" "$PLIST")"
actual_minimum="$(/usr/libexec/PlistBuddy -c "Print :LSMinimumSystemVersion" "$PLIST")"
actual_architectures="$(lipo -archs "$APP_PATH/Contents/MacOS/applet")"
[[ "$actual_bundle_id" == "$BUNDLE_ID" ]]
[[ "$actual_minimum" == "13.0" ]]
[[ "$actual_architectures" == *"x86_64"* ]]
[[ "$actual_architectures" == *"arm64"* ]]
[[ -f "$RESOURCES/AppIcon.icns" ]]
[[ ! -e "$APP_PATH/Contents/Resources/data" ]]

mkdir -p "$STAGING_DIR"
cp -R "$APP_PATH" "$STAGING_DIR/$PRODUCT_NAME.app"
cp "$ROOT/docs/首次使用说明.txt" "$STAGING_DIR/首次使用说明.txt"
ln -s /Applications "$STAGING_DIR/Applications"

hdiutil create \
  -volname "$PRODUCT_NAME" \
  -srcfolder "$STAGING_DIR" \
  -ov \
  -format UDZO \
  "$DMG_PATH" >/dev/null
hdiutil verify "$DMG_PATH" >/dev/null

(
  cd "$DIST_DIR"
  shasum -a 256 "$DMG_NAME" > "$DMG_NAME.sha256"
)

echo ""
echo "Release artifacts:"
echo "  $DMG_PATH"
echo "  $DMG_PATH.sha256"
