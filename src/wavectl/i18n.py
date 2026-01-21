import os
import locale
import sys

# Translations Dictionary
TRANSLATIONS = {
    "zh_CN": {
        "Welcome to WaveCtl!": "欢迎使用 WaveCtl！",
        "Manage your WaveTerm configuration with ease.\n": "轻松管理您的 WaveTerm 配置。\n",
        "What would you like to configure?": "您想要配置什么？",
        "AI Settings": "AI 设置",
        "SSH Connections": "SSH 连接",
        "Themes": "主题",
        "Widgets": "小组件",
        "Exit": "退出",
        "Goodbye!": "再见！",
        "{choice} module is under construction.": "{choice} 模块正在建设中。",
        "Configure AI Settings": "配置 AI 设置",
        "Select AI Provider:": "选择 AI 提供商：",
        "Go Back": "返回",
        "Enter Model Name (e.g., gpt-4, gpt-3.5-turbo):": "输入模型名称 (例如 gpt-4, gpt-3.5-turbo)：",
        "Enter OpenAI API Key:": "输入 OpenAI API 密钥：",
        "Enter Anthropic API Key:": "输入 Anthropic API 密钥：",
        "Enter Ollama Model Name (e.g., llama2):": "输入 Ollama 模型名称 (例如 llama2)：",
        "Do you need to specify a custom Base URL? (Default is usually http://localhost:11434/v1)": "您需要指定自定义 Base URL 吗？ (默认为 http://localhost:11434/v1)",
        "Enter Base URL:": "输入 Base URL：",
        "Enter a name for this preset (display name):": "为此预设输入名称 (显示名称)：",
        "Successfully saved AI mode '{preset_name_input}' to ~/.config/waveterm/waveai.json": "成功保存 AI 模式 '{preset_name_input}' 到 ~/.config/waveterm/waveai.json",
        "Do you want to set this as your default AI mode?": "您希望将其设置为默认 AI 模式吗？",
        "Set '{preset_name_input}' (key: {mode_key}) as the default AI mode.": "已将 '{preset_name_input}' (键: {mode_key}) 设置为默认 AI 模式。",
        "Configure SSH Connections": "配置 SSH 连接",
        "What would you like to do?": "您想要做什么？",
        "Add New SSH Connection": "添加新 SSH 连接",
        "Enter Hostname or IP (Required):": "输入主机名或 IP (必填)：",
        "Hostname is required.": "主机名是必填项。",
        "Enter Username:": "输入用户名：",
        "Enter Port:": "输入端口：",
        "Do you use an identity file (private key)?": "您使用身份文件 (私钥) 吗？",
        "Path to private key:": "私钥路径：",
        "Enter a Display Name (Alias) [Optional]:": "输入显示名称 (别名) [可选]：",
        "Successfully saved SSH connection '{connection_key}' to ~/.config/waveterm/connections.json": "成功保存 SSH 连接 '{connection_key}' 到 ~/.config/waveterm/connections.json",
        "Configure Theme": "配置主题",
        "Select a Global Terminal Theme:": "选择全局终端主题：" ,
        "Successfully set global theme to '{choice}' ({theme_value})": "成功设置全局主题为 '{choice}' ({theme_value})",
        "Configure Widgets": "配置小组件",
        "Select active default widgets:": "选择启用的默认小组件：",
        "Successfully updated active widgets.": "成功更新启用的小组件。",
        "Terminal": "终端",
        "Files": "文件",
        "Web": "网页",
        "AI": "AI",
        "Sysinfo": "系统信息",
        "Default Dark": "默认深色",
        "One Dark Pro": "One Dark Pro",
        "Dracula": "Dracula",
        "Monokai": "Monokai",
        "Campbell": "Campbell",
        "Warm Yellow": "暖黄",
        "Rose Pine": "Rose Pine",
        "OpenAI": "OpenAI",
        "Anthropic (Claude)": "Anthropic (Claude)",
        "Ollama (Local)": "Ollama (本地)",
        "Warning: Direct Anthropic support requires an OpenAI compatible endpoint.": "警告：直接支持 Anthropic 需要兼容 OpenAI 的端点。",
        "MacOS Option as Meta": "MacOS Option 键作为 Meta 键",
        "Treat Option key as Meta on MacOS?": "在 MacOS 上将 Option 键视为 Meta 键？",
        "Updated MacOS Option as Meta setting.": "已更新 MacOS Option 键作为 Meta 键的设置。",
        "Enter Model Name:": "输入模型名称：",
    }
}

_CURRENT_LOCALE = None

def _get_system_locale():
    # Priority 1: Environment Variable
    env_lang = os.environ.get("WAVECTL_LANG")
    if env_lang:
        return env_lang

    # Priority 2: System Locale
    try:
        sys_locale, _ = locale.getdefaultlocale()
        if sys_locale:
            return sys_locale
    except:
        pass

    return "en_US"

def setup_i18n():
    global _CURRENT_LOCALE
    _CURRENT_LOCALE = _get_system_locale()

def t(key, **kwargs):
    """
    Translate the string 'key' to the current locale.
    Format the string with kwargs if provided.
    """
    if _CURRENT_LOCALE is None:
        setup_i18n()

    # Determine if we use Chinese
    use_zh = _CURRENT_LOCALE.startswith("zh")

    if use_zh:
        translation = TRANSLATIONS.get("zh_CN", {}).get(key, key)
    else:
        translation = key

    if kwargs:
        return translation.format(**kwargs)
    return translation
