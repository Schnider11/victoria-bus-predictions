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



def interpolate_in_motion(trip_id: str, vu: VehicleUpdate):
    t = abstract_trips[trip_id]

    # We would only call this if the bus is in transit to stop `x`, so
    # we need to get how long it would take to get from trip `x - 1`
    # to trip `x`
    sec = get_timedeltas(
        trip_id,
        vu.current_stop_sequence - 1,
        vu.current_stop_sequence
    )

    p = vu.pos.to_point()
    
    # Get stop information
    s1 = stops[t.stops[vu.current_stop_sequence - 2].stop_id].to_point()
    s2 = stops[t.stops[vu.current_stop_sequence - 1].stop_id].to_point()
    
    if trip_id == "10093896:5676830:5690445" and vu.current_stop_sequence == 14:
        print("interpolate_in_motion")
        print(vu.pos, stops[t.stops[vu.current_stop_sequence - 2].stop_id], stops[t.stops[vu.current_stop_sequence - 1].stop_id])
        print(p, p.distance(s1), p.distance(s2), s1, s2)

    v1 = Vector(p.x - s1.x, p.y - s1.y)
    v2 = Vector(s2.x - s1.x, s2.y - s1.y)

    p = v1.proj(v2)
    # if trip_id == "10093896:5676830:5690445" and vu.current_stop_sequence == 14:
    #     print("projection", p)

    p = Point(p.x, p.y) + s1

    path_len = s1.distance(s2)

    try:
        dist_back = sec * (p.distance(s1) / path_len)
        dist_forw = sec * (p.distance(s2) / path_len)
    except ZeroDivisionError:
        print(trip_id, vu.current_stop_sequence)
        print(t.stops)
        print(t.stops[vu.current_stop_sequence - 2].stop_id, t.stops[vu.current_stop_sequence - 1].stop_id)
        print(stops[t.stops[vu.current_stop_sequence - 2].stop_id].to_point(), stops[t.stops[vu.current_stop_sequence - 1].stop_id].to_point())
        print(vu.pos, stops[t.stops[vu.current_stop_sequence - 2].stop_id], stops[t.stops[vu.current_stop_sequence - 1].stop_id])
        return None, None

    # if trip_id == "10093896:5676830:5690445" and vu.current_stop_sequence == 14:
    #     print("interpolate_in_motion")
    #     print(path_len, p, p.distance(s1), p.distance(s2))
    #     print(sec, dist_back, dist_forw, path_len, s1, s2)
    #     print(t.stops[vu.current_stop_sequence - 2].stop_id, t.stops[vu.current_stop_sequence - 1].stop_id)
    #     print(stops[t.stops[vu.current_stop_sequence - 2].stop_id], stops[t.stops[vu.current_stop_sequence - 1].stop_id])
    #     print(stops[t.stops[vu.current_stop_sequence - 2].stop_id].to_point(), stops[t.stops[vu.current_stop_sequence - 1].stop_id].to_point())
    
    if p.distance(s1) > path_len or p.distance(s2) > path_len:
        # The shortest distance line is behind the first stop or after the
        # second stop, then ignore this interpolation
        return None, None

    return dist_back, dist_forw

def interpolate_stop(
    trip_id: str,
    desired_stop_sequence: int,
    vu: Union[VehicleUpdate, InterpolatedStop]
):
    if isinstance(vu, InterpolatedStop):
        return get_timedeltas(trip_id, vu.stop_sequence, desired_stop_sequence)
    else:
        start, end = interpolate_in_motion(trip_id, vu)

        if start is None or end is None:
            return None
        
        interpolation = None
        if desired_stop_sequence <= vu.current_stop_sequence - 1:
            interpolation = start + get_timedeltas(
                trip_id,
                vu.current_stop_sequence - 1,
                desired_stop_sequence
            )
        elif desired_stop_sequence >= vu.current_stop_sequence:
            interpolation = -1 * end + get_timedeltas(
                trip_id,
                vu.current_stop_sequence,
                desired_stop_sequence
            )

        if trip_id == "10093896:5676830:5690445" and desired_stop_sequence == 15:
            print("interpolate_stop", start, end, interpolation)

        return interpolation

