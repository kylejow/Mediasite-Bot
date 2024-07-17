import pandas as pd
from datetime import datetime, timedelta

# Function to validate time
def is_valid_time(t):
    try:
        datetime.strptime(t, '%H:%M:%S')
        return True
    except ValueError:
        return False

# Function to validate duration
def is_valid_duration(hours, minutes):
    return hours >= 0 and minutes >= 0

# Function to validate recurring days in MTWRF format
def is_valid_days(days):
    valid_sequence = "MTWRF"
    index = 0
    
    for day in days:
        if day not in valid_sequence:
            return False
        while index < len(valid_sequence) and valid_sequence[index] != day:
            index += 1
        if index == len(valid_sequence):
            return False
    
    return True

def is_valid_room(room):
    return int(room) in {1001, 1002, 1301, 1303,
                         1320, 2040, 2050, 2100,
                         2302, 2303, 2304, 2306,
                         2320, 2360}

# Load courses from Excel file
courses = pd.DataFrame(pd.read_excel("schedules.xlsx"))

# Process each course
for index, course in courses.iterrows():
    try:
        crn = course['crn']

        if pd.isnull(crn):
            raise ValueError("CRN is empty")
        
        room_number = course['room']
        if not is_valid_room(room_number):
            raise ValueError(f"Invalid room number for course {crn}")
        
        title = course['title']
        if pd.isnull(title):
            raise ValueError(f"Title is empty for course {crn}")
        
        start = course['start']
        # Validate and parse start time
        if not is_valid_time(str(start)):
            raise ValueError(f"Invalid start time for course {title}")
        
        start = datetime.combine(datetime.today(), start) - timedelta(minutes=1)
        start_hour = int(start.strftime('%I'))
        start_minute = int(start.strftime('%M'))
        start_am_pm = start.strftime('%p')
        
        # Validate duration
        duration_hour = int(course['duration_hour'])
        duration_minute = int(course['duration_minute']) + 2
        if not is_valid_duration(duration_hour, duration_minute):
            raise ValueError(f"Invalid duration for course {title}")
        
        # Validate recurring days
        recurring_days = course['days']
        if not is_valid_days(recurring_days):
            raise ValueError(f"Invalid recurring days for course {title}")
        
        print(f"Course {crn} validated successfully")

    except Exception as e:
        print(f"Error processing course {crn}: {e}")
        continue
