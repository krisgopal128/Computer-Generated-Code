import tkinter as tk
import datetime
import time
import winsound

alarms = []


def set_alarm():
    global alarms
    alarm_time = f"{hour_var.get()}:{minute_var.get()}"
    repeat_days = [day.get() for day in repeat_vars if day.get()]
    alarms.append((alarm_time, repeat_days))
    update_alarm_label()


def trigger_alarm():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_day = now.weekday()
    for alarm_time, repeat_days in alarms:
        if current_time == alarm_time and (not repeat_days or current_day in repeat_days):
            alarm_popup()
            winsound.PlaySound("SystemExit", winsound.SND_ALIAS)  # Play alarm sound
            if not repeat_days:
                # Remove alarm if not recurring
                alarms.remove((alarm_time, repeat_days))
            update_alarm_label()
            break
    window.after(1000, trigger_alarm)  # Check again after 1 second


def alarm_popup():
    popup = tk.Toplevel()
    popup.title("Alarm!")
    message = tk.Label(popup, text="Time's up!")
    message.pack()

    okay_button = tk.Button(popup, text="Okay", command=popup.destroy)
    okay_button.pack()

    snooze_button_5 = tk.Button(popup, text="Snooze 5 mins", command=lambda: snooze_alarm(popup, 5))
    snooze_button_5.pack()

    snooze_button_10 = tk.Button(popup, text="Snooze 10 mins", command=lambda: snooze_alarm(popup, 10))
    snooze_button_10.pack()

    snooze_button_15 = tk.Button(popup, text="Snooze 15 mins", command=lambda: snooze_alarm(popup, 15))
    snooze_button_15.pack()


def snooze_alarm(popup, minutes):
    global alarms
    alarm_time = (datetime.datetime.now() + datetime.timedelta(minutes=minutes)).strftime("%H:%M")
    alarms.append((alarm_time, []))  # Add snoozed alarm as a non-recurring alarm
    update_alarm_label()
    popup.destroy()


def update_alarm_label():
    alarm_label.config(text="Alarms set for: " + ", ".join([f"{alarm_time} ({', '.join([days[day] for day in repeat_days])})" if repeat_days else alarm_time for alarm_time, repeat_days in alarms]))


# --- GUI Setup ---
window = tk.Tk()
window.title("Alarm Clock")

# Use a more modern font
window.option_add("*Font", "Helvetica 12")

# Set a background color
window.configure(bg="#f0f0f0")

# --- Description Label ---
description_label = tk.Label(window, text="Time in HH:MM      Day:", bg="#f0f0f0")
description_label.grid(row=0, column=0, columnspan=2)  # Use grid layout

# --- Hour Dropdown ---
hour_var = tk.StringVar(window)
hour_options = [str(i).zfill(2) for i in range(24)]  # 00, 01, 02, ..., 23
hour_dropdown = tk.OptionMenu(window, hour_var, *hour_options)
hour_dropdown.grid(row=1, column=0)  # Use grid layout

# --- Minute Dropdown ---
minute_var = tk.StringVar(window)
minute_options = [str(i).zfill(2) for i in range(60)]  # 00, 01, 02, ..., 59
minute_dropdown = tk.OptionMenu(window, minute_var, *minute_options)
minute_dropdown.grid(row=1, column=1)  # Use grid layout

repeat_vars = []
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for i, day in enumerate(days):
    var = tk.BooleanVar(window)
    repeat_vars.append(var)
    checkbutton = tk.Checkbutton(window, text=day, variable=var, bg="#f0f0f0")
    checkbutton.grid(row=i+2, column=0, sticky="w")  # Use grid layout for vertical arrangement

set_button = tk.Button(window, text="Set Alarm", command=set_alarm, bg="#4CAF50", fg="white")
set_button.grid(row=9, column=0, columnspan=2)  # Use grid layout for button placement

alarm_label = tk.Label(window, text="", bg="#f0f0f0")
alarm_label.grid(row=10, column=0, columnspan=2)  # Use grid layout for label placement

trigger_alarm()  # Start the alarm checking process

window.mainloop()
