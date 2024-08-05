import datetime
import os
import sys

import time_manipulation


def main():
    args = sys.argv[1:]

    if len(args) != 1:
        raise ValueError("Parameter is `X` where X is the path to the files")

    for file_name in os.listdir(args[0]):
        if len(file_name.split("_")) > 1:
            continue

        with open(args[0] + "/" + file_name, "r") as f:
            new_file_name = (
                file_name.split(".")[0] +
                "_" +
                datetime.datetime.now().strftime("%m-%d_%H-%M-%S") +
                "_converted.csv"
            )
            new_file = open(args[0] + "/" + new_file_name, "w")
            date = None
            for record in f:
                if len(record.strip()) == 0:
                    continue

                s = record.split(",")
                if len(s) > 2:
                    # Header info
                    date = "".join(s[-2:]).strip()
                    date = time_manipulation.format_to_datetime(date)
                    new_file.write(record)
                else:
                    stop_times = record.split(",")
                    print(stop_times)
                    new_stop_times = []
                    for i, t in enumerate(stop_times):
                        if t != "None":
                            t = t.split(":")
                            print(t)
                            t = datetime.timedelta(
                                minutes=int(t[0]),
                                seconds=int(t[1].split(".")[0]) + round(float(t[1].split(".")[1]) / 100.0)
                            )
                            new_stop_times.append(
                                str(int((date + t).timestamp()))
                            )
                            date += t

                    if len(new_stop_times) == 2:
                        new_file.write(
                            new_stop_times[0] +
                            "," + 
                            new_stop_times[1] +
                            "\n"
                        )
                    else:
                        new_file.write(
                            new_stop_times[0] +
                            "," + 
                            new_stop_times[0] +
                            "\n"
                        )
        new_file.close()

if __name__ == "__main__":
    main()