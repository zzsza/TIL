from apscheduler.jobstores.base import JobLookupError
from apscheduler.schedulers.background import BackgroundScheduler
import time


class Scheduler:
    def __init__(self):
        self.sched = BackgroundScheduler()
        self.sched.start()
        self.job_id = ''

    def __del__(self):
        self.shutdown()

    def shutdown(self):
        self.sched.shutdown()

    def kill_scheduler(self, job_id):
        try:
            self.sched.remove_job(job_id)
        except JobLookupError as err:
            print("fail to stop Scheduler: {err}".format(err=err))
            return

    def hello(self, type, job_id):
        print("%s Scheduler process_id[%s] : %d" % (type, job_id, time.localtime().tm_sec))

    def scheduler(self, type, job_id):
        print("{type} Scheduler Start".format(type=type))
        if type == 'interval':
            self.sched.add_job(self.hello, type, seconds=10, id=job_id, args=(type, job_id))
        elif type == 'cron':
            self.sched.add_job(self.hello, type, day_of_week='mon-fri',
                                                 hour='0-23', second='*/2',
                                                 id=job_id, args=(type, job_id))


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.scheduler('cron', "1")
    scheduler.scheduler('interval', "2")

    count = 0
    while True:
        '''
        count 제한할 경우 아래와 같이 사용
        '''
        print("Running main process")
        time.sleep(1)
        count += 1
        if count == 10:
            scheduler.kill_scheduler("1")
            print("Kill cron Scheduler")
        elif count == 15:
            scheduler.kill_scheduler("2")
            print("Kill interval Scheduler")