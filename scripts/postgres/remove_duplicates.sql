/* Due to the weird duplicates at times in the csv file, the following
   approach allows us to remove the duplicates in an easy way */
CREATE TEMP TABLE tmp_table
AS
SELECT * 
FROM vehicle_data
WITH NO DATA;

COPY tmp_table
FROM '/var/lib/postgresql/data/vehicleupdates_2024-05-11.csv'
DELIMITER ',' CSV HEADER;

INSERT INTO vehicle_data
SELECT DISTINCT ON (trip_id, vehicle_id, timestamp) *
FROM tmp_table
ORDER BY (timestamp);