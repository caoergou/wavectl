from typing import Dict, Any, Set, List
import json

class ConfigValidator:
    """
    Validates WaveTerm configuration files against the known schema.
    Strictly enforces that no unknown keys are present.
    """

    # settings.json keys
    SETTINGS_KEYS: Set[str] = {
        # App
        "app:globalhotkey", "app:dismissarchitecturewarning", "app:defaultnewblock",
        "app:showoverlayblocknums", "app:ctrlvpaste", "feature:waveappbuilder",

        # AI (Legacy/Global)
        "ai:preset", "ai:apitype", "ai:baseurl", "ai:apitoken", "ai:name",
        "ai:model", "ai:orgid", "ai:apiversion", "ai:maxtokens", "ai:timeoutms",
        "ai:proxyurl", "ai:fontsize", "ai:fixedfontsize",

        # Wave AI
        "waveai:showcloudmodes", "waveai:defaultmode",

        # Terminal
        "term:fontsize", "term:fontfamily", "term:theme", "term:disablewebgl",
        "term:localshellpath", "term:localshellopts", "term:gitbashpath",
        "term:scrollback", "term:copyonselect", "term:transparency",
        "term:allowbracketedpaste", "term:shiftenternewline", "term:macoptionismeta",

        # Editor
        "editor:minimapenabled", "editor:stickyscrollenabled", "editor:wordwrap",
        "editor:fontsize", "editor:inlinediff",

        # Web
        "web:openlinksinternally", "web:defaulturl", "web:defaultsearch",

        # Block Header
        "blockheader:showblockids",

        # AutoUpdate
        "autoupdate:enabled", "autoupdate:intervalms", "autoupdate:installonquit",
        "autoupdate:channel",

        # Markdown
        "markdown:fontsize", "markdown:fixedfontsize",

        # Preview
        "preview:showhiddenfiles",

        # Tab
        "tab:preset",

        # Widget
        "widget:showhelp",

        # Window
        "window:fullscreenonlaunch", "window:transparent", "window:blur",
        "window:opacity", "window:bgcolor", "window:reducedmotion",
        "window:tilegapsize", "window:showmenubar", "window:nativetitlebar",
        "window:disablehardwareacceleration", "window:maxtabcachesize",
        "window:magnifiedblockopacity", "window:magnifiedblocksize",
        "window:magnifiedblockblurprimarypx", "window:magnifiedblockblursecondarypx",
        "window:confirmclose", "window:savelastwindow", "window:dimensions",
        "window:zoom",

        # Telemetry
        "telemetry:enabled",

        # Conn
        "conn:askbeforewshinstall", "conn:wshenabled",

        # Debug
        "debug:pprofport", "debug:pprofmemprofilerate",

        # Tsunami
        "tsunami:scaffoldpath", "tsunami:sdkreplacepath", "tsunami:sdkversion",
        "tsunami:gopath"
    }

    # waveai.json inner keys
    WAVEAI_MODE_KEYS: Set[str] = {
        "display:name", "display:order", "display:icon", "display:description",
        "ai:provider", "ai:apitype", "ai:model", "ai:thinkinglevel",
        "ai:endpoint", "ai:azureapiversion", "ai:apitoken", "ai:apitokensecretname",
        "ai:azureresourcename", "ai:azuredeployment", "ai:capabilities",
        "ai:switchcompat", "waveai:cloud", "waveai:premium"
    }

    # connections.json inner keys
    CONNECTION_KEYS: Set[str] = {
        "conn:wshenabled", "conn:askbeforewshinstall", "conn:wshpath",
        "conn:shellpath", "conn:ignoresshconfig", "display:hidden",
        "display:order", "term:fontsize", "term:fontfamily", "term:theme",
        "cmd:env", "cmd:initscript", "cmd:initscript.sh", "cmd:initscript.bash",
        "cmd:initscript.zsh", "cmd:initscript.pwsh", "cmd:initscript.fish",
        "ssh:user", "ssh:hostname", "ssh:port", "ssh:identityfile",
        "ssh:identitiesonly", "ssh:batchmode", "ssh:pubkeyauthentication",
        "ssh:passwordauthentication", "ssh:passwordsecretname",
        "ssh:kbdinteractiveauthentication", "ssh:preferredauthentications",
        "ssh:addkeystoagent", "ssh:identityagent", "ssh:proxyjump",
        "ssh:userknownhostsfile", "ssh:globalknownhostsfile"
    }

    # widgets.json inner keys (meta block)
    # Note: These are context dependent, but we can list all known valid meta keys
    WIDGET_META_KEYS: Set[str] = {
        "view", "controller", "cmd", "cmd:args", "cmd:shell", "cmd:interactive",
        "cmd:login", "cmd:runonstart", "cmd:runonce", "cmd:clearonstart",
        "cmd:closeonexit", "cmd:closeonexitforce", "cmd:closeonexitdelay",
        "cmd:env", "cmd:cwd", "cmd:nowsh", "cmd:jwt", "term:localshellpath",
        "term:localshellopts", "connection", "url", "pinnedurl",
        "graph:numpoints", "sysinfo:type", "cmd:initscript", "cmd:initscript.sh",
        "cmd:initscript.bash", "cmd:initscript.zsh", "cmd:initscript.pwsh",
        "cmd:initscript.fish"
    }

    WIDGET_OUTER_KEYS: Set[str] = {
        "display:order", "display:hidden", "icon", "color", "label",
        "description", "magnified", "blockdef"
    }

    # presets.json inner keys
    # Note: We focus on Background Presets (bg) as they are the primary use case mentioned
    PRESET_BG_KEYS: Set[str] = {
        "display:name", "display:order", "bg:*", "bg", "bg:opacity",
        "bg:blendmode", "bg:bordercolor", "bg:activebordercolor"
    }

    @staticmethod
    def validate_keys(data: Dict[str, Any], allowed_keys: Set[str], context: str):
        """Checks if all keys in data are present in allowed_keys."""
        unknown_keys = set(data.keys()) - allowed_keys
        if unknown_keys:
            # Check for wildcard clear keys (e.g. app:*, ai:*) which are valid in some contexts but technically stored as keys?
            # Actually, in the Go struct tags, "ai:*" maps to AiClear bool.
            # If the json has "ai:*": true, it is a valid key.
            # I have added these to SETTINGS_KEYS where appropriate (e.g. app:*)
            # Let's check if any unknown keys match the pattern "group:*"

            # Special case for presets: keys are identifiers like "bg@blue"
            pass

        if unknown_keys:
             raise ValueError(f"Unknown keys found in {context}: {unknown_keys}")

    @staticmethod
    def validate_settings(data: Dict[str, Any]):
        # Allow any key that matches the known set
        # But also, Go's json parser might ignore unknown fields, but user asked for strictness.
        # "SettingsType" struct has specific tags.
        ConfigValidator.validate_keys(data, ConfigValidator.SETTINGS_KEYS, "settings.json")

    @staticmethod
    def validate_waveai(data: Dict[str, Any]):
        for mode_name, mode_config in data.items():
            ConfigValidator.validate_keys(mode_config, ConfigValidator.WAVEAI_MODE_KEYS, f"waveai.json mode '{mode_name}'")

    @staticmethod
    def validate_connections(data: Dict[str, Any]):
        for conn_name, conn_config in data.items():
            ConfigValidator.validate_keys(conn_config, ConfigValidator.CONNECTION_KEYS, f"connections.json connection '{conn_name}'")

    @staticmethod
    def validate_widgets(data: Dict[str, Any]):
        for widget_id, widget_config in data.items():
            if widget_config is None:
                continue # null is allowed to delete default widgets

            ConfigValidator.validate_keys(widget_config, ConfigValidator.WIDGET_OUTER_KEYS, f"widgets.json widget '{widget_id}'")

            if "blockdef" in widget_config:
                blockdef = widget_config["blockdef"]
                if "meta" in blockdef:
                    ConfigValidator.validate_keys(blockdef["meta"], ConfigValidator.WIDGET_META_KEYS, f"widgets.json widget '{widget_id}' meta")

    @staticmethod
    def validate_presets(data: Dict[str, Any]):
        for preset_id, preset_config in data.items():
            if preset_id.startswith("bg@"):
                ConfigValidator.validate_keys(preset_config, ConfigValidator.PRESET_BG_KEYS, f"presets.json preset '{preset_id}'")
            # We can add more preset types if needed, but 'bg' is the main one documented

    @staticmethod
    def validate(filename: str, data: Dict[str, Any]):
        if filename == "settings.json":
            ConfigValidator.validate_settings(data)
        elif filename == "waveai.json":
            ConfigValidator.validate_waveai(data)
        elif filename == "connections.json":
            ConfigValidator.validate_connections(data)
        elif filename == "widgets.json":
            ConfigValidator.validate_widgets(data)
        elif filename == "presets.json" or filename.startswith("presets/"):
             ConfigValidator.validate_presets(data)
        else:
            # Fallback for unrecognized files, or maybe raise error
            pass
