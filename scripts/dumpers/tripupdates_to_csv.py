import os
import sys
from datetime import datetime

import proto_enums
from google.transit import gtfs_realtime_pb2
from time_manipulation import *


def write_file_header(file):
    file.write("trip_id,start_time,start_date," +
        "schedule_relationship,route_id,direction_id,stop_sequence," +
        "arrival_timestamp,arrival_delay,departure_timestamp," +
        "departure_delay,stop_id,stop_schedule_relationship\n")

def write_entity_into_file(file, entity):
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

        file.write(str(entity.trip_update.trip.trip_id) + ","
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

def write_pb_file_as_csv(input_file, output_file):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = open(input_file, "rb")
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            write_entity_into_file(output_file, entity)

def write_tripupdates_as_csv(
    output_file_dir,
    output_file_name,
    input_file_dir,
    input_file_name=None,
):
    if output_file_dir[-1] != "/":
        output_file_dir = output_file_dir + "/"
        
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)

    output_file = open(output_file_dir + output_file_name, "w")
    write_file_header(output_file)

    if input_file_name is not None:
        write_pb_file_as_csv(
            "{}/{}".format(input_file_dir, input_file_name),
            output_file
        )
    else:
        for file in os.listdir(input_file_dir):
            write_pb_file_as_csv(
                "{}/{}".format(input_file_dir, file),
                output_file
            )
    output_file.close()

def main():
    args = sys.argv[1:]

    if len(args) != 5 and len(args) != 4:
        raise ValueError("Parameters must be one of the following two forms:"
        + "\n- `file Y y X x` to read a single file and write it as a csv "
        + "file where `X` is the input directory, `x` is the file to be read, "
        + "`Y` is the output directory, and `y` is the output file name.\n"
        + "- `folder/dir Y y X` to read an entire directory `X` of "
        + "tripupdate files and write them into a single file `y` in "
        + "directory `Y`")

    write_tripupdates_as_csv(*args[1:])

if __name__ == "__main__":
    main()