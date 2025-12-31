import threading
import time
import schedule
import os
from helper.config import ConfigManager
from dep.logger import get_logger

logger = get_logger(__name__)

# --- JOB FUNCTION & CONFIG ---
def heartbeat():
    logger.info("[scheduler][heartbeat] scheduler is running")

def clean_old_files(days=30):

    logger.info("[scheduler][clean_old_files] start...")

    download_dir = ConfigManager().config["download_dir"]
    cutoff_time = 60 * 60 * 24 * days # sec
    now = time.time()
    rm_list = []

    for dirpath, dirnames, filenames in os.walk(download_dir):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            access_time = os.stat(file_path).st_atime
            if now - access_time > cutoff_time:
                rm_list.append(file)
                os.remove(file_path)

    if len(rm_list) == 0:
        msg = "All files are survived"
    else:
        msg = "remove list: " + str(rm_list)

    logger.info(f"[scheduler][clean_old_files] {msg}")

# Format: (time interval, unit, job)
JOBS_CONFIG = [(30, "seconds", heartbeat), (60, "seconds", clean_old_files)]    

# --- CORE SCHEDULE LOGIC ---
def _run_threaded(job_func):
    """啟動新執行緒執行任務"""
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def _scheduler_loop():
    """排程器的主要迴圈，持續檢查是否有任務需要執行"""
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    """
    初始化並啟動排程服務
    這會啟動一個 Daemon Thread 在背景運行，不會阻塞主程式
    """

    for interval, unit, job_func in JOBS_CONFIG:
        scheduler_unit = getattr(schedule.every(interval), unit)
        scheduler_unit.do(_run_threaded, job_func)

    scheduler_thread = threading.Thread(target=_scheduler_loop, name="Scheduler_Loop")
    scheduler_thread.daemon = True  # 設定為 Daemon，主程式結束時它會自動結束
    scheduler_thread.start()
    logger.info("✅ Scheduler service started in background.")

if __name__ == "__main__":
    start_scheduler()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("exit!")
        exit(0)
