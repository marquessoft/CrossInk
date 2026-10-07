---
title: Simulator
nav_order: 15
---

# Development Device Simulator

CrossInk can run in the [CrossInk simulator](https://github.com/uxjulia/crossink-simulator), which renders the e-ink display in an SDL2 window. Use it for quick sanity checks without flashing firmware every time.

## Platform Support

The simulator builds on macOS and Linux. `platformio.ini` takes the SDL2 compiler and linker flags from `sdl2-config`, so no hardcoded SDK paths are needed.

- Linux host builds are configured by `scripts/simulator_host_toolchain.py`, which pins the C dialect for GCC 15+ and links OpenSSL for the simulator's MD5 helper.
- Native Windows is not supported. Use WSL and follow the Linux setup.

## Platform Origin

The simulator environment is specific to CrossInk: the parent project, [CrossPoint Reader](https://github.com/crosspoint-reader/crosspoint-reader), has no `[simulator-*]` env in `platformio.ini`. The pieces the Linux fixes touch come from three different places, so platform fixes have different homes upstream:

- The `[simulator-*]` env, its flags (including the clang-only `-Wno-c++11-narrowing` spelling), and the generated web headers that trigger narrowing all live in this repository and were tested only on macOS with Apple clang.
- The simulator's MD5 helper (`MD5Builder_linux.h` / `MD5Builder_mac.h`) lives in [uxjulia/crossink-simulator](https://github.com/uxjulia/crossink-simulator); Linux builds need `-lssl -lcrypto` because of this, and the clean fix would land there.
- `ricmoo/QRCode` (pinned the same way in CrossPoint Reader) predates C23, where `bool` is a keyword; `scripts/simulator_host_toolchain.py` pins the host C dialect to `gnu17` to work around it. CrossInk does not accept pull requests, so upstream-facing changes should go to CrossPoint Reader or the respective library repos.

## Prerequisites

```sh
# macOS
brew install sdl2

# Linux (Debian/Ubuntu)
sudo apt install libsdl2-dev libssl-dev
```

## Setup

Place EPUB books in `./fs_/books/` relative to the project root. That maps to the SD-card `/books/` path on device.

## Build And Run

```sh
pio run -e simulator
.pio/build/simulator/program
```

Use the X4 Pro environment to enable its touch, frontlight, and Home-key behavior:

```sh
pio run -e x4-pro-simulator -t run_simulator
```

## Keyboard Controls

| Key | Action |
| --- | --- |
| Up / Down | Page back / forward (side buttons) |
| Left / Right | Left / right front buttons |
| Return | Confirm / Select |
| Escape | Back |
| P | Power |
| H | X4 Pro Home key (tap to go Home; hold for 700 ms to toggle the reader menu) |

The `H` mapping is active only in `x4-pro-simulator`.

## Cache Note

On first open of an EPUB, an **Indexing...** popup appears while the section cache is built in `.crosspoint/`.

If rendering looks stale after a code change, delete `./fs_/.crosspoint/` to clear simulator caches.
