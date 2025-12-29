import time
from watchdog.observers import Observer

# utils
import utils.helper.os_tooler as os_tooler
import utils.scheduler.index as scheduler
from utils.helper.config import ConfigManager
from utils.watchdog.handler import MoverHandler

config = None

if __name__ == "__main__":
    # Load config
    config = ConfigManager().get_config()
    source_dir = config["watchdog"]["source_dir"]
    foldername_map_path = config["watchdog"]["foldername_map_path"]

    # Start scheduler
    scheduler.start_scheduler()

    # Prepare watchdog
    os_tooler.make_folder(foldername_map_path)
    event_handler = MoverHandler(source_dir, foldername_map_path)

    # Start watchdog
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()

    print("🚀 Watchdog listening...:", source_dir)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Watchdog stop to listen...")
    except Exception as e:
        print("Unexpected error", e)
    observer.join()
