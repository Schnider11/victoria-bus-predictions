The Victoria transit busses can have great delays at times. In some instances,
it is due to constructions that cause busses to alter their routes to get back
on track. In other instances, traffic, number of people getting on and off the
bus, people that require special accommodations *NOTE: Should we mention this?*,
and drivers can greatly alter the expected arrival time of busses, which
requires people to wait for more than 30 minutes for a bus at times. All of
these factors add several layers of complexity because route alterations and
reasons for delays are not documented in the data.

Busses always try to be on schedule, so if a bus is running ahead of schedule,
then the driver will wait at a stop for a few minutes before resuming
operation. However, in cases of delays due to the various uncontrollable
factors, that forces the bus to be late at best and a congestion of multiple
instances of the same bus running one behind the other at worst. 

After facing many delays, we became curious if these delays can be predicted by
looking at historical data and using a machine learning model to learn the
patterns in the data. We will collect data for a number of months and use them
to construct a number of machine learning models using a number of different
algorithms, and the measure of accuracy will be mean squared error between the
predicted time and actual time.


Through our work, we hope to answer the following questions: 
- Are there delay patterns that can be learned and predicted using a machine
learning model based on the day of the week, time, and route?
- Can results for examining a single route be generalized to all routes?
- Are the results reliable?
- Measures of quality: How good is a given route scheduling or how well
does a vehicle follow a route?