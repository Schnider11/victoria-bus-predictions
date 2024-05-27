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