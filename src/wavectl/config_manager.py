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

        self.settings_file = self.config_dir / "settings.json"
        self.waveai_file = self.config_dir / "waveai.json"

        # Ensure directories exist
        self.ensure_config_dirs()

    def ensure_config_dirs(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)

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

    def load_waveai(self) -> Dict[str, Any]:
        return self._read_json(self.waveai_file)

    def save_waveai(self, data: Dict[str, Any]):
        self._write_json(self.waveai_file, data)

    def update_waveai_mode(self, mode_key: str, mode_data: Dict[str, Any]):
        """Update or add a single AI mode in waveai.json."""
        modes = self.load_waveai()
        modes[mode_key] = mode_data
        self.save_waveai(modes)

    def set_config_value(self, key: str, value: Any):
        """Set a value in the main settings.json file."""
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)
