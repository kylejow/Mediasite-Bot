from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from time import sleep
import calendar
import datetime

def login(driver, url, username, password):
    driver.get(url)

    username_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "UserName"))
    )
    username_field.send_keys(username)

    password_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "Password"))
    )
    password_field.send_keys(password)

    signIn_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Sign In')]"))
    )
    signIn_button.click()

    # verify login with presence of "System Overview" header
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//h2[@class='pull-left' and @data-title='System Overview']"))
        )
    except:
        raise RuntimeError("Login failed.")

    print("Login successful.")

# navigate to parent folder prior to running this
def add_new_folder(driver, parent_folder_name, new_folder_name):
    parent_folder = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//a[text()='{parent_folder_name}']"))
    )

    actions = ActionChains(driver)
    actions.context_click(parent_folder).perform()

    context_menu = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'vakata-contextmenu-only'))
    )

    if context_menu.is_displayed() and context_menu.value_of_css_property("visibility") == "visible":
        add_folder = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, ".//a[text()='Add Folder...']"))
        )
        add_folder.click()
    else:
        print("Context menu is not visible.")


    folder_name_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "nameBox"))
    )
    actions = ActionChains(driver)
    actions.move_to_element(folder_name_input).click().send_keys(new_folder_name).perform()

    save_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "Save"))
    )
    save_button.click()

    print(f"Added new folder: {new_folder_name}")
    sleep(1)

# navigates to folder given folder path (ex "Test Folder/Law - In Use/Student Assistant Test Edit Folder")
def navigate_to_folder(driver, folder_path):
    folders = folder_path.split('/')
    # get left navigation element
    navigation = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "NavContent"))
    )

    for folder in folders:
        folder_element = navigation.find_element(By.XPATH, f".//a[text()='{folder}']")
        folder_element.click()
        # wait for folder to expand
        sleep(1)

    try:
        navigation.find_element(By.XPATH, f".//a[text()='{folders[-1]}']")
    except:
        raise RuntimeError(f"Could not navigate to: {'/'.join(folders)}")
    print(f"Navigated to: {'/'.join(folders)}")

# opens the "Add New -> Schedule" option on destination folder
# assumes destination folder is visible on navigation
def add_new_schedule(driver, destination_folder):
    navigation = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "NavContent"))
    )
    destination_folder_element = navigation.find_element(By.XPATH, f".//a[text()='{destination_folder}']")

    # right click on destination folder
    actions = ActionChains(driver)
    actions.context_click(destination_folder_element).perform()

    # await context menu to appear
    context_menu = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'vakata-contextmenu-only'))
    )

    # if context menu is visible, click on "Add New -> Schedule"
    if context_menu.is_displayed() and context_menu.value_of_css_property("visibility") == "visible":
        add_new_option = context_menu.find_element(By.XPATH, ".//a[text()='Add New']")
        add_new_option.click()
        schedule_option = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, ".//a[text()='Schedule']"))
        )
        schedule_option.click()
    else:
        raise RuntimeError("Context menu is not visible.")
    
    # wait for schedule screen to load
    sleep(2)

# assuming is on the "Add Schedule" screen
# ends with "Add Recurrence" window open
def input_schedule(driver, title, room):
    add_schedule_change_template(driver)
    add_schedule_information(driver, title)
    add_schedule_scheduleOptions(driver, room)
    add_schedule_delivery(driver)
    add_recurrence(driver)

# changes the template to "Law Template - MP4 (On-Demand)"
def add_schedule_change_template(driver):
    # get the add schedule window
    add_schedule_window = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "ContentPage"))
    )

    # click on the "Change Template" dropdown
    change_template_dropdown = add_schedule_window.find_element(By.XPATH, "//button[contains(text(), 'Change Template')]")
    change_template_dropdown.click()

    # select the "Law Template - MP4 (On-Demand)" template
    xpath = "//div[contains(@class, 'entity-selector-template-row-view') and contains(text(), 'Law Template - MP4 (On-Demand)')]"
    template = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    template.click()

    # click on the "Ok" button to confirm template change
    template_change_confirmation = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@data-widget-name='SfDialog']//button[contains(text(), 'Ok')]"))
    )
    template_change_confirmation.click()

    # wait for template to change
    sleep(1)

    # check if template change was successful
    try:
        add_schedule_window.find_element(By.XPATH, '//h4[@id="sfPageHeaderSubTitle" and @data-title="Created From: Law Template - MP4 (On-Demand)"]')
    except:
        raise RuntimeError("Template change failed.")

