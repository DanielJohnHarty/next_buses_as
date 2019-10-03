from selenium import webdriver
import pandas as pd
import json
import datetime
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

def get_bus_times_df():
    now=datetime.datetime.now()

    bus_lines_to_work = {'A':"https://www.vianavigo.com/fiches-horaires/bus/056356001:A?date={}-{}-{}T{}:{}&direction=-1&line=056356001:A||A|Bus|Phébus".format(now.year, now.month, now.day, now.hour, now.minute),
                        'E':"https://www.vianavigo.com/fiches-horaires/bus/056356026:E?date={}-{}-{}T{}:{}&direction=-1&line=056356026:E||E|Bus|Phébus".format(now.year, now.month, now.day, now.hour, now.minute),
                        'K': "https://www.vianavigo.com/fiches-horaires/bus/056356021:K?date={}-{}-{}T{}:{}&direction=-1&line=056356021:K||K|Bus|Phébus".format(now.year, now.month, now.day, now.hour, now.minute),
                        'BAK': "https://www.vianavigo.com/fiches-horaires/bus/056356102:BAK?date={}-{}-{}T{}:{}&direction=-1&line=056356102:BAK||BAK|Bus|Phébus".format(now.year, now.month, now.day, now.hour, now.minute)}


    buses_to_work_df = pd.DataFrame()

    browser = webdriver.Chrome()

    for busline, url in bus_lines_to_work.items():
        browser.get(url)
        WebDriverWait(browser,poll_frequency=1, timeout=10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'table-detail-schedule')))

        schedule = browser.find_element_by_class_name('table-detail-schedule').get_attribute('innerHTML')

        schedule_df = pd.read_html(schedule)[0] # Get the first table, additional tables will be in additional list slots

        schedule_df.columns = ['BusStop', '1st','2nd','3rd','4th','5th']
        schedule_df['BusLine'] = busline
        schedule_df.dropna(axis=0, inplace=True)
        schedule_df[[ '1st','2nd','3rd','4th','5th']] = \
            schedule_df[[ '1st','2nd','3rd','4th','5th']].apply(lambda x:x.str.replace('h',':'))


        buses_to_work_df = buses_to_work_df.append(schedule_df)
        
        
    browser.close()

    buses_to_work_from_home = buses_to_work_df[buses_to_work_df['BusStop']=='Evêché']

    ranked_buses_to_work = pd.DataFrame()

    for i in [ '1st','2nd','3rd','4th','5th']:
        temp_df = buses_to_work_from_home[['BusStop', i, 'BusLine']]
        temp_df.columns = ['BusStop', 'BusTime', 'BusLine']
        ranked_buses_to_work = ranked_buses_to_work.append(temp_df)

    ranked_buses_to_work.sort_values(by=['BusTime'], inplace=True)
    ranked_buses_to_work = ranked_buses_to_work[ranked_buses_to_work['BusTime']>'{}:{}'.format(now.hour,now.minute)]

    return ranked_buses_to_work


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    df = get_bus_times_df()
    print(df.to_string())
    print(datetime.datetime.now()-start_time)
    
