
from selenium import webdriver
from getpass import getpass
import utils

driver = webdriver.Chrome()
driver.implicitly_wait(1)
url = "https://mediasite.ucdavis.edu/Mediasite/manage"
username = input("Enter your username: ")
password = getpass("Enter your password: ")
destination_folder = "Student Assistant Test Edit Folder"
room_number = "2320"
title = "test mediasite bot"
start_day = 20
start_month = 9
start_year = 2025
start_hour = 11
start_minute = 30
start_am_pm = "AM"
start_am_pm = start_am_pm.upper()
duration_hour = 1
duration_minute = 30

recurring_end_month = None
recurring_end_day = None
recurring_end_year = None
recurring_days = None
recurring = 'n'
if recurring == 'y':
    recurring = True
    recurring_end_day = 17
    recurring_end_month = 9
    recurring_end_year = 2026
    recurring_days = "MTWRF"
else:
    recurring = False


utils.login(driver, url, username, password)
utils.navigate_to_folder(driver, "Test Folder/Law - In Use/Student Assistant Test Edit Folder")
utils.add_new_schedule(driver, destination_folder)
utils.input_schedule(driver, title, room_number)
utils.select_start_date(driver, start_month, start_day, start_year)
utils.select_start_time(driver, start_hour, start_minute, start_am_pm)
utils.set_duration(driver, duration_hour, duration_minute)
if recurring:
    utils.repeats_weekly(driver, recurring_end_month, recurring_end_day, recurring_end_year, recurring_days)
else:
    utils.repeats_one_time_only(driver)
utils.save_recurrence(driver)
# utils.save_schedule(driver)

# utils.navigate_to_folder(driver, "Test Folder/Law - In Use/Student Assistant Test Edit Folder")
# folders = ['test1', 'test2', 'test3', 'test4', 'test5']
# for folder in folders:
#     utils.add_new_folder(driver, "Student Assistant Test Edit Folder", folder)

tmp = input("Press any key to quit.\n")
driver.quit()