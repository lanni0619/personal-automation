import os
import json
import threading

class ConfigManager:
    _instance = None
    _lock = threading.Lock()  # 保證多執行緒環境下的單例安全

    def __new__(cls, config_filename="config.json"):
        if not cls._instance:
            with cls._lock:  # 確保只有一個執行緒能初始化實例
                if not cls._instance:
                    cls._instance = super(ConfigManager, cls).__new__(cls)
                    cls._instance._init(config_filename)
        return cls._instance

    def _init(self, config_filename):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "../../"))

        self.config_path = os.path.join(project_root, config_filename)
        self.config = None
        self.load_config()

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