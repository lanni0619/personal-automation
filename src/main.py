import time
from watchdog.observers import Observer

# utils
import utils.helper.os_tooler as os_tooler
from utils.watchdog.handler import MoverHandler
import utils.scheduler.index as scheduler

if __name__ == "__main__":

    source_dir = r"C:\Users\parktron\Downloads"
    foldername_map_path = {
        "image": r"C:\Users\parktron\Downloads\images",
        "app": r"C:\Users\parktron\Downloads\apps",
        "archiver": r"C:\Users\parktron\Downloads\archiver",
        "pdf": r"C:\Users\parktron\Downloads\pdf",
        "excel": r"C:\Users\parktron\Downloads\excel",
    }

    # Start scheduler
    scheduler.start_scheduler()

    # Prepare Watchdog
    os_tooler.make_folder(foldername_map_path)
    event_handler = MoverHandler(source_dir, foldername_map_path)

    # Start Watchdog
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
