# Notes

- We cannot compare two trips from two different routes because they will
  likely have differing number of stops
  - Need a way to condense a trip into a few numbers that communicate some
      measure of the quality of the trip
  - If sub-trips overlap, then we can use the stops that are in common to do
      a comparison

# Metrics for comparing two trips

- **The average delays between the expected times and the actual ones**
  - Could produce information about which stops are "bad"
  - Can only happen if the two trips are along one route
- **The duration of the expected trip vs actual trip**
  - Communicates how good the roads that the trip takes
- Different delays should be given different weights/penalties
  - A bus being late for *10-15 minutes* might be as bad as being early by
      *2-3 minutes* since if the bus is that late, then it's pretty close to
      the next bus anyway, and if the bus is that early, then if you're right
      on time, the bus will miss you anyway
    - Given a trip, return a tuple of how many were good ones and how many
          were bad ones
    - These times are not sensitive to the frequency, they need to change
          depending on the frequency

# Use cases

## Comparing actual vs abstract

> Does route 7 stick well to its schedule? How long should I expect to wait to
> get a bus if I am following the schedule?

- Input: Two sub-trips. One actual and one abstract
- Gives a measure of how good a sub-trip is
- This would be a specific instance of a trip at a specific time

## Comparing two trips of the same route

- This would be a specific instance of a trip at a specific time

### Same day

> Does route 7 run better in the morning or in the afternoon?

- Communicates how well trips run at different times of the day, and whether or
not they are effected by traffic

### Different day (same group), same time

> Does route 7 run better on Mondays than Tuesdays?

- Should only compare trips that are weekday trips or weekend trips
- Communicates how well trips run at a specific time of the day
  - A candidate for updating that trip across all days

## Comparing two trips from different routes

### Which is the better one that gets me from A to B

- Input: Two sub-trips where both start and end at the same stop
- Given two end-points, how early should I be at the stop and how
- Averages don't really matter because we don't care about how well a bus does
  in each one of the stops, we only care about the final outcome. So just
  compare the deltas
  - However, if they are about the same time, then which sticks better to the
      timeschedule

### Which one does better in general/sticks

> How does route 4 run in comparison to route 7?
> If I had two busses that get me to my destination and I am short on time,
> which one should I pick?

- Input: Two trips/sub-trips where both start and end at the same stop, which
  is the better trip?
  - Averages don't really matter because we don't care about how well a bus
      does in each one of the stops, we only care about the final outcome. So
      just compare the deltas
- Trips must be condensed first
- Take into account multiple trips that run at similar times
- Shows how good a route is compared to other routes

## Comparing weekend trips vs weekday trips

> Does route 7 busses run better on weekends or not?

- Trips must be condensed first
