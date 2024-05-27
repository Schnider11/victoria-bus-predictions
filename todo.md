## Researching

- [ ] Document the data
- [ ] Find out how to generate tripupdate information using vehicleupdates
and the static data. Probably some cross-correlation with the static data
- [ ] Learn about timeserires
- [ ] Check whether the data reflects the fact that some busses become
other busses (7 to 21 and vice versa). Check if the vehicle ID remains and
whether you can trace that relation from the data
- [ ] Find out what happens to the order of the stops if there is construction,
does the bus seem like it skipped a number of stops from the data or is there
a correlation between the old and new stops?
- [ ] Is there any alternatives to using `(trip_id, vehicle_id, timestamp)`
as a composite primary key?
    - `stop_id` won't work if the bus spent more than 30 seconds heading or
    stopping at a single stop, which might happen at the start of the route
- [ ] Should the status codes be saved in their own table rather than being
just out there in the data?
- [ ] Make a file similar to vehicleupdates_to_csv but for tripupdates
    1. Make a txt version and understand why the sizes are different as
    files seem to become larger and larger until ~10 AM, then they plateau
    for a bit, then they decrease in size
        > The decrease is understandable because tripupdates only contains
        information from that point in the day until the end of the day, or
        that's how it was assumed so far at least. However, the increase is
        weird
    2. After completing the first task, create a script that converts the
    `pb` files into `csv` files - might only need a handful of tripupdates
    files for an entire day to create a table for that day

## In Progress


## Done

- [x] Find out what can be cut away from tripupdates
- [x] Write a script/program that generates a .csv file from vehicleupdates
- [x] Revert scripts to how they were before
- [x] Verify what `IN_TRANSIT_TO` and `STOPPED_AT` mean
    - > Added a proto_enums.py file that contains information taken
    from the github page that describes what fields mean
- [x] Investigate weird rows in vehicleupdates that contain hardly any
information ![img](images/vehicleupdates_missing_info.png)
    - It seems like some vehicle stop somewhere and do not get assigned routes
    (maybe stopped for service, break, etc.). These vehicles will be ignored
    ![img](images/vehicleupdates_missing_info_explained.png)
- [x] Adjust questions in the `project_description.md` to be from the
prespective of the user
- [x] Create tables for stops and try to join with vehicle_data