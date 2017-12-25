from notifyme import app, db
from .models import Competition, Registration, RSSParser
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import ConflictingIdError
from mailer.models import create_msg, send_msg
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
                try:
                    open_time = new_event.open_time
                    if open_time is not None:
                        dt_mod = dt - datetime.timedelta(minutes=10)
                        sched.add_job(lambda: send_emails(event), 'cron',
                                      id=event, year=dt_mod.year,
                                      month=dt_mod.month,
                                      day=dt_mod.day,
                                      hour=dt_mod.hour,
                                      minute=dt_mod.minute,
                                      second=dt_mod.second)
                except ConflictingIdError:
                    pass
                except OverflowError:
                    pass
        db.session.commit()


def send_emails(event):
    with app.app_context():
        comp = db.session.query(Competition).\
                    filter(Competition.name == event).one()
        comp_site = comp.name
        s = db.session.query(Registration).\
            filter(Registration.comp_name == event).all()
        for reg in s:
            msg = create_msg(event, comp_site, [reg.email])
            send_msg(msg)
        db.session.delete(comp)
        db.session.commit()
        # need to also pop off the competition from the database

sched.add_job(populate_db, 'interval', id="populate_db", minutes=1)
