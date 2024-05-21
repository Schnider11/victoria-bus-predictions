/* Vehicle updates */

CREATE TABLE IF NOT EXISTS vehicle_data (
    trip_id VARCHAR (50),
    vehicle_id VARCHAR (20),
    start_time TIME,
    start_date DATE,
    schedule_relationship VARCHAR (50),
    route_id VARCHAR (50),
    direction_id SMALLINT,
    speed REAL,
    current_stop_sequence SMALLINT,
    current_status VARCHAR (30),
    timestamp VARCHAR (20),
    congestion_level VARCHAR (30),
    stop_id VARCHAR (10),
    PRIMARY KEY(trip_id, vehicle_id, timestamp)
);