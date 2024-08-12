# User Guide for Alarm Clock

## Requirements:
- Python 3.x
- Tkinter library (usually included with Python)
- `winsound` module for playing alarm sound (available on Windows)

## How to Use:

### Launch the Application:
1. Run the Python script (`alarm_clock.py`).

### Setting an Alarm:
1. Select the hour and minute for the alarm using the dropdowns.
2. Optionally, choose the days on which the alarm should repeat by checking the boxes for "Mon," "Tue," "Wed," etc.
3. Click the "Set Alarm" button to set the alarm.

### Alarm Notifications:
- When the alarm time is reached, a popup window will appear with the message "Time's up!"
- The alarm sound will play.

### Snoozing:
- The popup offers three snooze options: 5, 10, and 15 minutes.
- Click the corresponding button to snooze the alarm for the selected duration.

### Alarm Management:
- Non-recurring alarms will automatically be removed after they trigger.
- Recurring alarms will continue to activate on the specified days.

## Customization:
- The application uses a modern font and background color for a clean interface.
- The "Alarms set for:" label displays all currently set alarms.

Code generated on gemma-1.5-pro-exp-0801 dated 10-Aug-2024