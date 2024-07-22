#!/bin/bash

counter=20
while [ $counter -le 31 ]
do
    date="2024-05-"$counter
    python timetable_builder.py folder /home/jack/uvic/honors-proj/csv/ trips_$date.csv /home/jack/uvic/honors-proj/tripupdates/$date/
    ((counter++))
done
