import os
import locale
import sys
from .config_manager import ConfigManager

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
        "Select Action:": "选择操作：",
        "Add New AI Mode": "添加新 AI 模式",
        "Global AI Settings": "全局 AI 设置",
        "Select Global AI Setting:": "选择全局 AI 设置：",
        "Default AI Mode": "默认 AI 模式",
        "Show Cloud Modes": "显示云端模式",
        "AI Proxy URL": "AI 代理 URL",
        "AI Font Size": "AI 字体大小",
        "AI Fixed Font Size": "AI 固定字体大小",
        "No AI modes found. Please add a mode first.": "未找到 AI 模式。请先添加一个模式。",
        " [Current Default]": " [当前默认]",
        "Skip / Keep Current": "跳过 / 保持当前",
        "Select Default AI Mode:": "选择默认 AI 模式：",
        "Set '{default_mode}' as the default AI mode.": "已将 '{default_mode}' 设置为默认 AI 模式。",
        "Show Built-in Cloud Modes (OpenAI, Anthropic, etc.)?": "显示内置云端模式 (OpenAI, Anthropic 等)？",
        "Hide Cloud Modes": "隐藏云端模式",
        "Keep Current ({val})": "保持当前 ({val})",
        "Updated show cloud modes setting.": "已更新显示云端模式设置。",
        "Enter Proxy URL (empty to remove):": "输入代理 URL (留空以移除)：",
        "Removed proxy URL.": "已移除代理 URL。",
        "Updated proxy URL.": "已更新代理 URL。",
        "Enter AI Font Size (int, 0/empty to default):": "输入 AI 字体大小 (整数，0/留空为默认)：",
        "Reset AI font size to default.": "已重置 AI 字体大小为默认。",
        "Updated AI font size.": "已更新 AI 字体大小。",
        "Invalid integer.": "无效的整数。",
        "Enter AI Fixed Font Size (int, 0/empty to default):": "输入 AI 固定字体大小 (整数，0/留空为默认)：",
        "Reset AI fixed font size to default.": "已重置 AI 固定字体大小为默认。",
        "Updated AI fixed font size.": "已更新 AI 固定字体大小。",
        "OpenRouter": "OpenRouter",
        "Google (Gemini)": "Google (Gemini)",
        "Azure OpenAI": "Azure OpenAI",
        "Azure OpenAI (Legacy)": "Azure OpenAI (旧版)",
        "Custom / Local (Ollama, etc.)": "自定义 / 本地 (Ollama 等)",
        "Enter Display Name:": "输入显示名称：",
        "Enter Model Name:": "输入模型名称：",
        "Enter Model Name (e.g. anthropic/claude-sonnet-4.5):": "输入模型名称 (例如 anthropic/claude-sonnet-4.5)：",
        "Note: OpenAI provider uses the secret named OPENAI_KEY.": "注意：OpenAI 提供商使用名为 OPENAI_KEY 的密钥。",
        "Do you have this secret set?": "您是否已设置此密钥？",
        "Enter your OpenAI API Key (to display setup command):": "输入您的 OpenAI API 密钥 (用于显示设置命令)：",
        "Please run the following command to set your secret:": "请运行以下命令来设置您的密钥：",
        "(You can do this after finishing this configuration)": "(您可以在完成此配置后执行此操作)",
        "Note: OpenRouter provider uses the secret named OPENROUTER_KEY.": "注意：OpenRouter 提供商使用名为 OPENROUTER_KEY 的密钥。",
        "Enter your OpenRouter API Key (to display setup command):": "输入您的 OpenRouter API 密钥 (用于显示设置命令)：",
        "Note: Google provider uses the secret named GOOGLE_AI_KEY.": "注意：Google 提供商使用名为 GOOGLE_AI_KEY 的密钥。",
        "Enter your Google AI API Key (to display setup command):": "输入您的 Google AI API 密钥 (用于显示设置命令)：",
        "Enter Azure Resource Name:": "输入 Azure 资源名称：",
        "Note: Azure provider uses the secret named AZURE_OPENAI_KEY.": "注意：Azure 提供商使用名为 AZURE_OPENAI_KEY 的密钥。",
        "Enter your Azure OpenAI API Key (to display setup command):": "输入您的 Azure OpenAI API 密钥 (用于显示设置命令)：",
        "Enter Azure Deployment Name:": "输入 Azure 部署名称：",
        "Enter API Version (optional, default: 2025-04-01-preview):": "输入 API 版本 (可选，默认：2025-04-01-preview)：",
        "Note: For Azure Legacy, you should store your API key in a secret.": "注意：对于旧版 Azure，您应该将 API 密钥存储在密钥中。",
        "Enter Secret Name for API Key (default: AZURE_OPENAI_KEY):": "输入 API 密钥的密钥名称 (默认：AZURE_OPENAI_KEY)：",
        "Do you have the secret '{secret_name}' set?": "您是否已设置密钥 '{secret_name}'？",
        "Enter your Azure API Key (to display setup command):": "输入您的 Azure API 密钥 (用于显示设置命令)：",
        "Note: Custom/BYOK models do not require telemetry enabled.": "注意：自定义/BYOK 模型不需要启用遥测。",
        "Select API Type:": "选择 API 类型：",
        "Enter Endpoint URL (e.g. http://localhost:11434/v1/chat/completions):": "输入端点 URL (例如 http://localhost:11434/v1/chat/completions)：",
        "Do you want to use a secret for the API Token?": "您想为 API 令牌使用密钥吗？",
        "Enter Secret Name:": "输入密钥名称：",
        "Remember to run: wsh secret set {secret_name}=<your-key>": "记得运行：wsh secret set {secret_name}=<您的密钥>",
        "Enter API Token (or 'not-needed'/'ollama'):": "输入 API 令牌 (或 'not-needed'/'ollama')：",
        "Enter Icon Name (FontAwesome, e.g. robot, sparkles, brain) [optional]:": "输入图标名称 (FontAwesome，例如 robot, sparkles, brain) [可选]：",
        "Select Thinking Level (optional):": "选择思考层级 (可选)：",
        "Quick (Low)": "快捷 (低)",
        "Balanced (Medium)": "平衡 (中)",
        "Deep (High)": "深度 (高)",
        "Enter a unique ID for this mode (key in json):": "输入此模式的唯一 ID (json 中的键)：",
        "Successfully saved AI mode '{display_name}' to waveai.json": "成功将 AI 模式 '{display_name}' 保存到 waveai.json",
        "Select Capabilities supported by this model:": "选择此模型支持的能力：",
        "Tools (Read/Write files, run commands)": "工具 (读/写文件，运行命令)",
        "Images (Vision)": "图像 (视觉)",
        "PDFs (Read PDF content)": "PDF (读取 PDF 内容)",
        "Listing (Directory Listing)": "列表 (目录列表)",
        "Do you want to store the SSH password in the secret store?": "您想在密钥库中存储 SSH 密码吗？",
        "Enter Secret Name for Password:": "输入密码的密钥名称：",
        "Enter SSH Password (to display setup command):": "输入 SSH 密码 (用于显示设置命令)：",
        "Set Global Terminal Theme": "设置全局终端主题",
        "Set Terminal Font Size": "设置终端字体大小",
        "Set Terminal Font Family": "设置终端字体族",
        "Set Default Tab Theme": "设置默认标签页主题",
        "Toggle Help Widget": "切换帮助组件",
        "Create Background Preset": "创建背景预设",
        "Successfully set font size to {size}": "成功将字体大小设置为 {size}",
        "Enter Font Family (e.g. Fira Code):": "输入字体族 (例如 Fira Code)：",
        "Successfully set font family to '{family}'": "成功将字体族设置为 '{family}'",
        "Enter Custom Key...": "输入自定义键...",
        "Enter Tab Preset Key (e.g. bg@myred):": "输入标签页预设键 (例如 bg@myred)：",
        "Successfully set default tab preset to '{preset_key}'": "成功将默认标签页预设设置为 '{preset_key}'",
        "Help Widget Visibility:": "帮助组件可见性：",
        "Show": "显示",
        "Hide": "隐藏",
        "Help widget enabled.": "帮助组件已启用。",
        "Help widget disabled.": "帮助组件已禁用。",
        "Preset Name (e.g. My Red):": "预设名称 (例如 My Red)：",
        "Preset Key (e.g. myred):": "预设键 (例如 myred)：",
        "Background Type:": "背景类型：",
        "Solid Color": "纯色",
        "Gradient": "渐变",
        "Image": "图像",
        "Color (hex/rgba, e.g. #ff0000):": "颜色 (十六进制/rgba，例如 #ff0000)：",
        "Gradient CSS (e.g. linear-gradient(...)):": "渐变 CSS (例如 linear-gradient(...))：",
        "Image Path (absolute or starting with ~):": "图像路径 (绝对路径或以 ~ 开头)：",
        "Opacity (0.0 - 1.0, default 0.5):": "不透明度 (0.0 - 1.0，默认 0.5)：",
        "Successfully created background preset '{name}' ({full_key})": "成功创建背景预设 '{name}' ({full_key})",
        "Rainbow": "彩虹",
        "Green": "绿色",
        "Blue": "蓝色",
        "Red": "红色",
        "Ocean Depths": "深海",
        "Aqua Horizon": "水色地平线",
        "Sunset": "日落",
        "Enchanted Forest": "魔法森林",
        "Twilight Mist": "暮色薄雾",
        "Dusk Horizon": "黄昏地平线",
        "Tropical Radiance": "热带光辉",
        "Twilight Ember": "暮色余晖",
        "Cosmic Tide": "宇宙潮汐",
        "Configure General Settings": "配置常规设置",
        "Select Setting to Configure:": "选择要配置的设置：",
        "Telemetry Enabled": "启用遥测",
        "Terminal Scrollback": "终端回滚行数",
        "Copy on Select": "选择即复制",
        "Confirm Window Close": "确认关闭窗口",
        "Save Last Window State": "保存上次窗口状态",
        "Show Block Numbers Overlay": "显示区块编号叠加层",
        "Shift+Enter for Newline": "Shift+Enter 换行",
        "Show Hidden Files in Preview": "在预览中显示隐藏文件",
        "Use Native Title Bar": "使用原生标题栏",
        "Use Option as Meta (MacOS)": "使用 Option 键作为 Meta 键 (MacOS)",
        "Terminal Transparency": "终端透明度",
        "Disable Hardware Acceleration": "禁用硬件加速",
        "Allow Bracketed Paste": "允许括号粘贴",
        "Editor Word Wrap": "编辑器自动换行",
        "Default Web Home URL": "默认网页主页 URL",
        "Enable Telemetry?": "启用遥测？",
        "Updated telemetry setting.": "已更新遥测设置。",
        "Enter Scrollback Lines (-1 for default, max 50000):": "输入回滚行数 (-1 为默认，最大 50000)：",
        "Value too high, setting to 50000": "值过高，设置为 50000",
        "Updated scrollback setting.": "已更新回滚设置。",
        "Enable Copy on Select?": "启用选择即复制？",
        "Updated copy on select setting.": "已更新选择即复制设置。",
        "Confirm before closing window?": "关闭窗口前确认？",
        "Updated confirm close setting.": "已更新确认关闭设置。",
        "Save last window state?": "保存上次窗口状态？",
        "Updated save last window setting.": "已更新保存窗口状态设置。",
        "Show block numbers overlay?": "显示区块编号叠加层？",
        "Updated overlay block nums setting.": "已更新区块编号叠加层设置。",
        "Use Shift+Enter for newline?": "使用 Shift+Enter 换行？",
        "Updated Shift+Enter setting.": "已更新 Shift+Enter 设置。",
        "Show hidden files in preview?": "在预览中显示隐藏文件？",
        "Updated show hidden files setting.": "已更新显示隐藏文件设置。",
        "Use native title bar?": "使用原生标题栏？",
        "Updated native title bar setting.": "已更新原生标题栏设置。",
        "Value must be between 0.0 and 1.0": "值必须在 0.0 到 1.0 之间",
        "Updated transparency setting.": "已更新透明度设置。",
        "Invalid float.": "无效的浮点数。",
        "Disable Hardware Acceleration?": "禁用硬件加速？",
        "Updated hardware acceleration setting.": "已更新硬件加速设置。",
        "Allow Bracketed Paste?": "允许括号粘贴？",
        "Updated bracketed paste setting.": "已更新括号粘贴设置。",
        "Enable Editor Word Wrap?": "启用编辑器自动换行？",
        "Updated editor word wrap setting.": "已更新编辑器自动换行设置。",
        "Enter Default Web Home URL (empty to remove):": "输入默认网页主页 URL (留空以移除)：",
        "Removed default web home URL.": "已移除默认网页主页 URL。",
        "Updated default web home URL.": "已更新默认网页主页 URL。",
        "General Settings": "常规设置",
        "Select Language:": "选择语言：",
        "Language": "语言",
        "Language updated.": "语言已更新。",
        "None": "无",
        "Default": "默认",
        "Enter Max Tokens (int, 0/empty for default):": "输入最大 Token 数 (整数，0/留空为默认)：",
        "Updated max tokens.": "已更新最大 Token 数。",
        "Terminal Font Size": "终端字体大小",
        "Enter Terminal Font Size (int, 0/empty to default):": "输入终端字体大小 (整数，0/留空为默认)：",
        "Updated terminal font size.": "已更新终端字体大小。",
        "Terminal Font Family": "终端字体族",
        "Enter Terminal Font Family (empty to default):": "输入终端字体族 (留空为默认)：",
        "Updated terminal font family.": "已更新终端字体族。",
    }
}

_CURRENT_LOCALE = None

def get_language():
    """Get the current language preference."""
    cm = ConfigManager()
    config = cm.load_wavectl_config()
    lang = config.get("lang")
    if lang:
        return lang

    # Fallback to environment variable
    env_lang = os.environ.get("WAVECTL_LANG")
    if env_lang:
        return env_lang

    # Fallback to system locale
    try:
        # Priority 2: System Locale
        # getlocale() is safer than getdefaultlocale() which is deprecated
        sys_locale, _ = locale.getlocale()
        if sys_locale:
            return sys_locale
    except:
        pass

    return "en_US"

def set_language(lang):
    """Set the language preference and save it."""
    global _CURRENT_LOCALE
    _CURRENT_LOCALE = lang
    cm = ConfigManager()
    config = cm.load_wavectl_config()
    config["lang"] = lang
    cm.save_wavectl_config(config)

def _get_system_locale():
    return get_language()

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
        try:
            return translation.format(**kwargs)
        except (KeyError, ValueError):
            return translation
    return translation
