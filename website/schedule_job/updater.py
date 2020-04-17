from apscheduler.schedulers.background import BackgroundScheduler
from schedule_job import test

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(test.Coding, 'interval', minutes=2)
    scheduler.start()