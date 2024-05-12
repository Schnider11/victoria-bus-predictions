Please add the following in crontab using `crontab -e` while checking the
instructions.

Use the following snippet of code to run the scraper every 30 seconds. Crontab
doesn't allow for seconds-level of granularity so the `sleep 30` was needed.
The Python program will automatically create the vehicleupdates and tripupdates
folders and timestamp everything.

Edit the following two lines as follows:
- Adjust the parameter of `cd` to where the script resides
- Adjust the parameter of the Python executable as well

```bash
* * * * * ( cd /home/jack/uvic/honors-proj/; /home/jack/miniforge3/envs/ai-ml/bin/python ./update_scraper.py )
* * * * * ( sleep 30; cd /home/jack/uvic/honors-proj/; /home/jack/miniforge3/envs/ai-ml/bin/python ./update_scraper.py )
```

The following is to zip the files as you requested. I wrote it to run 5 minutes
before midnight just in case it took too long.

Edit the following line as the following:
- Adjust the parameter of `cd` to where the other script resides
- Adjust the time closer to midnight if you'd like, although I don't
think that will change much
```bash
55 23 * * * ( cd /home/jack/uvic/honors-proj/; /usr/bin/bash ./zip_files.sh )
```