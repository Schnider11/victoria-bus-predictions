import os
import sys

from google.transit import gtfs_realtime_pb2


def write_file_header(out_file):
    out_file.write("trip_id,vehicle_id,start_time,start_date," +
        "schedule_relationship,route_id,direction_id,speed," +
        "current_stop_sequence,current_status,timestamp," +
        "congestion_level,stop_id\n")

def write_entity_into_file(file, entity):
    file.write(str(entity.vehicle.trip.trip_id) + ","
        + str(entity.vehicle.vehicle.id) + ","
        + str(entity.vehicle.trip.start_time) + ","
        + str(entity.vehicle.trip.start_date) + ","
        + str(entity.vehicle.trip.schedule_relationship) + ","
        + str(entity.vehicle.trip.route_id) + ","
        + str(entity.vehicle.trip.direction_id) + ","
        + str(entity.vehicle.position.speed) + ","
        + str(entity.vehicle.current_stop_sequence) + ","
        + str(entity.vehicle.current_status) + ","
        + str(entity.vehicle.timestamp) + ","
        + str(entity.vehicle.congestion_level) + ","
        + str(entity.vehicle.stop_id) + "\n")

def write_pb_file(input_file, output_file):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = open(input_file, "rb")
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField("vehicle"):
            if entity.vehicle.HasField("trip"):
                # Vehicle is actually on the road
                write_entity_into_file(out_file, entity)

def write_vehicleupdates_as_csv(
    output_file_dir,
    output_file,
    input_file_dir,
    input_file=None,
):
    if output_file_dir[-1] != "/":
        output_file_dir = output_file_dir + "/"
        
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)

    out_file = open(output_file_dir + output_file, "w")
    write_file_header(out_file)

    if input_file is not None:
        write_pb_file("{}/{}".format(input_file_dir, input_file), out_file)
    else:
        for file in os.listdir(input_file_dir):
            write_pb_file("{}/{}".format(input_file_dir, file), out_file)
    out_file.close()

def main():
    args = sys.argv[1:]
    print(args)

    if len(args) != 5 and len(args) != 4:
        raise ValueError("Parameters must be one of the following two forms:"
        + "\n- `file Y y X x` to read a single file and write it as a csv "
        + "file where `X` is the input directory, `x` is the file to be read, "
        + "`Y` is the output directory, and `y` is the output file name.\n"
        + "- `folder/dir Y y X` to read an entire directory `X` of "
        + "vehicleupdate files and write them into a single file `y` in "
        + "directory `Y`")

    if "file" in args[0]:
        write_vehicleupdates_as_csv(*args[1:])
    else:
        write_vehicleupdates_as_csv(*args[1:])

if __name__ == "__main__":
    main()