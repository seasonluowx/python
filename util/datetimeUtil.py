def get_time_long(time1, time2):
    time = (time2 - time1).seconds * 1000 + (time2 - time1).microseconds / 1000
    return time