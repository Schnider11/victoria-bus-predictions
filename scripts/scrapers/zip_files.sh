#!/bin/bash

date=$(date -I)
zip -r "${date}" "vehicleupdates/${date}" "tripupdates/${date}"

# Do we want one file to contain