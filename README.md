# WaveCtl: WaveTerm Configuration Manager

`wavectl` is a lightweight, interactive CLI tool designed to simplify the configuration of [Wave Terminal](https://www.waveterm.dev/). It provides a unified interface to manage all aspects of WaveTerm (v0.9.0+), from AI models and SSH connections to themes and widgets.

## Features

*   **Comprehensive Configuration:** Manage all WaveTerm settings including:
    *   **AI Settings:** Configure models (OpenAI, Claude, etc.) and API keys.
    *   **SSH Connections:** Simplify SSH setup and key management.
    *   **Appearance:** Interactive theme selection and customization.
    *   **Widgets:** Configure and arrange terminal widgets.
*   **Interactive Design:** A user-friendly Terminal User Interface (TUI) guides you through configurations, eliminating the need to manually edit complex JSON files.
*   **Version Aware:** Built specifically for the modern WaveTerm configuration structure.
*   **Extensible:** Designed to easily add support for new WaveTerm features as they are released.

## Installation

```bash
# Clone the repository
git clone https://github.com/caoergou/wavectl.git
cd wavectl

# Install dependencies (requires Python 3.10+)
pip install .
```

## Usage

### Interactive Mode (Recommended)

Run the main command to enter the interactive configuration dashboard:

```bash
wavectl
```

This will launch a TUI where you can navigate through different configuration categories (AI, SSH, Themes, etc.).

## Configuration

`wavectl` reads and writes configurations located in the standard WaveTerm configuration directory (e.g., `~/.config/waveterm/` on Linux/macOS).

## Contributing

Contributions are welcome! Please check the ROADMAP.md for planned features.
