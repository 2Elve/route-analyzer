import time
import schedule
from threading import Thread
from typing import Callable

class BackgroundScheduler:
    def __init__(self):
        self.job_func = None
    
    def schedule_hourly_job(self, job_func: Callable):
        """ This function executes the program each hour """
        self.job_func = job_func
        schedule.every().hour.do(self._run_job)
        
        thread = Thread(target=self._run_scheduler)
        thread.daemon = True
        thread.start()
    
    def _run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def _run_job(self):
        try:
            self.job_func()
        except Exception as e:
            print(f"Error en ejecución programada: {e}")