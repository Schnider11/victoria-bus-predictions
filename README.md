
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