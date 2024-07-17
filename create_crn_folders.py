import pandas as pd 
from selenium import webdriver
import utils
from getpass import getpass

courses = pd.DataFrame(pd.read_excel("schedules.xlsx"))
url = "https://mediasite.ucdavis.edu/Mediasite/manage"
username = input("Enter your username: ")
password = getpass("Enter your password: ")
driver = webdriver.Chrome()
driver.implicitly_wait(1)
utils.login(driver, url, username, password)
destination_folder = 'UC Davis Courses'
utils.navigate_to_folder(driver, destination_folder)

for index, course in courses.iterrows():
    new_folder = course['crn']
    utils.add_new_folder(driver, destination_folder, new_folder)
