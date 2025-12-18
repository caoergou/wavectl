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
