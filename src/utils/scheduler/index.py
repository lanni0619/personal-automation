import threading
import time
import schedule


# --- JOB FUNCTION & CONFIG ---
def example_job():
    print("I'm working on a scheduled task!")

def clean_old_files(days=30):
    pass

# Format: (time interval, unit, job)
JOBS_CONFIG = [(3, "seconds", example_job)]

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
    print("✅ Scheduler service started in background.")

if __name__ == "__main__":
    start_scheduler()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("exit!")
        exit(0)
