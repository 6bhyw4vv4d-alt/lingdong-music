# 灵动音乐

一个轻量的 macOS Apple Music 桌面歌词工具。启动后会在屏幕顶部显示一个置顶、可拖动的“灵动岛”歌词胶囊，读取 Music.app 当前歌曲信息，从 LRCLIB 匹配同步歌词并按播放进度显示当前句。

## 安装内测版

- macOS 13 或更高版本
- 系统自带 Music.app / Apple Music
- 网络可访问 `https://lrclib.net`

1. 从 GitHub Releases 下载 `Lingdong-Music-v0.2.0-beta.2-macos-universal.dmg`。
2. 打开 DMG，将 `灵动音乐.app` 拖入 Applications。
3. 在“应用程序”中右键 `灵动音乐.app`，选择“打开”。
4. 首次使用时，允许灵动音乐控制 Music.app。

当前内测版没有 Developer ID 签名和 Apple 公证，因此第一次必须使用右键打开。完成一次确认后，后续可以正常双击启动。

## 日常使用

- 顶部歌词胶囊可以直接拖动。
- 点击胶囊右侧的“修正”，可重新匹配歌词、粘贴 LRC、用“早 / 准 / 晚”调整歌词快慢和修改样式。
- 外文歌词如果带有相同时间戳的中文行，会在原歌词下面自动显示中文。
- 粘贴双语 LRC 时，把外文和中文放在同一个时间戳即可，例如 `[00:10.00]Hello` 和 `[00:10.00]你好`。
- 打开修正面板后可用快捷键调整，每次 `0.5` 秒并自动保存：`⌥[` 提前、`⌥0` 恢复同步、`⌥]` 延后。
- 点击菜单栏音符图标，可以显示/隐藏歌词、打开权限设置、查看版本或退出。

## 本地开发

直接运行源码：

```bash
osascript -l JavaScript lyric-island.jxa
```

也可以使用启动脚本：

```bash
./run.sh
```

运行检查：

```bash
./scripts/smoke-test.sh
```

构建通用架构 App 和 DMG：

```bash
./scripts/build-release.sh
```

构建产物会写入 `dist/`，默认文件名为：

- `灵动音乐-v0.2.0-beta.2-macos-universal.dmg`
- `灵动音乐-v0.2.0-beta.2-macos-universal.dmg.sha256`

## 数据和隐私

设置和人工歌词保存在：

```text
~/Library/Application Support/灵动音乐/
```

从源码首次启动时，如果用户数据目录为空，程序会自动迁移项目 `data/` 下已有的设置和人工歌词。发布包不会包含开发者个人数据。

灵动音乐只把查询歌词所需的歌曲名、歌手、专辑和时长发送到 LRCLIB，不读取 Apple Music 官方歌词，也不要求 Apple ID、密码或 token。
