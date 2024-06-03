/* 7-VIC view */

CREATE VIEW vic7
AS
SELECT trip_id, vehicle_id, start_time, start_date, schedule_relationship,
direction_id, current_stop_sequence, current_status, timestamp, stop_id
FROM vehicle_data
ORDER BY start_date, start_time, direction_id, current_stop_sequence;

CREATE VIEW vic7_stops
AS
SELECT vic7.*, stops.stop_name
FROM vic7 JOIN stops ON vic7.stop_id = stops.stop_id;

CREATE VIEW vehicle_join_trip
AS
SELECT vehicle_data.trip_id, vehicle_data.start_time,
vehicle_data.start_date, vehicle_data.route_id, vehicle_data.direction_id,
vehicle_data.current_stop_sequence, vehicle_data.timestamp,
trip_data.arrival_timestamp, trip_data.departure_timestamp
FROM vehicle_data JOIN trip_data
ON vehicle_data.trip_id=trip_data.trip_id
WHERE vehicle_data.start_date=trip_data.start_date
AND vehicle_data.current_stop_sequence=trip_data.stop_sequence
ORDER BY vehicle_data.route_id, vehicle_data.start_time,
vehicle_data.start_date, vehicle_data.direction_id,
vehicle_data.current_stop_sequence;