# Colby Buildings Scraper

Quick utility scraper to find out what times buildings are being used for
events (class, meetings, TA hours, etc.) at Colby College. Useful for when you
want to find a quiet place to study, but are unsure if a room is being used for
a class or event. (However some events are still not listed on the website.)

URL: `https://www.colby.edu/itscustomcf/news_events/calendar/buildingavail.cfm`

## Usage

Sample output:

```
Room: 103 Laboratory
 - 10/24 9:30-10:45 AM

Room: 218 Laboratory
 - 10/24 1:00-4:00 PM

Room: 219 Paleontology Lab

Room: 311 Classroom
 - 10/24 12:00-12:50 PM
 - 10/24 4:00-6:30 PM
 - 10/24 7:00-9:00 PM

Room: 312 Faculty Laboratory
 - 10/24 8:00-10:50 AM
 - 10/24 1:00-3:50 PM

Room: 405 Classroom
 - 10/24 6:30-8:30 PM
```

Examples:

```
# gets the schedule for today
py scrape.py -b "S G Mudd"

# specify a different date
py scrape.py -b "Keyes" -d "10-28"

# specify different start and end times
py scrape.py -b "Davis Science Building" -s "10-20" -e "10-30"
```

I use it with a simple bash script and dmenu to quickly get the schedule for a building (`meta+o+B`):

```bash
#!/usr/bin/env bash

building=$(dmenu -i -fn "JetBrains Mono-11" < ~/code/colby-buildings-scraper/buildings.txt)
python3 ~/code/colby-buildings-scraper/scrape.py -b "$building" > /tmp/colbybuildings.txt

alacritty --class floating -o window.dimensions.columns=120 -o window.dimensions.lines=40 -e less /tmp/colbybuildings.txt
```
