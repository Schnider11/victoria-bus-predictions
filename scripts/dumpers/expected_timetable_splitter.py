import sys
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import tzlocal
from dataclasses_and_helpers import *


def unix_timestamp_to_local(timestamp):
    unix_timestamp = float(str(timestamp))
    local_timezone = tzlocal.get_localzone()
    local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
    return local_time.strftime("%Y-%m-%d_%H:%M:%SZ")

def datetime_to_date(dt: datetime):
    return dt.strftime("%Y%m%d")

def datetime_to_time(dt: datetime):
    return dt.strftime("%H:%M:%S")

def is_in_motion(trip: TripUpdate):
    return trip.stops[0].stop_sequence != "1"

le_trips_dict = {}

def classify_and_write_trip(
    t,
    ae_file,
    le_file,
    im_file
):
    if is_in_motion(t):
        im_file.write(t.to_csv())
    else:
        if t.trip_id not in le_trips_dict:
            le_trips_dict[t.trip_id] = t
        elif le_trips_dict[t.trip_id].fetch_time < t.fetch_time:
            # Save the more recent trip update instead
            le_trips_dict[t.trip_id] = t
            
        ae_file.write(t.to_csv())

def main():
    args = sys.argv[1:]

    if len(args) != 1:
        raise ValueError("Parameter is the input file path to be split into "
            + "an average, a last expected, and an in progress file")

    path = "/".join(args[0].split("/")[:-1])
    base_file_name = args[0].split("/")[-1].split(".")[0]

    ae_file = open(path + "/" + base_file_name + "_actual_expected.csv", "w")
    le_file = open(path + "/" + base_file_name + "_last_expected.csv", "w")
    im_file = open(path + "/" + base_file_name + "_in_motion.csv", "w")

    dtypes = {
        "trip_id": object,
        "fetch_time": object,
        "start_time": object,
        "start_date": object,
        "schedule_relationship": object,
        "route_id": object,
        "direction_id": object,
        "stop_sequence": object,
        "arrival_timestamp": object,
        "arrival_delay": object,
        "departure_timestamp": object,
        "departure_delay": object,
        "stop_id": object,
        "stop_schedule_relationship": object,
    }

    df = pd.read_csv(args[0], dtype=dtypes)

    header = ",".join(list(df.columns)) + "\n"
    for f in [ae_file, le_file, im_file]:
        f.write(header)

    start_idx = -1
    curr_trip = None

    for (i, row) in enumerate(df.itertuples(index=False)):
        t = create_base_trip(row)

        if curr_trip is None:
            curr_trip = create_base_trip(row)
            start_idx = i            
        elif t != curr_trip:
            curr_trip = t

            t = process_trip(df[start_idx:i])
            classify_and_write_trip(
                t,
                ae_file,
                le_file,
                im_file
            )

            start_idx = i

    t = process_trip(df[start_idx:df.size])
    classify_and_write_trip(
        t,
        ae_file,
        le_file,
        im_file
    )    

    for t in le_trips_dict.values():
        le_file.write(t.to_csv())

if __name__ == "__main__":
    main()