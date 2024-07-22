#!/bin/bash

counter=15
while [ $counter -le 31 ]
do
    folder_name="2024-05-"$counter
    python vehicleupdates_to_csv.py folder /home/jack/uvic/honors-proj/csv/ vehicleupdates_$folder_name.csv /home/jack/uvic/honors-proj/vehicleupdates/$folder_name
    ((counter++))
done
