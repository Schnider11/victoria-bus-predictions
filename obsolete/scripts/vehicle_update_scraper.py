import os
import time
import urllib.request
from datetime import datetime

now = str(datetime.now()).split()
now[1] = now[1].split(".")[0]

# Make a date folder in human-readable time
vehicle_update_path = "./vehicleupdates/{}".format(now[0])
if not os.path.exists(vehicle_update_path):
    os.makedirs(vehicle_update_path)

urllib.request.urlretrieve(
    "https://bct.tmix.se/gtfs-realtime/vehicleupdates.pb?operatorIds=48",
    "{}/vehicleupdates_{}.pb".format(vehicle_update_path, int(time.time()))
)