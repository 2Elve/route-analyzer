import time
import schedule
from threading import Thread
from typing import Callable

class BackgroundScheduler:
    def __init__(self):
        self.job_func = None
        self.job_args = None
        self.job_kwargs = None 
    
    def schedule_hourly_job(
            self, 
            job_func: Callable,
            *args,
            **kwargs
        ):
        """ This function executes the program each hour """
        self.job_func = job_func
        self.job_args = args
        self.job_kwargs = kwargs
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
            self.job_func(*self.job_args, **self.job_kwargs)
        except Exception as e:
            print(f"Error on programed execution: {e}")