#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      HP-PC
#
# Created:     03-08-2024
# Copyright:   (c) HP-PC 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# importing the required modules
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

# defining the function to add tasks to the list
def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        # adding the string to the tasks list
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string ,))
        list_update()
        task_field.delete(0, 'end')

# defining the function to update the list
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

# defining the function to delete a task from the list
def delete_task():
    # using the try-except method
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

# function to delete all tasks from the list
def delete_all_tasks():
    message_box = messagebox.askyesno('Delete all', 'Are you sure?')
    if message_box == True:
        while(len(tasks) != 0):
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()

# function to clear the list
def clear_list():
    task_listbox.delete(0, 'end')

# function to close the application
def close():
    print(tasks)
    guiWindow.destroy()

# function to retrieve data from the database
def retrieve_database():
    while(len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

# main function
if __name__ == "__main__":
    guiWindow =tk.Tk()
    guiWindow.title("To-Do List Manager - JAVATPOINT")
    guiWindow.geometry("500x450+750+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg = "#B5E5CF")

    # using the connect() method to connect to the database
    the_connection = sql.connect('listOfTasks.db')
    # creating the cursor object of the cursor class
    the_cursor = the_connection.cursor()
    # using the execute() method to execute a SQL statement
    the_cursor.execute('create table if not exists tasks (title text)')

    # defining an empty list
    tasks = []

    # defining frames using the tk.Frame() widget
    header_frame = tk.Frame(guiWindow, bg = "Black")
    functions_frame = tk.Frame(guiWindow, bg = "Black")
    listbox_frame = tk.Frame(guiWindow, bg = "Black")

    # using the pack() method to place the frames in the application
    header_frame.pack(fill = "both")
    functions_frame.pack(side = "left", expand = True, fill = "both")
    listbox_frame.pack(side = "right", expand = True, fill = "both")

    # defining a label using the ttk.Label() widget
    header_label = ttk.Label(
        header_frame,
        text = "The To-Do List",
        font = ("Brush Script MT", "30"),
        background = "Black",
        foreground = "#ed1a21"
    )
    # using the pack() method to place the label in the application
    header_label.pack(padx = 20, pady = 20)

    # defining another label using the ttk.Label() widget
    task_label = ttk.Label(
        functions_frame,
        text = "Enter the Task:",
        font = ("Brush Script MT", "15", "bold"),
        background = "Black",
        foreground = "Red"
    )
    # using the place() method to place the label in the application
    task_label.place(x = 30, y = 40)

    # defining an entry field using the ttk.Entry() widget
    task_field = ttk.Entry(
        functions_frame,
        font = ("Consolas", "11"),
        width = 18,
        background = "White",
        foreground = "Red"
    )
    # using the place() method to place the entry field in the application
    task_field.place(x = 30, y = 80)

    # adding buttons to the application using the ttk.Button() widget
    add_button = ttk.Button(
        functions_frame,
        text = "Add Task",
        width = 24,
        command = add_task
    )
    remove_button = ttk.Button(
        functions_frame,
        text = "Remove Task",
        width = 24,
        command = delete_task
    )
    remove_all_button = ttk.Button(
        functions_frame,
        text = "Remove All Tasks",
        width = 24,
        command = delete_all_tasks
    )
    exit_button = ttk.Button(
        functions_frame,
        text = "Exit",
        width = 24,
        command = close
    )
    # using the place() method to set the position of the buttons in the application
    add_button.place(x = 30, y = 120)
    remove_button.place(x = 30, y = 160)
    remove_all_button.place(x = 30, y = 200)
    exit_button.place(x = 30, y = 240)

    # defining a list box using the tk.Listbox() widget
    task_listbox = tk.Listbox(
        listbox_frame,
        width = 26,
        height = 13,
        selectmode = 'SINGLE',
        background = "White",
        foreground = "Black",
        selectbackground = "Red",
        selectforeground = "White"
    )
    # using the place() method to place the list box in the application
    task_listbox.place(x = 10, y = 20)

    # calling some functions
    retrieve_database()
    list_update()
    # using the mainloop() method to run the application
    guiWindow.mainloop()
    # establishing the connection with database
    the_connection.commit()
    the_cursor.close()