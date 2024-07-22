#!/bin/bash

counter=20
while [ $counter -le 31 ]
do
    folder_name="2024-05-"$counter
    python tripupdates_to_csv.py folder /home/jack/uvic/honors-proj/csv/ trips_$folder_name.csv /home/jack/uvic/honors-proj/tripupdates/$folder_name
    ((counter++))
done
