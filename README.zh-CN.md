# gameboy-color-kusoge

[日本語](README.md) · [English (US)](README.en-US.md) · **简体中文**

**DASH // DUEL** 是一款面向 Game Boy Color 和 ModRetro Chromatic 的原创连打竞速游戏。两名玩家共用一台掌机，进行100米短跑对战。

![体育场](art/stadium.png)
![运动员跑步动画帧](art/runners.png)

## 操作方法

- **START**：开始比赛，或在结果画面再次比赛。
- **玩家1（蓝色）**：交替按方向键的**左、右**。
- **玩家2（红色）**：交替按 **A、B**。
- 按住不放或同时按下两个按键，不会持续加速。
- 两名选手都到达终点后显示结果与各自用时；时间相同则为平局。

## 下载

请前往 [Releases](https://github.com/GOROman/gameboy-color-kusoge/releases/latest) 下载最新测试版 `dash-duel.gbc`，并使用 `SHA256SUMS` 校验文件。本游戏**仅支持 Game Boy Color**，不支持黑白 Game Boy。

仓库中也保留了最初的32 KiB卡带版本：[dist/dash-duel.gbc](dist/dash-duel.gbc)。Release文件根据对应标签的源码构建，可能比此文件更新。

## 构建

安装 GBDK-2020 **4.5.0** 和 Python 3，然后运行：

```sh
GBDK_LCC=/path/to/gbdk/bin/lcc python3 scripts/build.py
```

输出文件：`build/dash-duel.gbc`。

运行真实ROM的模拟器测试：

```sh
python3 -m pip install pyboy==2.7.0 pillow==12.3.0
python3 scripts/test_rom.py build/dash-duel.gbc
```

## CI与自动发布

GitHub Actions 会在推送到 `main` 或提交 Pull Request 时构建并测试游戏。推送 `v*` 标签后，只有构建和模拟器测试全部通过，才会自动创建 GitHub Release，上传ROM、校验文件及游戏截图。

## 源码与美术资源

- `plugins/dash/engine/src/dash.c`：共用的游戏逻辑。
- `scripts/build.py`：将上述源码转换为 `standalone.c`，并使用GBDK构建。
- `plugins/dash/engine/src/dash_assets.h`：图块数据。
- `art/redesign.py`：使用Pillow生成体育场、选手与图块数据；字体使用macOS的Monaco。
- `project.gbsproj`、`project/`、`assets/`、`plugins/`：保留的GB Studio编辑项目。

最初的开发电脑因磁盘空间不足，未能完成GB Studio CLI构建。发布的ROM使用上方已测试的GBDK直接构建流程。

自动测试覆盖启动、开始比赛、拒绝按住加速、平局、玩家1获胜与再次比赛。初始版本已完成卡带写入和回读一致性验证。模拟器测试不能代替实体屏幕、按键和音频验证。

本仓库不包含第三方游戏卡带的提取ROM或存档。许可信息请见 [LICENSE](LICENSE)。
