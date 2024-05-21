# Abstract
After facing many delays riding Victoria transit busses, which happen for
numerous reasons that are outside of any person's control, we became curious
how accurate are the current bus timetables in comparison to actual delay
times and if this can be improved by looking at historical data. We will
define measure of what makes routes good and see if using data mining
techniques would allow us to find and suggest a more accurate timetable.

Despite recent efforts by B.C. Transit to install hardware for tracking
location on busses, busses are often late when compared to their schedule.
This research will not only offer an opportunity for an improvement on the
timetables, but it will also allow for a more accurate prediction of where
busses are in cases where the tracking technology is malfunctioning.

# Research Questions
Through our work, we hope to answer the following questions:
- How good are the timetables of busses in Victoria?
- Are there any delay patterns in the expected arrival time of busses in
routes in Victoria based on route, time, and day?
- If the timetables are not accurate, can we use a machine learning model
to find a better timetable that more accurately reflects delays?
    1. Compare timetables with the data
    2. Now we have a measure of goodness, are there any pattern we can
    take advantage of to create better timetables?

# Measures of quality
- How good is a given route scheduling or how well does a vehicle follow
a route?
    - The absolute difference of a stop of when a bus arrives and when
    it was expected to arrive could be a measure of how good a stop is
    - For a route, it could be the average of the absolute delays
    of all the stops. We could say that we're checking every route
    individually and computing the quality metric of the route
        - Should hours of the day have a bigger contribution to the
        weights?
        - It is safe to asssume that the timetables were built with time
        of the day and day of the week in mind, but is it actually the
        case

# Hypotheses
Knowing the time of the day and the day of the week, we can improve on the
timetable, and that having a weighted importance for different times,
especially between 8 AM-5 PM because that's when most people will work and
transport, would result in higher accuracy


- How: Use historical transit data and create metrics for route quality,
and by using machine learning, try to find better timetables