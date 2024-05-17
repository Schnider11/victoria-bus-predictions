CREATE TABLE IF NOT EXISTS vehicle_data (
    trip_id VARCHAR (50),
    vehicle_id VARCHAR (20),
    start_time VARCHAR (50),
    start_date VARCHAR (50),
    schedule_relationship VARCHAR (50),
    route_id VARCHAR (50),
    direction_id VARCHAR (50),
    speed VARCHAR (50),
    current_stop_sequence VARCHAR (50),
    current_status VARCHAR (2),
    timestamp VARCHAR (20),
    congestion_level VARCHAR (2),
    stop_id VARCHAR (10),
    PRIMARY KEY(trip_id, start_time, start_date)
)
