import time
import json
from watchdog.observers import Observer

# utils
import utils.helper.os_tooler as os_tooler
from utils.watchdog.handler import MoverHandler
import utils.scheduler.index as scheduler

config = None

if __name__ == "__main__":

    # Load config
    with open('config.json', 'r') as file:
        config = json.load(file)
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