# sets "Information" tab fields
def add_schedule_information(driver, title):
    title_field = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "name"))
    )
    title_field.send_keys(title)
    print(f"Title set to: {title}")

# sets "Schedule Options" tab fields
def add_schedule_scheduleOptions(driver, room):
    # get the add schedule window
    add_schedule_window = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "ContentPage"))
    )

    # click on the "Schedule Options" tab
    schedule_options_tab = add_schedule_window.find_element(By.XPATH, "//a[text()='Schedule Options']")
    schedule_options_tab.click()

    # set the presentation naming
    presentation_naming = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'TitleTypeId'))
    )
    presentation_naming_selector = Select(presentation_naming)
    # wait for the dropdown to be clickable
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(presentation_naming)
    )
    presentation_naming_selector.select_by_value('ScheduleNameAndAirDateTime')

    # set the recorder options
    recorder_options = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'RecorderOptions'))
    )
    recorder_options_selector = Select(recorder_options)
    # wait for the dropdown to be clickable
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(recorder_options)
    )
    recorder_options_selector.select_by_value('FullyAutomated')

    select_recorder(driver, room)

    print("Schedule options set.")

# selects the desired recorder within the "Schedule Options" tab
def select_recorder(driver, room):
    # get the add schedule window
    add_schedule_window = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "ContentPage"))
    )

    # get the recorder options
    recorder_options = add_schedule_window.find_element(By.XPATH, "//div[@class='form-group recorders']")

    # open the recorder selection dropdown
    recorder_selection = recorder_options.find_element(By.XPATH, "//span[@class='entity-name ellipsis' and contains(text(), 'Please Select a Recorder')]")
    recorder_selection.click()

    # wait for the recorder dropdown to appear
    recorder_dropdown = recorder_options.find_element(By.XPATH, ".//div[@class='sf-dropdown-panel wrapper']")
    WebDriverWait(driver, 5).until(
        EC.visibility_of(recorder_dropdown)
    )

    # search for the desired recorder
    recorder_search_input = recorder_dropdown.find_element(By.CSS_SELECTOR, "form.form-search input.search-query")
    recorder_search_input.send_keys(room)
    # wait for the search results to appear
    sleep(2)

    # select the desired recorder
    recorder = recorder_dropdown.find_element(By.XPATH, f".//a[contains(text(), 'LAW-MSR-KH{room}')]")
    recorder.click()

    # check if recorder selection was successful
    try:
        add_schedule_window.find_element(By.XPATH, f"//span[@class='entity-name ellipsis' and contains(text(), 'LAW-MSR-KH{room}')]")
    except:
        raise RuntimeError(f"Recorder selection failed.")

    print(f"Recorder set to: {room}")

# sets "Delivery" tab fields
def add_schedule_delivery(driver):
    # get the add schedule window
    add_schedule_window = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "ContentPage"))
    )

    delivery_tab = add_schedule_window.find_element(By.XPATH, "//a[text()='Delivery']")
    delivery_tab.click()

    # check the "Audio Transcriptions" box
    audio_transcriptions_box = add_schedule_window.find_element(By.XPATH, "//input[@type='checkbox' and @name='captioning']")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(audio_transcriptions_box)
    )
    audio_transcriptions_box.click()

    # verify that automatic captions are enabled
    try:
        select_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'audio-transcription-profile'))
        )
        select = Select(select_element)
        selected_option = select.first_selected_option.text
        assert selected_option == "*Automatic Captions"
    except:
        raise RuntimeError("Audio Transcriptions not enabled.")

    print("Audio Transcriptions enabled.")

