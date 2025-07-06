import time
import schedule
from threading import Thread
from typing import Callable

class BackgroundScheduler:
    def __init__(self):
        self.scheduled_jobs = []
    
    def schedule_hourly_job(
        self, 
        job_func: Callable, 
        *args, 
        **kwargs
    ):
        """ This function executes the program each hour """

        job = schedule.every().minute.do(lambda: job_func(*args, **kwargs))
        self.scheduled_jobs.append(job)
        
        if len(self.scheduled_jobs) == 1:
            thread = Thread(target=self._run_scheduler, daemon=True)
            thread.start()
    
    def _run_scheduler(self):
        """ Execute scheduler on background """
        
        while True:
            schedule.run_pending()
            time.sleep(1)


