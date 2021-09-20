import pickle
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox

import pyttsx3

root = tk.Tk()
root.title("Remindo")
root.iconbitmap("RemindoIcon.ico")
root.option_add('*Font', 'Arial')
root['background'] = '#d3d3d3'

voice_checked = tk.IntVar()

voice = pyttsx3.init()


# voice.say("Insert your tasks in the box below, along with a due time, and i will notify you of them!")
# voice.runAndWait()

def add_task():
    task = entry_task.get().capitalize()

    # Task must not be empty
    if task != "":
        # Task must contain a time, following 'at'
        if "at" in task:
            listbox_task.insert(tk.END, task)
            print(f"Task {task} has been entered.")
            # Delete text when task has been added
            entry_task.delete(0, tk.END)
        else:
            # Show warning when formatting is wrong ir time is missing
            tk.messagebox.showwarning(title="Warning",
                                      message="Please add a time at the end of your task.\n\nFor example: \n\n       "
                                              "'Take out dog at 12:45'")
    else:
        # Show warning is task field is empty
        tk.messagebox.showwarning(title="Warning", message="Enter a task first")


def task_completed():
    slct_task = listbox_task.curselection()[0]
    print(slct_task)
    print(''.join([u'\u0336{}'.format(c) for c in slct_task]))
    # except:
    #     tk.messagebox.showwarning(title="Warning", message="Select a task first")


def del_task():
    # If a task is selected, delete it upon pressing 'delete' button
    try:
        slct_task = listbox_task.curselection()[0]
        listbox_task.delete(slct_task)
    except:
        tk.messagebox.showwarning(title="Warning", message="Select a task first")


def load_tasks():
    # Load tasks from a .dat file containing previously saved list of tasks
    try:
        tasks = pickle.load(open("tasks.dat", "rb"))
        # Remove current tasks before loading in from savefile
        listbox_task.delete(0, tk.END)
        for task in tasks:
            listbox_task.insert(tk.END, task)
    except:
        tk.messagebox.showwarning(title="Warning", message="Cannot find task file")


def save_tasks():
    # Save current list of tasks in .dat file in working directory
    tasks = listbox_task.get(0, listbox_task.size())
    pickle.dump(tasks, open("tasks.dat", "wb"))


def get_time_from_task(task):
    # Get time from task string and convert to datetime datatype
    time = task.split("at ", 1)[1]
    datetime_time = datetime.strptime(time, '%H:%M').time()
    print(datetime_time)
    return datetime_time


frame_tasks = tk.Frame(root)
frame_tasks.pack()

listbox_task = tk.Listbox(frame_tasks, height=20, width=50)
listbox_task.pack(side=tk.LEFT)


def activate_voice_assist():
    # Voice mode is activated
    if voice_checked.get() == 1:
        return True
    # Voice mode is deactivated
    elif voice_checked.get() == 0:
        return False
    else:
        tk.messagebox.showwarning(title="Warning", message="Something went wrong")


def sound_alarm():
    tasks = listbox_task.get(0, "end")

    # Get the current time
    now = datetime.now()
    current_time = datetime.now().time()

    for task in tasks:
        # Get time and task description from tasks
        task_time = get_time_from_task(task)
        task_desc = task.split("at ", 1)[0]
        print(f"Extended by 5 minutes: {extend_by_5_mins(task_time)}")

        # Check whether task is due
        if current_time > task_time:
            if activate_voice_assist():
                # Vocally remind user of task
                voice.say(str(task_desc) + " is due!")
                voice.runAndWait()
            # Information box reminding user of task
            result = tk.messagebox.askquestion(task_desc.capitalize(),
                                               f"{task} is due! \n \n Do you want extend by 5 minutes?")
            if result == 'yes':
                print("Yes")
            else:
                pass

                # Try to schedule next check at 0 second of next minute
    delay = 60 - now.second
    root.after(delay * 1000, sound_alarm)

# Not yet implemented
def extend_by_5_mins(task_time):
   task_time += timedelta(minutes=5)
   print(task_time)


# GUI

scrollbar_tasks = tk.Scrollbar(frame_tasks)
scrollbar_tasks.pack(side=tk.RIGHT, fill=tk.Y)

listbox_task.config(yscrollcommand=scrollbar_tasks.set)
scrollbar_tasks.config(command=listbox_task.yview)

entry_task = tk.Entry(root, width=50)
entry_task.pack()

btn_add = tk.Button(root, text="Add task", width=48, command=add_task)
btn_add.pack()

btn_comp = tk.Button(root, text="Task completed", width=48, command=task_completed)
btn_comp.pack()

btn_del = tk.Button(root, text="Delete task", width=48, command=del_task)
btn_del.pack()

btn_load = tk.Button(root, text="Load tasks", width=48, command=load_tasks)
btn_load.pack()

btn_save = tk.Button(root, text="Save tasks", width=48, command=save_tasks)
btn_save.pack()

Checkbutton(root, text="Activate voice mode", variable=voice_checked, onvalue=1, offvalue=0,
            command=activate_voice_assist).pack(side=tk.BOTTOM)

sound_alarm()

root.mainloop()
