import os

import pandas as pd
from dataclasses_and_helpers import *

abstract_trips = {}
trip_timedeltas = {}

def convert_and_assign_to_timedeltas(t: AbstractTrip):
    # So first, get the abstract trips to measure how long it would
    # take from one stop to another. If a stop is in its own minute, then
    # it takes approximately an entire minute to get to it. If not, then
    # it takes (60 / however many stops that are in the same minute).
    # Under that assumption, build a stop delta and use that to estimate
    # if a bus is in transition then how far ago was it at the earlier
    # stop + knowing where the bus is in relation to the road between the
    # two stops!

    # Assuming that the trips file is well-formatted and that the
    # first stop we see for a trip is the first one, if we see that
    # the first stop is not actually the first stop, then print the
    # trip ID, assume that it is corrupted, and discard the trip.
    # The problem could be originating from BC Transit's website
    # where the trips files are being updated

    if not(t.len() > 0 and t.stops[0].stop_sequence == "1"):
        print("Trip {} is invalid".format(t.trip_id))
        return

    timedeltas = []

    # Use count to keep track of how many stops share the same minute and then
    # allocate the deltas appropriately
    count = 1

    for i in range(t.len() - 1):
        if t.stops[i].timestamp == t.stops[i + 1].timestamp:
            count += 1
            if i < t.len() - 2:
                continue

        for j in range(count):
            if j < count - 1:
                timedeltas.append((60 // count, j))
            elif j == count - 1:
                timedeltas.append((t.stops[i + 1].timestamp - (t.stops[i].timestamp + 60 * (count - 1) // count), j))
        count = 1

    # for j in range(count):
    #     if j == 0:
    #         timedeltas.append((curr_timestamp - prev_timestamp, j))
    #     else:
    #         timedeltas.append((60 // count, j))
    
    trip_timedeltas[t.trip_id] = timedeltas

def build_trip_timedeltas(path, vu_file_name):
    date = vu_file_name.split("_")[1].split(".")[0]
    abstract_trips_file = "trips_{}_abstract_no_dups.csv".format(date)
    if not os.path.isfile(path + "/" + abstract_trips_file):
        raise FileNotFoundError("Abstract trips file not found, make "
            + "sure that {} is in the same folder ".format(abstract_trips_file)
            + "as the vehicleupdates file")
    
    at_dtypes = {
        "trip_id": object,
        "start_time": object,
        "start_date": object,
        "route_id": object,
        "direction_id": object,
        "stop_sequence": object,
        "arrival_timestamp": np.int64,
        "arrival_delay": np.int16,
        "departure_timestamp": np.int64,
        "departure_delay": np.int16,
        "stop_id": object
    }

    df_trips = pd.read_csv(path + "/" + abstract_trips_file, dtype=at_dtypes)
    
    start_idx = -1
    curr_trip = None

    for (i, row) in enumerate(df_trips.itertuples(index=False)):
        t = create_base_abstract_trip(row)

        if curr_trip is None:
            curr_trip = create_base_abstract_trip(row)
            start_idx = i            
        elif t != curr_trip:
            curr_trip = t
            t = process_abstract_trip(df_trips[start_idx:i])
            abstract_trips[t.trip_id] = t

            convert_and_assign_to_timedeltas(t)
            start_idx = i

def get_timedeltas(
    trip_id: str,
    start_stop_sequence: np.int8,
    end_stop_sequence: np.int8
):
    td = 0
    if start_stop_sequence < end_stop_sequence:
        for i in range(start_stop_sequence - 1, end_stop_sequence - 1):
            td += trip_timedeltas[trip_id][i][0]
    else:
        for i in range(end_stop_sequence - 1, start_stop_sequence - 1):
            td -= trip_timedeltas[trip_id][i][0]
    return td

def get_subminute_timedelta(
    trip_id: str,
    stop_sequence: np.int8,
):
    td = 0

    # Subtract one because we want timedeltas to the current stop
    stop_sequence -= 1

    while(stop_sequence > 0):
        # Different stop, can't use the timedelta to check reliably because it
        # could be that two sequences of stops have the same timedeltas
        # resulting in something like [(20, 0), (20, 1), (20, 2), (20, 0),
        # *(20, 1)*, (20, 2)], which won't allow us to know that by just
        # looking at the timedeltas
        if trip_timedeltas[trip_id][stop_sequence][0] >= 60:
            return td
        elif stop_sequence + 1 >= len(trip_timedeltas[trip_id]) or \
            trip_timedeltas[trip_id][stop_sequence][1] > trip_timedeltas[trip_id][stop_sequence + 1][1]:
            return td

        td += trip_timedeltas[trip_id][stop_sequence][0]
        stop_sequence -= 1

    return td