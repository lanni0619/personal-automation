import time
from watchdog.observers import Observer

# utils
import helper.os_tooler as os_tooler
import dep.scheduler as scheduler
from helper.config import ConfigManager
from dep.watchdog_handler import MoverHandler
from dep.logger import get_logger

config = None
logger = get_logger(__name__)

if __name__ == "__main__":
    # Load config
    config = ConfigManager().config
    source_dir = config["download_dir"]
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

    logger.info("🚀 Watchdog listening...: " + source_dir)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.error("Watchdog stop to listen...")
    except Exception as e:
        logger.error("🛑 Unexpected error", e)

    observer.join()
