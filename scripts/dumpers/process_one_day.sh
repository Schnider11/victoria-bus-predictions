if [ -z "$1" ] ; then
  echo "No argument supplied"
  exit 1
fi

date=$1

python vehicleupdates_to_csv.py folder /home/jack/uvic/honors-proj/csv/ vehicleupdates_${date}.csv /home/jack/uvic/honors-proj/vehicleupdates/${date}
python timetable_builder.py folder /home/jack/uvic/honors-proj/csv/ trips_${date}.csv /home/jack/uvic/honors-proj/tripupdates/${date}
# python expected_timetable_splitter.py /home/jack/uvic/honors-proj/csv/trips_${date}_expected.csv

sort -u /home/jack/uvic/honors-proj/csv/trips_${date}_abstract.csv -o /home/jack/uvic/honors-proj/csv/trips_${date}_abstract_no_dups.csv
sort -t ',' -k 2,2 -k 3,3 -k 1,1d -k 6,6n /home/jack/uvic/honors-proj/csv/trips_${date}_abstract_no_dups.csv -o /home/jack/uvic/honors-proj/csv/trips_${date}_abstract_no_dups.csv
rm /home/jack/uvic/honors-proj/csv/trips_${date}_abstract.csv

# Fixing the header because it gets messed up by sorting
vim -s vim_make_header_first_line.keys /home/jack/uvic/honors-proj/csv/vehicleupdates_${date}.csv
vim -s vim_make_header_first_line.keys /home/jack/uvic/honors-proj/csv/trips_${date}_abstract_no_dups.csv

# Fix records
sort -t ',' -k 4,4 -k 3,3  -k 1,1d -k 6,6h -k 7,7 -k 11,11n -k 13,13n /home/jack/uvic/honors-proj/csv/vehicleupdates_${date}.csv -o /home/jack/uvic/honors-proj/csv/vehicleupdates_${date}.csv
# python fix_records.py /home/jack/uvic/honors-proj/csv/vehicleupdates_${date}.csv vehicle
python ignore_records.py /home/jack/uvic/honors-proj/csv/vehicleupdates_${date}.csv vehicle
# python fix_records.py /home/jack/uvic/honors-proj/csv/trip_${date}_abstract_no_dups.csv trip
python ignore_records.py /home/jack/uvic/honors-proj/csv/trip_${date}_abstract_no_dups.csv trip

# Fixing the header because it gets messed up by sorting
vim -s vim_make_header_first_line.keys /home/jack/uvic/honors-proj/csv/vehicleupdates_${date}.csv
vim -s vim_make_header_first_line.keys /home/jack/uvic/honors-proj/csv/trips_${date}_abstract_no_dups.csv

# Perform interpolation
python interpolating_vehicleupdates.py /home/jack/uvic/honors-proj/csv vehicleupdates_${date}.csv