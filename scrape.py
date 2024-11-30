import argparse
import re
import time

from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def main(building, start_month, start_day, start_year, end_month, end_day, end_year):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options) 
    URL = "https://www.colby.edu/itscustomcf/news_events/calendar/buildingavail.cfm"
    driver.get(URL)

    building_select = Select(driver.find_element(By.NAME, 'building'))
    building_select.select_by_visible_text(building) 

    start_month_select = Select(driver.find_element(By.NAME, 'startmonth'))
    start_month_select.select_by_value(start_month) 

    start_day_select = Select(driver.find_element(By.NAME, 'startday'))
    start_day_select.select_by_value(start_day)  

    start_year_select = Select(driver.find_element(By.NAME, 'startyear'))
    start_year_select.select_by_value(start_year)  

    end_month_select = Select(driver.find_element(By.NAME, 'endmonth'))
    end_month_select.select_by_value(end_month)  

    end_day_select = Select(driver.find_element(By.NAME, 'endday'))
    end_day_select.select_by_value(end_day)  

    end_year_select = Select(driver.find_element(By.NAME, 'endyear'))
    end_year_select.select_by_value(end_year)  

    submit_button = driver.find_element(By.XPATH, "//input[@value='Show Schedule']")
    submit_button.click()

    # time.sleep(1)

    html_content = driver.page_source 
    soup = BeautifulSoup(html_content, 'html.parser')

    event_table = soup.find('table', class_='table_lorange_topbord')

    if event_table is None or isinstance(event_table, NavigableString):
        print("No events found")
        driver.quit()
        exit()

    events = {}

    for row in event_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        
        if len(columns) > 2:  
            room = columns[0].get_text(strip=True)
            date = columns[1].get_text(strip=True)
            
            events_links = columns[2].find_all('a')
            for link in events_links:
                if 'javascript:alert' in link['href']:
                    event_info = link['href'].split('"')[1]

                    if room in events:
                        events[room].append({
                            'date': date,
                            'event_info': event_info
                        })
                    else:
                        events[room] = [{
                            'date': date,
                            'event_info': event_info
                        }]

    match_time_re = r"(\d{2}\/\d{2})\s*(\d{1,2}:\d{1,2}-\d{1,2}:\d{2})\s*(AM|PM)"

    for room, room_events in events.items():
        print(f"Room: {room}")
        for event in room_events:
            match_time = re.search(match_time_re, event['event_info'])
            if match_time:
                d, t, m = match_time.groups()
                print(f" - {d} {t} {m}")
            else:
                print(f" - {event['event_info']}")
        print()

    driver.quit()

def format_string(s):
    return s.replace("_", " ").replace("-", " ").lower()

def parse_date(s:str):
    current_year = time.strftime("%Y")

    split_date = s.split('-')

    if len(split_date) < 2:
        return None, None, None

    date_month = split_date[0]
    date_day = split_date[1]

    if len(split_date) > 2:
        date_year = split_date[2]
    else:
        date_year = current_year

    return date_month, date_day, date_year

if __name__ == "__main__":
    buildings = [
        "34 Burleigh Street",
        "Alfond Apartment Complex",
        "Alfond Athletic Center",
        "Anthony",
        "Arboretum",
        "Arey",
        "Art Museum",
        "Averill",
        "Bixler",
        "Coburn",
        "Colby Gardens",
        "Colby Hume Camp",
        "Cotter Union",
        "Dana",
        "Davis Science Building",
        "Diamond",
        "Drummond",
        "East Quad",
        "Eustis",
        "Field House",
        "Fields",
        "Foss",
        "Garrison Foster",
        "Global Dorms",
        "Goddard-Hodgkins",
        "Gordon Center For Creative & Performing Arts",
        "Grossman",
        "Heights",
        "Hill Family House",
        "Hillside Complex",
        "Johnson",
        "Johnson Pond House 1",
        "Johnson Pond House 2",
        "Johnson Pond House 3",
        "Johnson Pond House 4",
        "Keyes",
        "Lawn Areas",
        "Leonard",
        "Lorimer Chapel",
        "Lovejoy",
        "Lunder House",
        "Marriner",
        "Mary Low",
        "Miller Library",
        "Mitchell",
        "Music Shell",
        "New Athletic Center",
        "Not Applicable",
        "Observatory",
        "Olin",
        "Outdoor Areas",
        "Parking Lots",
        "Pepper",
        "Perkins-Wilson",
        "Pierce",
        "Piper",
        "President's House",
        "Roberts",
        "Robins",
        "Runnals",
        "S G Mudd",
        "Schupf",
        "SSWAC",
        "Sturtevant",
        "Taylor",
        "Treworgy",
        "West Quad",
        "Williams",
        "Woodman",
    ]

    parser = argparse.ArgumentParser(description='Fetch building event schedules.')
    parser.add_argument('-b','--building', type=str, required=True, help='Building name (e.g., "S G Mudd")')
    parser.add_argument('-s', '--start', type=str, required=False, help='Start date (MM-DD[-YYYY])')
    parser.add_argument('-e', '--end', type=str, required=False, help='End date (MM-DD[-YYYY])')
    parser.add_argument('-d','--date', type=str, required=False, help='Default Date (sets -e and -s) (MM-DD[-YYYY])')
    
    args = parser.parse_args()

    formatted_building = format_string(args.building)
    matched_building = None

    for building in buildings:
        if formatted_building == format_string(building):
            matched_building = building
            break

    if matched_building is None:
        print("error: invalid building name")
        exit()

    if not args.date:
        args.date = time.strftime("%m-%d-%Y")
    elif args.start or args.end:
        print("error: cannot set -d with -s or -e")
        exit()


    date_month, date_day, date_year = parse_date(args.date)

    if date_month is None:
        print("error: invalid date")
        exit()

    if not args.start:
        args.start = args.date
    if not args.end:
        args.end = args.date

    start_month, start_day, start_year = parse_date(args.start)
    end_month, end_day, end_year = parse_date(args.end)

    if start_month is None or start_year is None or start_day is None:
        print("error: invalid start date")
        exit()

    if end_month is None or end_year is None or end_day is None:
        print("error: invalid end date")
        exit()

    if int(start_year) > int(end_year) or (int(start_year) == int(end_year) and int(start_month) > int(end_month)) or (int(start_year) == int(end_year) and int(start_month) == int(end_month) and int(start_day) > int(end_day)):
        print("error: invalid date range, start date must be before end date")
        exit()

    main(matched_building, start_month, start_day, start_year, end_month, end_day, end_year)
