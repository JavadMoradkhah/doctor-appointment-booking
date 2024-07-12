from datetime import time


def time_to_seconds(time: time) -> int:
    return time.hour * 3600 + time.minute * 60 + time.second


def calc_time_diff(time1: time, time2: time):
    return time_to_seconds(time1) - time_to_seconds(time2)
