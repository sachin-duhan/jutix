from pathlib import Path
from typing import Dict, Any
from jutix.config.settings import settings

class ConfigHandler:
    def __init__(self):
        """Initialize config handler using Dynaconf settings"""
        self.settings = settings

    @property
    def config(self) -> Dict[str, Any]:
        """Get current configuration"""
        return {
            "enabled_files": self.settings.enabled_files,
            "exclude_files": self.settings.exclude_files,
            "metrics": self.settings.metrics,
            "percentiles": self.settings.percentiles,
            "output_settings": self.settings.output_settings.to_dict(),
            "log_settings": self.settings.log_settings.to_dict()
        }

    def get_output_settings(self) -> Dict[str, str]:
        """Get output directory settings"""
        return self.settings.output_settings.to_dict()

    def get_log_settings(self) -> Dict[str, Any]:
        """Get logging settings"""
        return self.settings.log_settings.to_dict()

    def update_settings(self, **kwargs):
        """Update settings dynamically"""
        for key, value in kwargs.items():
            self.settings.set(key, value) 