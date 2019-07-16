from random import randrange

import datetime

def generate_timings(start, threshold, hours_limit = 23, minutes_limit = 60, next_day_start_barricade = False):
    for iter in range(threshold):
        if next_day_start_barricade:
            barricade = (23 - start.now().hour)
            if hours_limit > barricade:
                bkp_hours_limit = hours_limit
                hours_limit = barricade
                print("Barricade executed: Given - {} : Updated to - {}".format(bkp_hours_limit, hours_limit))
        timing = start + datetime.timedelta(hours=randrange(hours_limit), minutes=randrange(minutes_limit))
        yield timing

def get_string_time(datetime):
    return datetime.strftime("%d/%m/%y %H:%M")