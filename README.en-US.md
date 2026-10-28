# gameboy-color-kusoge

[日本語](README.md) · **English (US)** · [简体中文](README.zh-CN.md)

**DASH // DUEL** is an original button-mashing sprint game for Game Boy Color and ModRetro Chromatic. Two players share one handheld and race over 100 meters.

![Stadium](art/stadium.png)
![Runner animation frames](art/runners.png)

## How to play

- **START:** start a race or play again from the results screen.
- **Player 1 (blue):** alternate **LEFT and RIGHT** on the D-pad.
- **Player 2 (red):** alternate **A and B**.
- Holding a button or pressing both buttons together will not keep accelerating your runner.
- Both players finish before the results appear. Each runner gets a finish time; equal times produce a tie.

## Download

Get the latest tested ROM from [Releases](https://github.com/GOROman/gameboy-color-kusoge/releases/latest). Download `dash-duel.gbc` and check it against `SHA256SUMS`. This is a **Game Boy Color-only** game, not a monochrome Game Boy game.

The repository also contains [dist/dash-duel.gbc](dist/dash-duel.gbc), the original 32 KiB cartridge build. Release assets are built from their tagged source and may be newer.

## Build

Install GBDK-2020 **4.5.0** and Python 3, then run:

```sh
GBDK_LCC=/path/to/gbdk/bin/lcc python3 scripts/build.py
```

Output: `build/dash-duel.gbc`.

To run the real-ROM gameplay tests:

```sh
python3 -m pip install pyboy==2.7.0 pillow==12.3.0
python3 scripts/test_rom.py build/dash-duel.gbc
```

## CI and releases

GitHub Actions builds and tests pushes to `main` and pull requests. Pushing a `v*` tag additionally publishes the tested ROM, checksums, and a gameplay screenshot as a GitHub Release. The release job runs only after the build and emulator tests pass.

## Source and artwork

- `plugins/dash/engine/src/dash.c`: shared gameplay source.
- `scripts/build.py`: converts that source into `standalone.c` and builds it with GBDK.
- `plugins/dash/engine/src/dash_assets.h`: tile data.
- `art/redesign.py`: generates the stadium, runners, and tile data with Pillow; uses the Monaco font on macOS.
- `project.gbsproj`, `project/`, `assets/`, and `plugins/`: retained GB Studio editing project.

The GB Studio CLI build was not completed because the original development machine ran out of disk space. Distributed ROMs use the tested direct GBDK build above.

Automated tests cover boot, start, held-input rejection, tied finishes, a Player 1 win, and rematches. The original cartridge write and readback matched. Emulator tests do not verify physical display, controls, or audio.

Third-party cartridge dumps and save files are not included. See [LICENSE](LICENSE) for licensing.

## Javelin and shot put

Press SELECT on the idle/results screen to cycle through sprint, javelin, and shot put. START begins. Players take turns: alternate A/B to charge, adjust the angle with LEFT/RIGHT, then press A to throw. Aim near 45 degrees. START advances to the next player; longest distance wins.
