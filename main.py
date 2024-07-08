import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText  # Import ScrolledText for better log display
from selenium import webdriver
from getpass import getpass
import utils
import sys

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, text):
        self.text_space.insert(tk.END, text)
        self.text_space.see(tk.END)  # Scroll to the end

def toggle_recurring_fields():
    if recurring_var.get() == 'y':
        recurring_end_date_label.grid()
        recurring_end_day_entry.grid()
        recurring_end_month_entry.grid()
        recurring_end_year_entry.grid()
        recurring_days_frame.grid()
    else:
        recurring_end_date_label.grid_remove()
        recurring_end_day_entry.grid_remove()
        recurring_end_month_entry.grid_remove()
        recurring_end_year_entry.grid_remove()
        recurring_days_frame.grid_remove()

def start_bot():
    try:
        log_window = tk.Toplevel(root)
        log_window.title("Log Window")
        
        log_text = ScrolledText(log_window, height=20, width=60)
        log_text.pack(fill=tk.BOTH, expand=True)
        
        sys.stdout = StdoutRedirector(log_text)  # Redirect stdout to log_text

        driver = webdriver.Chrome()
        driver.implicitly_wait(1)
        
        url = "https://mediasite.ucdavis.edu/Mediasite/manage"
        username = username_entry.get()
        password = password_entry.get()
        folder_path = folder_entry.get()
        destination_folder = folder_path.split("/")[-1]
        room_number = room_number_entry.get()
        title = title_entry.get()
        start_month = int(start_month_entry.get())
        start_day = int(start_day_entry.get())
        start_year = int(start_year_entry.get())
        start_hour = int(start_hour_entry.get())
        start_minute = int(start_minute_entry.get())
        start_am_pm = am_pm_var.get().upper()
        duration_hour = int(duration_hour_entry.get())
        duration_minute = int(duration_minute_entry.get())
        
        recurring = recurring_var.get()
        if recurring == 'y':
            recurring = True
            recurring_end_month = int(recurring_end_month_entry.get())
            recurring_end_day = int(recurring_end_day_entry.get())
            recurring_end_year = int(recurring_end_year_entry.get())
            recurring_days = ''.join(day for index, day in enumerate(days_of_week) if recurring_days_vars[index].get() == "1")
        else:
            recurring = False

        utils.login(driver, url, username, password)
        
        utils.navigate_to_folder(driver, folder_path)
        
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

        # TODO uncomment
        # utils.save_schedule(driver)

        # utils.close_schedule(driver)
        
        # Inform user about completion
        log_text.insert(tk.END, "Schedule created successfully!\n")
        
        # Add Quit button with confirmation dialog
        def confirm_quit():
            if messagebox.askokcancel("Close", "Are you sure you want to close the webdriver?"):
                log_window.destroy()
        
        quit_button = tk.Button(log_window, text="Close", command=confirm_quit)
        quit_button.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        log_window.protocol("WM_DELETE_WINDOW", confirm_quit)  # Handle window close event
        
        log_window.wait_window()  # Wait for log window to be closed
        
    except Exception as e:
        log_text.insert(tk.END, f"Error: {str(e)}\n")
    finally:
        if 'driver' in locals():
            driver.quit()

def quit_app():
    root.destroy()

root = tk.Tk()
root.title("Mediasite Bot")

# Username
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Password
tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Folder Path
def select_common_path(selected_path):
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, selected_path)
tk.Label(root, text="Folder Path:").grid(row=2, column=0, padx=10, pady=5)
folder_entry = tk.Entry(root)
folder_entry.grid(row=2, column=1, padx=10, pady=5)
menubutton = tk.Menubutton(root, text="▼", relief="raised")
menubutton.grid(row=2, column=2, padx=0, pady=5)
menu = tk.Menu(menubutton, tearoff=0)
menubutton.configure(menu=menu)
common_paths = ["Law/Academic Success/1LASP Workshops 2023-24",
                "Test Folder/Law - In Use/Student Assistant Test Edit Folder",
               ]
for path in common_paths:
    menu.add_command(label=path, command=lambda p=path: select_common_path(p))

