import tkinter as tk
from tkinter import ttk
import datetime
import pickle
from tkcalendar import DateEntry

class ToDoList:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")

        self.tasks = []
        self.load_tasks()

        self.create_widgets()

    def create_widgets(self):
        self.task_entry = tk.Entry(self.master, width=50)
        self.task_entry.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Date Picker
        self.due_date_entry = DateEntry(self.master, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.due_date_entry.grid(row=1, column=0, padx=10, pady=10)

        # Priority Dropdown
        self.priority_var = tk.StringVar(self.master)
        self.priority_var.set("Medium")  # Default priority
        priority_options = ["High", "Medium", "Low"]
        self.priority_dropdown = tk.OptionMenu(self.master, self.priority_var, *priority_options)
        self.priority_dropdown.grid(row=1, column=1, padx=10, pady=10)

        # Category Dropdown
        self.category_var = tk.StringVar(self.master)
        self.category_var.set("General")  # Default category
        category_options = ["Work", "Personal", "Errands", "Other"]
        self.category_dropdown = tk.OptionMenu(self.master, self.category_var, *category_options)
        self.category_dropdown.grid(row=1, column=2, padx=10, pady=10)

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=3, padx=10, pady=10)

        self.task_list = ttk.Treeview(self.master, columns=("Task", "Due Date", "Priority", "Category", "Completed"), show="headings")
        self.task_list.heading("Task", text="Task")
        self.task_list.heading("Due Date", text="Due Date")
        self.task_list.heading("Priority", text="Priority")
        self.task_list.heading("Category", text="Category")
        self.task_list.heading("Completed", text="Completed")
        self.task_list.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        self.task_list.bind("<Double-1>", self.edit_task)

        self.complete_button = tk.Button(self.master, text="Complete Task", command=self.complete_task)
        self.complete_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.delete_button = tk.Button(self.master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=5, column=2, columnspan=2, padx=10, pady=10)

        self.refresh_list()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            due_date = self.due_date_entry.get_date()
            priority = self.priority_var.get()
            category = self.category_var.get()
            completed = False
            self.tasks.append((task, due_date, priority, category, completed))
            self.task_entry.delete(0, tk.END)
            self.refresh_list()
            self.save_tasks()

    def refresh_list(self):
        for item in self.task_list.get_children():
            self.task_list.delete(item)
        for task in self.tasks:
            self.task_list.insert("", tk.END, values=task)

    def complete_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            item_id = selected_item[0]
            index = self.task_list.index(item_id)
            self.tasks[index] = (self.tasks[index][0], self.tasks[index][1], self.tasks[index][2], self.tasks[index][3], not self.tasks[index][4])
            self.refresh_list()
            self.save_tasks()

    def delete_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            item_id = selected_item[0]
            self.tasks.pop(self.task_list.index(item_id))
            self.task_list.delete(item_id)
            self.save_tasks()

    def edit_task(self, event):
        selected_item = self.task_list.selection()
        if selected_item:
            item_id = selected_item[0]
            task = self.task_list.item(item_id, "values")
            self.edit_window = tk.Toplevel(self.master)
            self.edit_window.title("Edit Task")

            task_label = tk.Label(self.edit_window, text="Task:")
            task_label.grid(row=0, column=0, padx=10, pady=10)

            self.edit_task_entry = tk.Entry(self.edit_window, width=50)
            self.edit_task_entry.insert(0, task[0])
            self.edit_task_entry.grid(row=0, column=1, padx=10, pady=10)

            due_date_label = tk.Label(self.edit_window, text="Due Date:")
            due_date_label.grid(row=1, column=0, padx=10, pady=10)

            self.edit_due_date_entry = DateEntry(self.edit_window, width=12, background='darkblue',
                                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            self.edit_due_date_entry.set_date(task[1])
            self.edit_due_date_entry.grid(row=1, column=1, padx=10, pady=10)

            priority_label = tk.Label(self.edit_window, text="Priority:")
            priority_label.grid(row=2, column=0, padx=10, pady=10)

            self.edit_priority_var = tk.StringVar(self.edit_window)
            self.edit_priority_var.set(task[2])
            priority_options = ["High", "Medium", "Low"]
            self.edit_priority_dropdown = tk.OptionMenu(self.edit_window, self.edit_priority_var, *priority_options)
            self.edit_priority_dropdown.grid(row=2, column=1, padx=10, pady=10)

            category_label = tk.Label(self.edit_window, text="Category:")
            category_label.grid(row=3, column=0, padx=10, pady=10)

            self.edit_category_var = tk.StringVar(self.edit_window)
            self.edit_category_var.set(task[3])
            category_options = ["Work", "Personal", "Errands", "Other"]  # Add your desired categories here
            self.edit_category_dropdown = tk.OptionMenu(self.edit_window, self.edit_category_var, *category_options)
            self.edit_category_dropdown.grid(row=3, column=1, padx=10, pady=10)

            save_button = tk.Button(self.edit_window, text="Save Changes", command=lambda: self.save_edited_task(item_id, task))
            save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def save_edited_task(self, item_id, original_task):
        index = self.task_list.index(item_id)
        updated_task = (
            self.edit_task_entry.get(),
            self.edit_due_date_entry.get_date(),
            self.edit_priority_var.get(),
            self.edit_category_var.get(),
            self.tasks[index][4]  # Keep the original 'Completed' status
        )
        self.tasks[index] = updated_task
        self.refresh_list()
        self.save_tasks()
        self.edit_window.destroy()

    def save_tasks(self):
        with open("tasks.pickle", "wb") as f:
            pickle.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open("tasks.pickle", "rb") as f:
                self.tasks = pickle.load(f)
        except FileNotFoundError:
            pass

root = tk.Tk()
todo_list = ToDoList(root)
root.mainloop()
