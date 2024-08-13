# Input:



Create a To-Do List application with a graphical user interface (GUI) using Python and the Tkinter library. The application should include the following features:



# Features:



### Task Management:

- **Add Task**: Users can add a new task by entering the task name in the text entry field. Each task should have the following attributes:

  - **Due Date**: A date picker to select the task's due date.

  - **Priority**: A dropdown menu to select the task's priority (High, Medium, Low).

  - **Category**: A dropdown menu to categorize the task (Work, Personal, Errands, Other).



- **Task List**: Tasks are displayed in a list with columns for Task Name, Due Date, Priority, Category, and Completed status.

  - **Complete Task**: Users can mark a task as completed by selecting it from the list and clicking the "Complete Task" button. The completed status will toggle between completed and not completed.

  - **Delete Task**: Users can delete a task by selecting it from the list and clicking the "Delete Task" button.

  - **Edit Task**: Users can double-click a task in the list to open an edit window where they can modify the task details (Task Name, Due Date, Priority, Category).



### Persistence:

- **Save Tasks**: Tasks are saved automatically whenever a task is added, completed, edited, or deleted. The tasks are stored in a file named `tasks.pickle` using Python's `pickle` module.

- **Load Tasks**: The application loads tasks from the `tasks.pickle` file when it starts, ensuring that the user’s tasks persist between sessions.



### GUI Layout:

- **Task Entry Field**: An entry widget for users to input the task name.

- **Date Picker**: A date entry widget for selecting the due date of the task.

- **Priority Dropdown**: A dropdown menu for selecting the task's priority.

- **Category Dropdown**: A dropdown menu for categorizing the task.

- **Buttons**:

  - "Add Task": Adds the task with the specified details to the task list.

  - "Complete Task": Marks the selected task as completed or not completed.

  - "Delete Task": Deletes the selected task from the list.



### Requirements:

- **Libraries**: Python 3.10, Tkinter, `tkcalendar`, `pickle`.

- **Environment**: The application should run on any standard Python environment with the required libraries installed.



### Code Structure:

- The application should be structured with a `ToDoList` class encapsulating the logic and GUI elements.

- Each task should be represented as a tuple containing the task name, due date, priority, category, and completed status.



### User Guide:

- **Adding a Task**: Enter the task name, select the due date, choose the priority and category, and click "Add Task".

- **Completing a Task**: Select the task from the list and click "Complete Task".

- **Editing a Task**: Double-click on a task in the list to open the edit window, make changes, and save them.

- **Deleting a Task**: Select the task from the list and click "Delete Task".



# File Generation:



Generate a single Python file named `todo_list.py` containing the complete code for the To-Do List application, incorporating all the specified features and functionality.



User Guide:



Include a concise user guide within a comment block at the end of the `todo_list.py` file. This guide should explain how to add, complete, edit, and delete tasks, as well as how the application's persistence works.



Ensure that the code is well-documented with comments explaining the purpose of each section and function.

