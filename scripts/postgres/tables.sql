/* Vehicle updates */

CREATE TABLE IF NOT EXISTS vehicle_data (
    trip_id VARCHAR (50),
    vehicle_id VARCHAR (20),
    start_time TIME,
    start_date DATE,
    schedule_relationship VARCHAR (50),
    route_id VARCHAR (10),
    direction_id SMALLINT,
    speed REAL,
    latitude REAL,
    longitude REAL,
    current_stop_sequence SMALLINT,
    current_status VARCHAR (30),
    timestamp VARCHAR (20),
    congestion_level VARCHAR (30),
    stop_id VARCHAR (10),
    PRIMARY KEY(trip_id, start_date, current_stop_sequence)
);

CREATE TABLE IF NOT EXISTS trip_data (
    trip_id VARCHAR (50),
    start_time TIME,
    start_date DATE,
    schedule_relationship VARCHAR (50),
    route_id VARCHAR (10),
    direction_id SMALLINT,
    stop_sequence SMALLINT,
    arrival_timestamp VARCHAR (20),
    arrival_delay SMALLINT,
    departure_timestamp VARCHAR (20),
    departure_delay SMALLINT,
    stop_id VARCHAR (10),
    stop_schedule_relationship VARCHAR (50),
    PRIMARY KEY(trip_id, stop_sequence, arrival_timestamp, departure_timestamp)
);

CREATE TABLE IF NOT EXISTS trips (
    route_id VARCHAR (10),
    service_id VARCHAR (50),
    trip_id VARCHAR (50),
    trip_headsign VARCHAR (50),
    shape_id VARCHAR (10),
    block_id VARCHAR (10),
    direction_id SMALLINT,
    /* PRIMARY KEY(trip_id, vehicle_id, timestamp) */
);

CREATE TABLE IF NOT EXISTS stops (
    stop_id VARCHAR (10) PRIMARY KEY,
    stop_name VARCHAR (100),
    stop_latitude REAL,
    stop_longitude REAL,
    stop_code VARCHAR (10)
);

