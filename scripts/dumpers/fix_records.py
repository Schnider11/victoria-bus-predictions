import os
import sys

import pandas as pd


def get_new_file_name(day, rec_type):
    print("REMEMBER that the file names are hard-coded")
    file_name = ""
    if rec_type == "trips":
        file_name = "trips_2024-05-{}_abstract_no_dups_new.csv".format(day)
    elif rec_type == "vehicle":
        file_name = "vehicleupdates_2024-05-{}_new.csv".format(day)
    return file_name

def get_file_name(day, rec_type):
    print("REMEMBER that the file names are hard-coded")
    file_name = ""
    if rec_type == "trips":
        file_name = "trips_2024-05-{}_abstract_no_dups.csv".format(day)
    elif rec_type == "vehicle":
        file_name = "vehicleupdates_2024-05-{}.csv".format(day)
    return file_name

def get_df_date_format(day):
    print("REMEMBER that the date format is hard-coded")
    return "202405{}".format(day)

def fix_records(path, rec_type):
    print("REMEMBER that the range is hard-coded")
    for i in range(15, 30):
        # The way this works is that based on the difference in the
        # day, that will be the index. If the day is one smaller, then
        # the index will be -1 and will hit the last element of the
        # list while the rest is self-explanatory

        # This is needed for vehicleupdates, but not really for trips..

        files = [
            open(path + "/" + get_new_file_name(i, rec_type), "w"),
            open(path + "/" + get_file_name(i + 1, rec_type), "a"),
            open(path + "/" + get_file_name(i - 1, rec_type), "a")
        ]

        orig_file = open(path + "/" + get_file_name(i, rec_type), "r")
        for record in orig_file:
            s_record = record.split(",")
            if s_record[0] == "trip_id": # The header
                files[0].write(record)
                continue

            if rec_type == "trips":
                d = int((s_record[2])[-2:])
                if d - i == 0:
                    files[d - i].write(record)
            elif rec_type == "vehicle":
                d = int((s_record[3])[-2:])
                files[d - i].write(record)

        for f in [*files, orig_file]:
            f.close()

        os.rename(
            path + "/" + get_new_file_name(i, rec_type),
            path + "/" + get_file_name(i, rec_type)
        )

def main():
    args = sys.argv[1:]

    if len(args) != 2:
        raise ValueError("Parameters are `X x` where X is the path to the "
            + "file, x is the record files' type to be fixed")

    if "trip" in args[1]:
        fix_records(args[0], "trips")
    elif "vehicle" in args[1]:
        fix_records(args[0], "vehicle")

if __name__ == "__main__":
    main()