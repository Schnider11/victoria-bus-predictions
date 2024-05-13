# May 13

## Notes
- Files in tripupdates only have delays for the busses that are operating
around 30 minutes from fetching time, so the script has been split in two:
    - Fetch vehicleupdates every 30 seconds
    - Fetch tripupdates every 20 minutes

## Decisions
- Split scraping file into two and adjust timings

# May 12

## Notes
- A repo has been created to be shared between student and supervisor to ease
file and knowledge transfers
- The files fetched as tripupdates are quite large, do we need all the data?

## Decisions
- Meeting are going to take place every Monday at 9:00 PM

## TODO
- Document the data
- Are there delay patterns that can be learned using a machine learning model
based on the day of the week, time, and route?
- Find out what can be cut away from tripupdates

# May 9

## Notes
- Think in terms of questions that are important for the domain
	- Solve problems, do not create more
- [x] Make one script that downloads vehicle information every 30 seconds
- [ ] Do timeseries, they retain the information about the time of
day and day that is happening
Feed that into a machine learning model
- [x] Write a couple paragraphs about what we're doing and a couple
questions that we hope to answer **BY MONDAY**
	- Questions:
		- Are there delay patterns that can be learned using a machine learning
        model based on the day of the week, time, and route?
- [x] Write a Bash script that runs the Python script and zips the output files

## TODO
- Document the data
- Answer: Are there delay patterns that can be learned using a machine learning
model based on the day of the week, time, and route?