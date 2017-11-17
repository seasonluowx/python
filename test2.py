from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

def get_GMT_time():
    now = datetime.now()
    stamp = mktime(now.timetuple())
    return format_date_time(stamp)

print(get_GMT_time())