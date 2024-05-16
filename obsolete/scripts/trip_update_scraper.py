import os
import urllib.request
from datetime import datetime

from google.transit import gtfs_realtime_pb2


def write_tripupdates_as_text(input_file, input_file_dir, output_path):
    res = open(output_path, "w")
    feed = gtfs_realtime_pb2.FeedMessage()
    response = open("{}/{}".format(input_file_dir, input_file), "rb")
    feed.ParseFromString(response.read())
    for entity in feed.entity:
        if entity.HasField("trip_update"):
            if entity.trip_update.HasField("trip"):
                for ss in entity.trip_update.stop_time_update:
                    if ss.arrival.delay != 0 or ss.departure.delay != 0:
                        res.write(str(entity))
                        break
    res.close()

datetime_now = datetime.now()

# Split was needed because the timestamp contained the fractions as well
datetime_now_timestamp = str(datetime.strptime(str(datetime_now), "%Y-%m-%d %H:%M:%S.%f").timestamp()).split(".")[0]

date = str(datetime_now).split()
date[1] = date[1].split(".")[0]

trip_update_path = "./tripupdates/{}".format(date[0])
if not os.path.exists(trip_update_path):
    os.makedirs(trip_update_path)

urllib.request.urlretrieve(
    "https://bct.tmix.se/gtfs-realtime/tripupdates.pb?operatorIds=48",
    "{}/tripupdates_{}.pb".format(trip_update_path, datetime_now_timestamp)
)

trip_output_path = trip_update_path + "/tripupdates_{}.txt".format(datetime_now_timestamp)
write_tripupdates_as_text(
    "tripupdates_{}.pb".format(datetime_now_timestamp),
    trip_update_path,
    trip_output_path
)

os.remove("{}/tripupdates_{}.pb".format(trip_update_path, datetime_now_timestamp))