from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

def get_time_long(time1, time2):
    time = (time2 - time1).seconds * 1000 + (time2 - time1).microseconds / 1000
    return time

def get_GMT_time():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)