from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def blah():
	print "blah"


sched.add_job(blah, trigger='interval', id="blah", seconds=5)

sched.start()