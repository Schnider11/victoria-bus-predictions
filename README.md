
# Postgres Setup
- Change directory to `scripts`
- Run `docker compose up` to run the container in the foreground or
`docker compose up -d` to run in the background
    - The compose command will mount a folder for DB communication called
    pgdata, remember to **change that directory** if file structure changed. 
    Placing files and directories inside that directory will make them visible
    inside the docker container
- Log into the docker container using `sudo docker exec -it scripts-db-1 bash`
- Once inside, use `psql -U postgres` to access the postgres interface
- Relevant postgres commands:
    - Display all DBs `\l`
    - Conntect to a DB `\c <db_name>`
    - Display all tables of the currently connected DB `\dt`
    - Create a table using what's in `postgres/create_table.sql`
    - Load the csv file into the table using `\copy vehicle_data(trip_id,vehicle_id,start_time,start_date,schedule_relationship,route_id,direction_id,speed,current_stop_sequence,current_status,timestamp,congestion_level,stop_id) FROM '/var/lib/postgresql/data/vehicleupdates_2024-05-11.csv' DELIMITER ',' CSV HEADER;`

# Vehicleupdates to CSV
- Formats vehicleupdates as a CSV file, input options are:
    - `file Y y X x` to read a single file and write it as a csv file where
    `X` is the input directory, `x` is the file to be read, `Y` is the output
    directory, and `y` is the output file name.
    - `folder/dir Y y X` to read an entire directory `X` of 
    vehicleupdate files and write them into a single file `y` in 
    directory `Y`
- Usage examples:
    - `python file ./output_dir out_file.csv ./vehicleupdates/2024-05-11 vehicleupdates_1715488711.pb`
    - `python folder ./output_dir out_file.csv ./vehicleupdates/2024-05-11`
    - `python directory ./output_dir out_file.csv ./vehicleupdates/2024-05-11`

