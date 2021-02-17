from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.cron import CronTrigger
import urllib.request

sched = BlockingScheduler()

# @sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/1')
def scheduled_job():
    url = "https://linebothook.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

trigger = OrTrigger([
   CronTrigger(hour='10-20', minute='*/20')
])

sched.add_job(scheduled_job, trigger)
sched.start()