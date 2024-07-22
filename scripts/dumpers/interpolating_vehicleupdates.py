import math
import os
import sys
from datetime import datetime
from typing import Union

import pandas as pd
import tzlocal
from dataclasses_and_helpers import *
from stops_timedelta import *

stops = {}

def write_file_header(file):
    file.write("trip_id,vehicle_id,start_time,start_date," +
        "route_id,direction_id,stop_sequence," +
        "arrival_timestamp,arrival_delay," +
        "departure_timestamp,departure_delay," +
        "stop_id\n")

def load_stops():
    stops_dtypes = {
        "stop_id": object,
        "stop_name": object,
        "stop_lat": np.float32,
        "stop_lon": np.float32,
        "wheelchair_boarding": object,
        "stop_code": object,
    }

    df_stops = pd.read_csv(
        "/home/jack/uvic/honors-proj/metadata/20240609_200205/stops.txt",
        dtype=stops_dtypes
    )

    for row in df_stops.itertuples(index=False):
        stops[row.stop_id] = GCS(lat=np.float32(row.stop_lat), lon=np.float32(row.stop_lon))


def main():
    args = sys.argv[1:]

    if len(args) != 2:
        raise ValueError("Parameters are `X x` where X is the path to the "
            + "file, x is the input file path to be interpolated")

    build_trip_timedeltas(*args)
    load_stops()
    process_vehicleupdates_file(*args)

if __name__ == "__main__":
    main()