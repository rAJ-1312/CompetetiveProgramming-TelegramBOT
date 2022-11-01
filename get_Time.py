from datetime import datetime,timedelta
from dateutil import tz



def returnTime():
    s = datetime.now().replace(microsecond=0).isoformat()

    current = datetime.today()
    after_a_week = current + timedelta(days=7)

    e = after_a_week.replace(microsecond=0).isoformat()

    # print(s)
    # print(e)
    return s,e

returnTime()

def find_remaining_time(a):
    diff = a - datetime.now()
    t = str(diff)
    return t.split('.')[0]



def startTimeLocal(iso_utc_time):

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = datetime.strptime(iso_utc_time, '%Y-%m-%dT%H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone).isoformat()
    return local.split('+')[0]
    