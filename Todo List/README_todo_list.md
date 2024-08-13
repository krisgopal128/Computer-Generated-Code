# To-Do List Application

## Requirements:

- Python 3.x
- Tkinter library (usually included with Python)
- `tkcalendar` module (`pip install tkcalendar`)

## Features:

1. **Task Management**:
   - Add tasks with a description, due date, priority, and category.
   - Edit tasks with updated information.
   - Mark tasks as completed.
   - Delete tasks from the list.

2. **GUI Components**:
   - Task Entry: Input for the task description.
   - Date Picker: Select a due date for each task.
   - Priority Dropdown: Choose the priority level (High, Medium, Low).
   - Category Dropdown: Select a category (Work, Personal, Errands, Other).
   - Task List: Display tasks in a table with columns for Task, Due Date, Priority, Category, and Completed status.
   - Buttons: Add, complete, delete tasks, and save changes when editing.

3. **Data Persistence**:
   - Tasks are saved in a `pickle` file (`tasks.pickle`), allowing them to be loaded when the application is restarted.

## How to Use:

### Launch the Application:

1. Run the Python script `todo_list.py`.
2. The main window will open, displaying input fields for tasks, a date picker, priority, and category options.

### Add a Task:

1. Enter the task description in the "Task" field.
2. Choose a due date using the Date Picker.
3. Select a priority (High, Medium, Low) from the dropdown menu.
4. Select a category (Work, Personal, Errands, Other) from the dropdown menu.
5. Click the "Add Task" button to add the task to the list.

### Edit a Task:

1. Double-click on a task in the list to open the edit window.
2. Modify the task description, due date, priority, or category as needed.
3. Click "Save Changes" to update the task.

### Complete a Task:

1. Select a task from the list.
2. Click the "Complete Task" button to toggle the completion status.

### Delete a Task:

1. Select a task from the list.
2. Click the "Delete Task" button to remove the task.

### Data Persistence:

- All tasks are saved in a file named `tasks.pickle` whenever changes are made.
- When the application is reopened, it will load tasks from this file automatically.

Code generated on gemma-1.5-pro-exp-0801 & gemma-1.5-pro-latest dated 13-Aug-2024