# opens the "Add Recurrence" window
def add_recurrence(driver):
    # open the "Add Recurrence" window
    add_recurrence = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "AddRecurrence"))
    )
    add_recurrence.click()
    # wait for the window to open
    sleep(1)

    # verify that the "Add Recurrence" window is open
    try:
        window = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-header.clearfix"))
        )
        assert window.text == "Add Recurrence"
    except:
        raise RuntimeError("Add Recurrence window not found.")
    print("Add Recurrence window opened.")

# sets recurrence start date
def select_start_date(driver, month, day, year):
    # open the datepicker
    recurrence_datetime = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "recurrence-datetime"))
    )
    date_selection = recurrence_datetime.find_element(By.NAME, "datepicker")
    date_selection.click()

    # wait for the datepicker to open
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "datepicker.datepicker-dropdown"))
    )

    # input start date with datepicker
    navigate_datepicker(driver, month, year, day)

    ### element does not always update ###
    # # verify that the date was set correctly
    # try:
    #     datepicker_element = recurrence_datetime.find_element(By.CSS_SELECTOR, "input[name='datepicker']")
    #     datepicker_value = datepicker_element.get_attribute("value")
    #     assert datepicker_value == f"{month:02}/{day:02}/{year}"
    # except:
    #     raise RuntimeError("Failed to set start date.")

    print(f"Start date set to: {month:02}/{day:02}/{year}")

# datepicker must be open
# navigates to the desired date
def navigate_datepicker(driver, month, year, day):
    # Switch to the months view
    months_view_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".datepicker-days .datepicker-switch"))
    )
    months_view_button.click()

    # Switch to the years view
    years_view_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".datepicker-months .datepicker-switch"))
    )
    years_view_button.click()

    # Locate and click the desired year
    year_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[starts-with(@class, 'year') and text()='{year}']"))
    )
    year_element.click()

    # Locate and click the desired month
    month_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f"//span[starts-with(@class, 'month') and text()='{calendar.month_name[month][:3]}']"))
    )
    month_element.click()

    # Locate and click the desired day using Unix timestamp
    date = datetime.datetime(year, month, day)
    timestamp = calendar.timegm(date.utctimetuple())*1000

    date_element = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f'//td[@data-date="{timestamp}"]'))
    )
    date_element.click()

# sets recurrence start time
def select_start_time(driver, start_hour, start_minute, start_am_pm):
    # open the timepicker
    recurrence_datetime = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "recurrence-datetime"))
    )
    time_selection = recurrence_datetime.find_element(By.NAME, "timepicker")
    time_selection.click()

    # wait for the timepicker to open
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "bootstrap-timepicker-widget"))
    )

    # Find the input fields for hours, minutes, and meridian
    hour_input = driver.find_element(By.CSS_SELECTOR, 'input.bootstrap-timepicker-hour')
    minute_input = driver.find_element(By.CSS_SELECTOR, 'input.bootstrap-timepicker-minute')
    meridian_input = driver.find_element(By.CSS_SELECTOR, 'input.bootstrap-timepicker-meridian')

    # Clear the inputs and set the desired time
    hour_input.clear()
    hour_input.send_keys(start_hour)

    minute_input.clear()
    minute_input.send_keys(start_minute)

    meridian_input.clear()
    meridian_input.send_keys(start_am_pm)

    # click on title to close timepicker to prevent it from blocking other elements
    title = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="modal-header clearfix" and .//h3[text()="Add Recurrence"]]'))
    )
    title.click()

    ### element does not always update ###
    # # verify that the time was set correctly
    # try:
    #     timerpicker_element = recurrence_datetime.find_element(By.CSS_SELECTOR, "input[name='timepicker']")
    #     datepicker_value = timerpicker_element.get_attribute("value")
    #     assert datepicker_value == f"{start_hour:02}:{start_minute:02} {start_am_pm}"
    # except:
    #     raise RuntimeError("Failed to set start time.")

    print(f"Start time set to: {start_hour:02}:{start_minute:02} {start_am_pm}")

