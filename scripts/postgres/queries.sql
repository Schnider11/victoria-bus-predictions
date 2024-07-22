SELECT t1.trip_id, t1.start_date, t2.start_date
FROM trip_data AS t1 JOIN trip_data AS t2
ON t1.trip_id=t2.trip_id
WHERE t1.start_date='2024-05-14'
AND t2.start_date='2024-05-18';