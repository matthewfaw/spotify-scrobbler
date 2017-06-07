import time

def unix_timestamp(delta_minutes=0):
    return time.time() + delta_minutes*60