def interpolate_vehicleupdates(vu: VehicleUpdates):
    try:
        t = abstract_trips[vu.trip_id]
        n_stops = len(t.stops)
        trip_timedeltas[vu.trip_id]
    except KeyError:
        # If we don't have the trip, it was probably invalid
        return None

    stopped: dict[int, VehicleUpdate] = {}
    in_motion: dict[int, VehicleUpdate] = {}

    for u in vu.updates:
        if u.current_status == "STOPPED_AT":
            if u.current_stop_sequence in stopped:
                stopped[u.current_stop_sequence].arrival_timestamp = min(
                    stopped[u.current_stop_sequence].arrival_timestamp,
                    u.timestamp
                )

                stopped[u.current_stop_sequence].departure_timestamp = max(
                    stopped[u.current_stop_sequence].departure_timestamp,
                    u.timestamp
                )
            else:
                stopped[u.current_stop_sequence] = create_interpolated_from_vehicleupdate(u)
        else:
            # Both INCOMING_AT and IN_TRANSIT_TO basically mean the same
            # thing, so handle them similarly
            if u.current_stop_sequence in in_motion:
                in_motion[u.current_stop_sequence].append(u)
            else:
                in_motion[u.current_stop_sequence] = [u]

    at = create_base_actual_trip(vu)
    interpolated_stops: dict[int, InterpolatedStop] = {}
    for i in range(1, n_stops + 1):
        # Any more than three stops before or after would give an
        # unreasonable/bad interpolation
        curr_stop = create_base_interpolated_stop(
            i,
            t.stops[i - 1].stop_id
        )
        arr, dep = False, False
        # for j in range(1, 4):
        for j in range(1, 3):
            # Use the left one to interpolate arrival time and the right to
            # interpolate departure time. If only one of the two exist, then
            # update both timestamps to be the same. If we **already** have a
            # stopped record of the stop, then just update one of the
            # timestamps so that it remains consistent, i.e., arrival <=
            # departure.

            # The +1 is here in case we caught the base on route
            # to our desired stop.
            if ((i + 1 - j) in in_motion or (i - j) in stopped) and not arr:
                est = None
                timestamp = None

                if (i + 1 - j) in in_motion:
                    # Use the interpolation method to estimate and
                    # add up timedeltas
                    est = interpolate_stop(vu.trip_id, i, in_motion[i + 1 - j][0])
                    timestamp = in_motion[i + 1 - j][0].timestamp
                
                if (i - j) in stopped and est is None:
                    # Add up timedeltas as the interpolation
                    est = interpolate_stop(vu.trip_id, i, stopped[i - j])
                    timestamp = stopped[i - j].arrival_timestamp

                if est is not None:
                    # This timestamp needs to account for when there are multiple
                    # stops that share the same minute, then we should be adding
                    # that difference to this timestamp!
                    abstract_timestamp = get_subminute_timedelta(vu.trip_id, i - 1) + \
                        t.stops[i - 1].timestamp

                    if curr_stop.departure_timestamp == np.inf:
                        curr_stop.departure_timestamp = timestamp + est
                        curr_stop.departure_delay = curr_stop.departure_timestamp - abstract_timestamp

                    # Verify that the numbers make sense
                    if timestamp + est <= curr_stop.departure_timestamp:
                        curr_stop.arrival_timestamp = round(timestamp + est)
                        curr_stop.arrival_delay = round(curr_stop.arrival_timestamp - abstract_timestamp)

                        # if vu.trip_id == "10070488:5680783:5691013":
                        #     print(vu.trip_id, "arr", i, abstract_timestamp, curr_stop.arrival_timestamp, curr_stop.arrival_delay)

                        arr = True

            if ((i + j) in in_motion or (i + j) in stopped) and not dep:
                est = None
                timestamp = None

                if (i + j) in in_motion:
                    # Use the interpolation method to estimate and
                    # add up timedeltas
                    est = interpolate_stop(vu.trip_id, i, in_motion[i + j][0])
                    timestamp = in_motion[i + j][0].timestamp
                
                if (i + j) in stopped and est is None:
                    # Add up timedeltas as the interpolation
                    est = interpolate_stop(vu.trip_id, i, stopped[i + j])
                    timestamp = stopped[i + j].departure_timestamp

                if est is not None:
                    # This timestamp needs to account for when there are multiple
                    # stops that share the same minute, then we should be adding
                    # that difference to this timestamp!
                    abstract_timestamp = get_subminute_timedelta(vu.trip_id, i - 1) + \
                        t.stops[i - 1].timestamp

                    if curr_stop.arrival_timestamp == np.inf:
                        curr_stop.arrival_timestamp = round(timestamp + est)
                        curr_stop.arrival_delay = round(curr_stop.arrival_timestamp - abstract_timestamp)

                    # Verify that the numbers make sense
                    if timestamp + est >= curr_stop.arrival_timestamp:
                        curr_stop.departure_timestamp = round(timestamp + est)
                        curr_stop.departure_delay = round(curr_stop.departure_timestamp - abstract_timestamp)
                        
                        # if vu.trip_id == "10070488:5680783:5691013":
                        #     print(vu.trip_id, "dep", i, abstract_timestamp, curr_stop.arrival_timestamp, curr_stop.arrival_delay)

                        dep = True

            if i > 1 and i < n_stops:
                if arr or dep:
                    interpolated_stops[i] = curr_stop
                    break
            else:
                # First and last stop are edge cases
                if i == 1:
                    if dep:
                        interpolated_stops[i] = curr_stop
                        break
                elif i == n_stops:
                    if arr:
                        interpolated_stops[i] = curr_stop
                        break

        if i not in interpolated_stops:
            print("Could not find stop {}. Bad trip {}, ignoring".format(i, vu.trip_id))
            # print(in_motion)
            return None

    process_actual_trip(at, list(interpolated_stops.values()))
    return at

def process_vehicleupdates_file(
    path,
    vu_file_name
):
    vu_dtypes = {
        "trip_id": object,
        "vehicle_id": object,
        "start_time": object,
        "start_date": object,
        "schedule_relationship": object,
        "route_id": object,
        "direction_id": object,
        "speed": object,
        "current_stop_sequence": object,
        "current_status": object,
        "timestamp": object,
        "congestion_level": object,
        "stop_id": object
    }

    df_vu = pd.read_csv(path + "/" + vu_file_name, dtype=vu_dtypes)
    output_file_name = "interpolated" + vu_file_name.split("_")[1]
    output_file = open(path + "/" + output_file_name, "w")
    write_file_header(output_file)

    start_idx = -1
    curr_trip = None

    for (i, row) in enumerate(df_vu.itertuples(index=False)):
        t = create_base_vehicle_updates(row)

        if curr_trip is None:
            curr_trip = create_base_vehicle_updates(row)
            start_idx = i            
        elif t != curr_trip:
            curr_trip = t
            t = process_vehicle_updates(df_vu[start_idx:i])
            t = interpolate_vehicleupdates(t)
            if t is not None:
                output_file.write(t.to_csv())
            start_idx = i

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