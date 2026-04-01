import json
import os

class ConfigManager:
    @staticmethod
    def load_config(env="qa"):
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r') as f:
            full_config = json.load(f)
            if env not in full_config:
                raise ValueError(f"Environment '{env}' not found in configuration.")
            return full_config[env]
