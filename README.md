# 音悦台 / 灵动音乐

一个个人使用的 macOS Apple Music 桌面歌词原型。启动后会在屏幕顶部显示一个置顶、可拖动的“灵动岛”歌词胶囊，读取 Music.app 当前歌曲信息，从 LRCLIB 匹配同步歌词并按播放进度显示当前句。

## 运行要求

- macOS
- 系统自带 Music.app / Apple Music
- 终端可运行 `osascript`
- 网络可访问 `https://lrclib.net`

第一版不需要 npm、pnpm、yarn、Swift 或 Xcode。

## 启动

```bash
osascript -l JavaScript lyric-island.jxa
```

首次读取 Music.app 时，macOS 可能会请求允许终端或脚本控制 Music.app。请在系统弹窗里允许；如果拒绝过，可以到“系统设置 > 隐私与安全性 > 自动化”里重新允许。

## 轻量检查

```bash
scripts/smoke-test.sh
```

这个检查只验证脚本内置解析逻辑和本地 JSON 格式，不会启动悬浮窗口。

## 人工修正

胶囊右侧的“修正”按钮会打开人工补充面板。可以：

- 修改歌名、歌手、专辑、时长后重新搜索 LRCLIB。
- 选择搜索候选并保存。
- 手动输入 LRCLIB ID 并保存。
- 粘贴 LRC 文本并保存。

保存后的映射会写入 `data/overrides.json`。脚本优先使用 Apple Music 曲目 ID；取不到时使用规范化后的歌手、歌名和时长作为 key。

## 数据和隐私

脚本只把查询歌词所需的歌曲名、歌手、专辑和时长发送到 LRCLIB，不读取 Apple Music 官方歌词，也不要求 Apple ID、密码或 token。
