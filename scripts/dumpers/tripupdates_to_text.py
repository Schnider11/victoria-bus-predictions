import os
import sys

from google.transit import gtfs_realtime_pb2


def write_pb_file_as_text(input_file, output_file):
    feed = gtfs_realtime_pb2.FeedMessage()
    response = open(input_file, "rb")
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            if entity.trip_update.HasField("trip"):
                output_file.write(str(entity))
    output_file.close()

def write_tripupdates_as_text(
    output_file_dir,
    output_file_name,
    input_file_dir,
    input_file_name
):
    if output_file_dir[-1] != "/":
        output_file_dir = output_file_dir + "/"
        
    if not os.path.exists(output_file_dir):
        os.makedirs(output_file_dir)

    output_file = open(output_file_dir + output_file_name, "w")

    write_pb_file_as_text(
        "{}/{}".format(input_file_dir, input_file_name),
        output_file
    )
    output_file.close()

def main():
    args = sys.argv[1:]

    if len(args) != 5 and len(args) != 4:
        raise ValueError("Parameters must be in the following form:"
        + "\n- `Y y X x` to read a single file and write it as a csv "
        + "file where `X` is the input directory, `x` is the file to be read, "
        + "`Y` is the output directory, and `y` is the output file name.\n")

    write_tripupdates_as_text(*args)

if __name__ == "__main__":
    main()