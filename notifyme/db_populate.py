from notifyme import app, db
from .models import Competition, RSSParser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import ConflictingIdError
import datetime
import logging
logging.basicConfig()
sched = BackgroundScheduler()


def populate_db():
    r = RSSParser()
    events = r.get_events()
    with app.app_context():
        strings = map(lambda x: x[0], db.session.query(Competition.name).all())
        for event in events.keys():
            if event not in strings:
                if events[event][1] is not None:
                    if events[event][1] != 'open':
                        dt = datetime.datetime.strptime(events[event][1],
                                                        '%Y-%m-%dT%XZ')
                    else:
                        dt = datetime.datetime.min
                    new_event = Competition(name=event,
                                            website=events[event][0],
                                            open_time=dt)
                else:
                    new_event = Competition(name=event,
                                            website=events[event][0],
                                            open_time=None)
                db.session.add(new_event)
                # create cronjob
                try:
                    sched.add_job(send_emails, 'cron', id="send to " + event, hour=1)
                except ConflictingIdError:
                    pass
        db.session.commit()


def send_emails():
    pass

sched.add_job(populate_db, 'interval', id="populate_db", seconds=10)
