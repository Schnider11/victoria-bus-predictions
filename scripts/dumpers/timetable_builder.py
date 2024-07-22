import os
import sys
from datetime import datetime

import proto_enums
from google.transit import gtfs_realtime_pb2
from time_manipulation import *


def write_file_header(file, trip_type):
    """
        Input:
        - trip_type: A character that is either 'e' or 'a' to denote that
            the trip is expected or abstract respectively
    """
    
    if trip_type == "a":
        file.write("trip_id,start_time,start_date," +
            "route_id,direction_id,stop_sequence,arrival_timestamp," +
            "arrival_delay,departure_timestamp,departure_delay,stop_id\n")
    elif trip_type == "e":
        file.write("trip_id,fetch_time,start_time,start_date," +
            "schedule_relationship,route_id,direction_id,stop_sequence," +
            "arrival_timestamp,arrival_delay,departure_timestamp," +
            "departure_delay,stop_id,stop_schedule_relationship\n")

def write_entity_into_file(file, entity, trip_type, fetch_time=None):
    """
        Input:
        - trip_type: A character that is either 'e' or 'a' to denote that
            the trip is expected or abstract respectively
    """
    start_time, start_date = normalize_time(
        str(entity.trip_update.trip.start_time), 
        str(entity.trip_update.trip.start_date)
    )

    for ss in entity.trip_update.stop_time_update:
        try:
            arrival_time, departure_time = fix_stop_times_on_first_stop(
                entity.trip_update.trip.trip_id, ss, start_time, start_date
            )
        except ValueError:
            raise ValueError(
                "Data for {} is corrupted".format(str(entity))
            )

        if trip_type == "a":
            file.write(
                str(entity.trip_update.trip.trip_id) + ","
                + start_time + ","
                + start_date + ","
                + str(entity.trip_update.trip.route_id) + ","
                + str(entity.trip_update.trip.direction_id) + ","
                + str(ss.stop_sequence) + ","
                + str(arrival_time) + ","
                + str(ss.arrival.delay) + ","
                + str(departure_time) + ","
                + str(ss.departure.delay) + ","
                + str(ss.stop_id) + "\n"
            )
        elif trip_type == "e":
            file.write(
                str(entity.trip_update.trip.trip_id) + ","
                + fetch_time + ","
                + start_time + ","
                + start_date + ","
                + proto_enums.ScheduleRelationship[entity.trip_update.trip.schedule_relationship] + ","
                + str(entity.trip_update.trip.route_id) + ","
                + str(entity.trip_update.trip.direction_id) + ","
                + str(ss.stop_sequence) + ","
                + str(arrival_time) + ","
                + str(ss.arrival.delay) + ","
                + str(departure_time) + ","
                + str(ss.departure.delay) + ","
                + str(ss.stop_id) + ","
                + proto_enums.ScheduleRelationship[ss.schedule_relationship] + "\n"
            )

def is_expected(entity):
    # Dev note: Some trips have their arrival and departure delays
    # have non-0's on other stops than the first so we need to go through
    # all of them
    for ss in entity.trip_update.stop_time_update:
        if ss.arrival.delay != 0 or ss.departure.delay != 0:
            return True
    return False

def classify_and_write_pb_file_as_csv(
    input_file,
    abstract_output_file,
    expected_output_file,
    fetch_time
):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = open(input_file, "rb")
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if not entity.HasField("trip_update"):
            raise ValueError("This is not a trip")

        # There are some trips that have no stop time updates for some
        # reason, ignoring them for now

        # TODO: Investigate why this happens
        if len(entity.trip_update.stop_time_update) == 0:
            continue
            # raise ValueError(
            #     "Trip {} has no stop time data".format(str(entity))
            # )

        if is_expected(entity):
            write_entity_into_file(
                expected_output_file, entity, "e", fetch_time
            )
        else:
            write_entity_into_file(
                abstract_output_file, entity, "a", None
            )

def write_timetables_as_csv(
    output_file_dir,
    output_file_name,
    input_file_dir,
    input_file_name=None,
):
    if output_file_dir[-1] != "/":
        output_file_dir = output_file_dir + "/"
        
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)

    file_name, file_format = output_file_name.split(".")
    abstract_output_file = open(
        output_file_dir + file_name + "_abstract." + file_format, "w"
    )
    expected_output_file = open(
        output_file_dir + file_name + "_expected." + file_format, "w"
    )

    write_file_header(abstract_output_file, "a")
    write_file_header(expected_output_file, "e")
    
    # Assuming that files follow the format of `trips_YYYY-MM-DD_fetchTime`,
    # Then we will parse the file names and send an additional arg
    # to write_entity_into_file as the fetchTime

    # The second split is for backwards compatability because some of the
    # older files had `.pb` as their format which will not change anything
    # if there is no dot
    if input_file_name is not None:
        classify_and_write_pb_file_as_csv(
            "{}/{}".format(input_file_dir, input_file_name),
            abstract_output_file,
            expected_output_file,
            (file.split("_")[-1]).split(".")[0]
        )
    else:
        for file in os.listdir(input_file_dir):
            print(input_file_dir + "/" + file)
            classify_and_write_pb_file_as_csv(
                "{}/{}".format(input_file_dir, file),
                abstract_output_file,
                expected_output_file,
                (file.split("_")[-1]).split(".")[0]
            )
    abstract_output_file.close()
    expected_output_file.close()

def main():
    args = sys.argv[1:]

    if len(args) != 5 and len(args) != 4:
        raise ValueError("Parameters must be one of the following two forms:\n"
            + "- `file Y y X x` to read a single file and write it as a csv "
            + "file where `X` is the input directory, `x` is the file to be "
            + "read, `Y` is the output directory, and `y` is the output file "
            + "name.\n"
            + "- `folder/dir Y y X` to read an entire directory `X` of "
            + "tripupdate files and write them into a single file `y` in "
            + "directory `Y`"
        )

    write_timetables_as_csv(*args[1:])

if __name__ == "__main__":
    main()