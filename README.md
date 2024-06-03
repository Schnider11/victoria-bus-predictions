
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
    - Due to duplicates in the CSV file, create a temp table that would
    be used to load in the CSV file, and then load unique entries into the
    actual table (check `scripts/postgres/remove_duplicates.sql`)
    - Describe a table `\d <table name>` or `\d+ <table name>`

# Vehicleupdates/Tripupdates to CSV
- Formats the file as a CSV file, input options are:
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

# Getting Files from Server
Use `wget --no-parent -r https://turingmachine.org/~dmg/temp/buses/20240514/`
to get all the files in the `20240514` directory for example.

# Grading
- 30% evaluation of the routes - a report on the goodness of the routes
    1. Describe the goodness measures - usually how well the bus
    is on track
    2. Report how good the timetables are in regards to the developed
    goodness measures and the actual times
- 30% Data mining part and new timetables
- 30% Final Report
- 10% Presentation