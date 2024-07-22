import os
import sys

import proto_enums
from google.transit import gtfs_realtime_pb2
from time_manipulation import normalize_time


def write_file_header(file):
    file.write("trip_id,vehicle_id,start_time,start_date," +
        "schedule_relationship,route_id,direction_id,speed," +
        "latitude,longitude,current_stop_sequence,current_status," +
        "timestamp,congestion_level,stop_id\n")

def write_entity_into_file(file, entity):
    # Start time sometimes shows up with hours as 25 or 26, normalize
    start_time, start_date = normalize_time(
        str(entity.vehicle.trip.start_time), 
        str(entity.vehicle.trip.start_date)
    )
    
    file.write(str(entity.vehicle.trip.trip_id) + ","
        + str(entity.vehicle.vehicle.id) + ","
        + start_time + ","
        + start_date + ","
        + proto_enums.ScheduleRelationship[entity.vehicle.trip.schedule_relationship] + ","
        + str(entity.vehicle.trip.route_id) + ","
        + str(entity.vehicle.trip.direction_id) + ","
        + str(entity.vehicle.position.speed) + ","
        + str(entity.vehicle.position.latitude) + ","
        + str(entity.vehicle.position.longitude) + ","
        + str(entity.vehicle.current_stop_sequence) + ","
        + proto_enums.VehicleStopStatus[entity.vehicle.current_status] + ","
        + str(entity.vehicle.timestamp) + ","
        + proto_enums.CongestionLevel[entity.vehicle.congestion_level] + ","
        + str(entity.vehicle.stop_id) + "\n")

def write_pb_file_as_csv(input_file, output_file):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = open(input_file, "rb")
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField("vehicle"):
            if entity.vehicle.HasField("trip"):
                # Vehicle is actually on the road
                write_entity_into_file(output_file, entity)

def write_vehicleupdates_as_csv(
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
        + "vehicleupdate files and write them into a single file `y` in "
        + "directory `Y`")

    write_vehicleupdates_as_csv(*args[1:])

if __name__ == "__main__":
    main()