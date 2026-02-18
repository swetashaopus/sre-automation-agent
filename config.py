"""
SRE Automation Agent - Configuration Module

Handles loading and managing configuration for the SRE automation agent.
"""

import os
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv


class Config:
    """Configuration manager for the SRE automation agent."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to YAML configuration file. If None, uses default config.
        """
        load_dotenv()
        
        self.config_file = config_file or os.getenv('SRE_CONFIG_FILE', 'config.yaml')
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            'monitoring': {
                'interval_seconds': 60,
                'cpu_threshold': 80,
                'memory_threshold': 85,
                'disk_threshold': 90
            },
            'alerts': {
                'enabled': True,
                'methods': ['log']
            },
            'logging': {
                'level': 'INFO',
                'file': 'sre_agent.log'
            },
            'services': []
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        # Merge with defaults
                        for key, value in file_config.items():
                            if isinstance(value, dict) and key in default_config:
                                default_config[key].update(value)
                            else:
                                default_config[key] = value
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_file}: {e}")
        
        return default_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation, e.g., 'monitoring.interval_seconds')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
