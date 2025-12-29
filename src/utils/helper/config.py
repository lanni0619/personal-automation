import json

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.config = None

    def load_config(self):
        try:
            with open(self.config_path, "r") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found: {self.config_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in: {self.config_path}")

    def get_config(self):
        if self.config is None:
            self.load_config()
        return self.config