import datetime
import os
import sys

import pandas as pd


def get_df_date_format(date: datetime.datetime) -> str:
    return date.strftime("%Y-%m-%d")

def get_new_file_name(date, rec_type):
    file_name = ""
    if rec_type == "trips":
        file_name = "trips_{}_abstract_no_dups_new.csv".format(get_df_date_format(date))
    elif rec_type == "vehicle":
        file_name = "vehicleupdates_{}_new.csv".format(get_df_date_format(date))
    return file_name

def get_file_name(date, rec_type):
    file_name = ""
    if rec_type == "trips":
        file_name = "trips_{}_abstract_no_dups.csv".format(get_df_date_format(date))
    elif rec_type == "vehicle":
        file_name = "vehicleupdates_{}.csv".format(get_df_date_format(date))
    return file_name

def fix_records(path, rec_type):
    date = path.split("/")[-1].split(".")[0].split("_")[1]
    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    path = "/".join(path.split("/")[:-1])
    # The way this works is that based on the difference in the
    # day, that will be the index. If the day is one smaller, then
    # the index will be -1 and will hit the last element of the
    # list while the rest is self-explanatory

    # This is needed for vehicleupdates, but not really for trips..
    d = datetime.timedelta(days = 1)
    files = [
        open(path + "/" + get_new_file_name(date, rec_type), "w"),
        open(path + "/" + get_file_name(date + d, rec_type), "a"),
        open(path + "/" + get_file_name(date - d, rec_type), "a")
    ]

    orig_file = open(path + "/" + get_file_name(date, rec_type), "r")
    for record in orig_file:
        s_record = record.split(",")
        if s_record[0] == "trip_id": # The header
            files[0].write(record)
            continue

        if rec_type == "trips":
            d = datetime.datetime.strptime(s_record[2], "%Y%m%d")
            diff = (d - date).days
            if diff == 0:
                files[diff].write(record)
        elif rec_type == "vehicle":
            d = datetime.datetime.strptime(s_record[3], "%Y%m%d")
            diff = (d - date).days
            if diff == 0:
                files[diff].write(record)

    for f in [*files, orig_file]:
        f.close()

    os.rename(
        path + "/" + get_new_file_name(date, rec_type),
        path + "/" + get_file_name(date, rec_type)
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