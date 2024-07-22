#!/bin/bash

counter=20
while [ $counter -le 31 ]
do
    folder_name="2024-05-"$counter
    sort -u /home/jack/uvic/honors-proj/csv/trips_${folder_name}_abstract.csv -o /home/jack/uvic/honors-proj/csv/trips_${folder_name}_abstract_no_dups.csv
    sort -t ',' -k 2,2 -k 3,3 -k 1,1 -k 6,6 -n /home/jack/uvic/honors-proj/csv/trips_${folder_name}_abstract_no_dups.csv -o /home/jack/uvic/honors-proj/csv/trips_${folder_name}_abstract_no_dups.csv
    ((counter++))
done