# Room number
tk.Label(root, text="Room Number:").grid(row=3, column=0, padx=10, pady=5)
room_number_entry = tk.Entry(root)
room_number_entry.grid(row=3, column=1, padx=10, pady=5)

# Title
tk.Label(root, text="Title:").grid(row=4, column=0, padx=10, pady=5)
title_entry = tk.Entry(root)
title_entry.grid(row=4, column=1, padx=10, pady=5)

# Start date
tk.Label(root, text="Start Date (MM/DD/YYYY):").grid(row=5, column=0, padx=10, pady=5)
start_month_entry = tk.Entry(root, width=5)
start_month_entry.grid(row=5, column=1, padx=10, pady=5, sticky='w')
start_day_entry = tk.Entry(root, width=5)
start_day_entry.grid(row=5, column=1, padx=10, pady=5)
start_year_entry = tk.Entry(root, width=5)
start_year_entry.grid(row=5, column=1, padx=10, pady=5, sticky='e')

# Start time
tk.Label(root, text="Start Time (HH:MM):").grid(row=6, column=0, padx=10, pady=5)
start_hour_entry = tk.Entry(root, width=5)
start_hour_entry.grid(row=6, column=1, padx=10, pady=5, sticky='w')
start_minute_entry = tk.Entry(root, width=5)
start_minute_entry.grid(row=6, column=1, padx=10, pady=5)

am_pm_var = tk.StringVar()
am_pm_var.set("AM")

# Toggle function for AM/PM
def toggle_am_pm():
    current_value = am_pm_var.get()
    new_value = "PM" if current_value == "AM" else "AM"
    am_pm_var.set(new_value)

# Button to toggle between AM and PM
am_pm_button = tk.Button(root, textvariable=am_pm_var, command=toggle_am_pm, width=4)
am_pm_button.grid(row=6, column=1, padx=5, pady=5, sticky='e')

# Duration
tk.Label(root, text="Duration (HH:MM):").grid(row=7, column=0, padx=10, pady=5)
duration_hour_entry = tk.Entry(root, width=5)
duration_hour_entry.grid(row=7, column=1, padx=10, pady=5, sticky='w')
duration_minute_entry = tk.Entry(root, width=5)
duration_minute_entry.grid(row=7, column=1, padx=10, pady=5)

# Recurring
tk.Label(root, text="Recurring:").grid(row=8, column=0, padx=10, pady=5)
recurring_var = tk.StringVar(value="n")
tk.Radiobutton(root, text="Yes", variable=recurring_var, value="y", command=toggle_recurring_fields).grid(row=8, column=1, padx=10, pady=5, sticky='w')
tk.Radiobutton(root, text="No", variable=recurring_var, value="n", command=toggle_recurring_fields).grid(row=8, column=1, padx=10, pady=5, sticky='e')

# Recurring end date
recurring_end_date_label = tk.Label(root, text="End Date (MM/DD/YYYY):")
recurring_end_date_label.grid(row=9, column=0, padx=10, pady=5)
recurring_end_month_entry = tk.Entry(root, width=5)
recurring_end_month_entry.grid(row=9, column=1, padx=10, pady=5, sticky='w')
recurring_end_day_entry = tk.Entry(root, width=5)
recurring_end_day_entry.grid(row=9, column=1, padx=10, pady=5)
recurring_end_year_entry = tk.Entry(root, width=5)
recurring_end_year_entry.grid(row=9, column=1, padx=10, pady=5, sticky='e')

# Recurring days frame
recurring_days_frame = tk.Frame(root)
recurring_days_frame.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

days_of_week = ["M", "T", "W", "R", "F"]  # Days of the week
recurring_days_vars = []
for index, day in enumerate(days_of_week):
    day_var = tk.StringVar(value="0")
    tk.Checkbutton(recurring_days_frame, text=day, variable=day_var, onvalue="1", offvalue="0").grid(row=0, column=index, padx=0, pady=5, sticky='w')
    recurring_days_vars.append(day_var)

# Initial state of recurring fields
toggle_recurring_fields()

# Buttons
tk.Button(root, text="Start Bot", command=start_bot).grid(row=11, column=0, padx=10, pady=10)
tk.Button(root, text="Quit", command=quit_app).grid(row=11, column=1, padx=10, pady=10)

root.mainloop()
