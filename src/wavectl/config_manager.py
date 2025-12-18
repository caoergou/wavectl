import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = Path.home() / ".config" / "waveterm"

        self.presets_dir = self.config_dir / "presets"
        self.settings_file = self.config_dir / "settings.json"
        self.connections_file = self.config_dir / "connections.json"
        self.widgets_file = self.config_dir / "widgets.json"

        # Ensure directories exist
        self.ensure_config_dirs()

    def ensure_config_dirs(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.presets_dir.mkdir(parents=True, exist_ok=True)

    def _read_json(self, filepath: Path) -> Dict[str, Any]:
        if not filepath.exists():
            return {}
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _write_json(self, filepath: Path, data: Dict[str, Any]):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_settings(self) -> Dict[str, Any]:
        return self._read_json(self.settings_file)

    def save_settings(self, settings: Dict[str, Any]):
        self._write_json(self.settings_file, settings)

    def load_presets(self, filename: str) -> Dict[str, Any]:
        """Load presets from a specific file in the presets directory."""
        filepath = self.presets_dir / filename
        return self._read_json(filepath)

    def save_presets(self, filename: str, presets: Dict[str, Any]):
        """Save presets to a specific file in the presets directory."""
        filepath = self.presets_dir / filename
        self._write_json(filepath, presets)

    def update_preset(self, filename: str, preset_key: str, preset_data: Dict[str, Any]):
        """Update or add a single preset in the specified file."""
        presets = self.load_presets(filename)
        presets[preset_key] = preset_data
        self.save_presets(filename, presets)

    def set_config_value(self, key: str, value: Any):
        """Set a value in the main settings.json file."""
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)

    def load_connections(self) -> Dict[str, Any]:
        return self._read_json(self.connections_file)

    def save_connections(self, connections: Dict[str, Any]):
        self._write_json(self.connections_file, connections)

    def update_connection(self, key: str, data: Dict[str, Any]):
        connections = self.load_connections()
        connections[key] = data
        self.save_connections(connections)

    def load_widgets(self) -> Dict[str, Any]:
        return self._read_json(self.widgets_file)

    def save_widgets(self, widgets: Dict[str, Any]):
        self._write_json(self.widgets_file, widgets)

    def update_widget(self, key: str, data: Any):
        """Update a widget configuration. set data to None (null) to delete/hide default."""
        widgets = self.load_widgets()
        if data is None:
             # In WaveTerm, setting a default widget key to null hides it.
             # But if we want to 'reset' a custom widget, we might delete key?
             # For overriding defaults: set key to null.
             widgets[key] = None
        else:
             widgets[key] = data
        self.save_widgets(widgets)

    def remove_widget_override(self, key: str):
        """Remove an entry from widgets.json (restoring default behavior if it was an override)."""
        widgets = self.load_widgets()
        if key in widgets:
            del widgets[key]
            self.save_widgets(widgets)
