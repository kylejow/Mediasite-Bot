import pandas as pd 
from selenium import webdriver
import utils
from getpass import getpass
from datetime import datetime, timedelta

courses = pd.DataFrame(pd.read_excel("schedules.xlsx")) 
print(courses)
url = "https://mediasite.ucdavis.edu/Mediasite/manage"
username = input("Enter your username: ")
password = getpass("Enter your password: ")
driver = webdriver.Chrome()
driver.implicitly_wait(1)
utils.login(driver, url, username, password)
utils.navigate_to_folder(driver, 'UC Davis Courses')

###################################
##### TODO SET SEMESTER DATES #####
start_month = 1
start_day = 1
start_year = 2025
recurring_end_month = 1
recurring_end_day = 1
recurring_end_year = 2026
##### TODO SET SEMESTER DATES #####
###################################

for index, course in courses.iterrows():
    destination_folder = course['crn']
    room_number = course['room']
    title = course['title']
    start = course['start']
    start = datetime.combine(datetime.today(), start) - timedelta(minutes=1)
    start_hour = int(start.strftime('%I'))
    start_minute = int(start.strftime('%M'))
    start_am_pm = start.strftime('%p')
    duration = course['duration']
    duration_hour = course['duration_hour']
    duration_minute = course['duration_minute'] + 2
    recurring_days = course['days']

    try:
        utils.add_new_schedule(driver, destination_folder)
        utils.input_schedule(driver, title, room_number)
        utils.select_start_date(driver, start_month, start_day, start_year)
        utils.select_start_time(driver, start_hour, start_minute, start_am_pm)
        utils.set_duration(driver, duration_hour, duration_minute)
        utils.repeats_weekly(driver, recurring_end_month, recurring_end_day, recurring_end_year, recurring_days)
        utils.save_recurrence(driver)
        utils.save_schedule(driver)
        utils.close_schedule(driver)
    except Exception as e:
        print(e)
        print("Error adding schedule for " + destination_folder)
        print(course)
        driver.quit()
        break