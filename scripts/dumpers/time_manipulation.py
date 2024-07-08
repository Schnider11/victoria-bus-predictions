from datetime import datetime, timedelta


def normalize_time(start_time, start_date):
    """
    Input:
        start_date: str in the format `YYYYMMDD`
        start_time: str in the format `HH:MM:SS`
    """
    hours = int(start_time[:2])
    if hours >= 24:
        delta = timedelta(hours=hours % 23)

        hours = hours - (hours % 23)
        start_time = "{:02d}".format(hours) + start_time[2:]

        new_date = datetime.strptime(
            start_date + start_time,
            "%Y%m%d%H:%M:%S"
        )
        new_date = new_date + delta

        new_date_str = new_date.strftime("%Y%m%d%H:%M:%S")

        start_date = new_date_str[:8]
        start_time = new_date_str[8:]

    return start_time, start_date

def fix_stop_times_on_first_stop(trip_id, curr_stop, start_time, start_date):
    """
        Functional description:

        If arrival.time or departure.time are undefined, which can be
        checked using not ss.HasField("arrival") for example, then if
        it is the first stop, set it to be the same time as the start
        time but convert it to a timestamp. Do the same for the departure
        on the first stop.

        If the departure time of the last stop is 0, is that a problem?
        Methinks not
    """
    arrival_time = int(str(curr_stop.arrival.time))
    departure_time = int(str(curr_stop.departure.time))

    if arrival_time == 0 and departure_time == 0:
        curr_stop_sequence = int(str(curr_stop.stop_sequence))
        if curr_stop_sequence == 1: # First stop
            departure_time = int(
                datetime.timestamp(
                    datetime.strptime(
                        start_time + "," + start_date, "%H:%M:%S,%Y%m%d"
                    )
                )
            )
            print("Changed departure time for trip {}".format(trip_id))
        else:
            raise ValueError(
                "Data for {} is corrupted".format(trip_id)
            )
    
    return arrival_time, departure_time