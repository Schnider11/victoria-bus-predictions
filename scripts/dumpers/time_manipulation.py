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
