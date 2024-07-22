#!/bin/bash

counter=20
while [ $counter -le 31 ]
do
    folder_name="2024-05-"$counter
    python expected_timetable_splitter.py /home/jack/uvic/honors-proj/csv/trips_${folder_name}_expected.csv
    ((counter++))
done