# sets recurrence duration
def set_duration(driver, duration_hour, duration_minute):
    # shitty ass mediasite no ID or name, use parent
    recurrence_dialog = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "RecurrenceDialog"))
    )
    duration_text = recurrence_dialog.find_element(By.XPATH, '//label[@class="control-label" and text()="Duration"]')
    # Find the parent form-group div
    form_group_div = duration_text.find_element(By.XPATH, './ancestor::div[@class="form-group"]')
    # Find the nested input element with name "timepicker"
    timepicker_input = form_group_div.find_element(By.CSS_SELECTOR, 'input[name="timepicker"]')
    # Click on the timepicker
    timepicker_input.click()

    # wait for the timepicker to open
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "bootstrap-timepicker-widget"))
    )

    # Clear the inputs and set the desired time
    hour_input = driver.find_element(By.CSS_SELECTOR, 'input.bootstrap-timepicker-hour')
    minute_input = driver.find_element(By.CSS_SELECTOR, 'input.bootstrap-timepicker-minute')

    hour_input.clear()
    hour_input.send_keys(duration_hour)

    minute_input.clear()
    minute_input.send_keys(duration_minute)

    # click on title to close timepicker
    title = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="modal-header clearfix" and .//h3[text()="Add Recurrence"]]'))
    )
    title.click()

    # verify that the time was set correctly
    # timepicker value does not change?

    print(f"Duration set to: {duration_hour}:{duration_minute:02}")

# sets recurrence to "One Time Only"
def repeats_one_time_only(driver):
    repeats_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'Repeats'))
    )
    repeats_options = Select(repeats_element)
    # wait for the dropdown to be clickable
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(repeats_element)
    )
    repeats_options.select_by_value('None')
    print("Repeats set to: One Time Only")


# sets recurrence to "Weekly"
# sets end date and days of the week
# assuming weekly is defaulted
def repeats_weekly(driver, end_month, end_day, end_year, days_of_week):
    # map for day IDs
    days_map = {
        'M': 'Monday',
        'T': 'Tuesday',
        'W': 'Wednesday',
        'R': 'Thursday',
        'F': 'Friday',
        'S': 'Saturday',
        'U': 'Sunday'
    }

    # check "Run on Days" boxes
    for day_char in days_map.keys():
        day_id = days_map.get(day_char)
        if day_id:
            checkbox = driver.find_element(By.ID, day_id)
            # Check if the checkbox should be selected
            if day_char in days_of_week:
                # Ensure checkbox is selected
                if not checkbox.is_selected():
                    checkbox.click()
            else:
                # Ensure checkbox is not selected
                if checkbox.is_selected():
                    checkbox.click()

    # open end date datepicker
    end_time_picker = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "Ends"))
    )
    date_selection = end_time_picker.find_element(By.NAME, "datepicker")
    date_selection.click()

    # wait for the datepicker to open
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "datepicker.datepicker-dropdown"))
    )

    # input end date with datepicker
    navigate_datepicker(driver, end_month, end_year, end_day)

    ### element does not always update ###
    # # verify that the end date was set correctly
    # try:
    #     datepicker_element = end_time_picker.find_element(By.CSS_SELECTOR, "input[name='datepicker']")
    #     datepicker_value = datepicker_element.get_attribute("value")
    #     assert datepicker_value == f"{end_month:02}/{end_day:02}/{end_year}"
    # except:
    #     raise RuntimeError("Failed to set start date.")

    print(f"Recurring end date set to: {end_month}/{end_day}/{end_year}")

# saves the recurrence
def save_recurrence(driver):
    save_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '.modal-footer .btn-primary[data-btn-index="Save"]'))
    )
    save_button.click()
    print("Recurrence saved.")

# saves the schedule
def save_schedule(driver):
    save_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "Save"))
    )
    save_button.click()

    # wait for schedule to save
    sleep(3)

    print("Schedule saved.")

# closes the schedule window
def close_schedule(driver):
    close_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'panel-close'))
    )
    close_button.click()

    print("Schedule closed.")