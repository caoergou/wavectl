# WaveCtl: WaveTerm Configuration Manager

[English](#english) | [中文](#chinese)

<a name="english"></a>

`wavectl` is a lightweight, interactive CLI tool designed to simplify the configuration of [Wave Terminal](https://www.waveterm.dev/). It provides a unified interface to manage all aspects of WaveTerm (v0.9.0+), from AI models and SSH connections to themes and widgets.

## Features

*   **Comprehensive Configuration:** Manage all WaveTerm settings including:
    *   **AI Settings:** Configure models (OpenAI, Claude, etc.) and API keys.
    *   **SSH Connections:** Simplify SSH setup and key management.
    *   **Appearance:** Interactive theme selection and customization.
    *   **Widgets:** Configure and arrange terminal widgets.
*   **Interactive Design:** A user-friendly Terminal User Interface (TUI) guides you through configurations, eliminating the need to manually edit complex JSON files.
*   **Version Aware:** Built specifically for the modern WaveTerm configuration structure.

## Installation

The easiest way to install `wavectl` is using [uv](https://github.com/astral-sh/uv).

```bash
# Install directly from the repository
uv tool install git+https://github.com/caoergou/wavectl.git
```

This will install `wavectl` as a standalone tool available in your shell.

## Quick Start

Once installed, simply run:

```bash
wavectl
```

Use the arrow keys to navigate the menu and `Enter` to select options.

## Language Support

`wavectl` automatically detects your system language. To force a specific language, set the `WAVECTL_LANG` environment variable:

```bash
WAVECTL_LANG=zh_CN wavectl
```

## Development

If you want to contribute to `wavectl`, we recommend using `uv` for dependency management.

```bash
# Clone the repository
git clone https://github.com/caoergou/wavectl.git
cd wavectl

# Sync dependencies
uv sync

# Run the application
uv run wavectl
```

---

<a name="chinese"></a>

# WaveCtl: WaveTerm 配置管理工具

`wavectl` 是一个轻量级的交互式命令行工具，旨在简化 [Wave Terminal](https://www.waveterm.dev/) 的配置过程。它提供了一个统一的界面来管理 WaveTerm (v0.9.0+) 的各个方面，从 AI 模型和 SSH 连接到主题和挂件。

## 功能特性

*   **全面的配置管理：** 管理所有 WaveTerm 设置，包括：
    *   **AI 设置：** 配置模型（OpenAI, Claude 等）和 API 密钥。
    *   **SSH 连接：** 简化 SSH 设置和密钥管理。
    *   **外观：** 交互式主题选择和自定义。
    *   **挂件：** 配置和排列终端挂件。
*   **交互式设计：** 用户友好的终端用户界面 (TUI) 指引您完成配置，无需手动编辑复杂的 JSON 文件。
*   **版本感知：** 专为现代 WaveTerm 配置结构构建。

## 安装

安装 `wavectl` 最简单的方法是使用 [uv](https://github.com/astral-sh/uv)。

```bash
# 直接从仓库安装
uv tool install git+https://github.com/caoergou/wavectl.git
```

这将把 `wavectl` 安装为一个独立的工具，您可以在 shell 中直接使用。

## 快速开始

安装完成后，只需运行：

```bash
wavectl
```

使用方向键浏览菜单，按 `Enter` 键选择选项。

## 语言支持

`wavectl` 会自动检测您的系统语言。如果需要强制使用特定语言，请设置 `WAVECTL_LANG` 环境变量：

```bash
WAVECTL_LANG=zh_CN wavectl
```

## 开发指南

如果您想为 `wavectl` 做出贡献，我们建议使用 `uv` 进行依赖管理。

```bash
# 克隆仓库
git clone https://github.com/caoergou/wavectl.git
cd wavectl

# 同步依赖
uv sync

# 运行应用
uv run wavectl
```
