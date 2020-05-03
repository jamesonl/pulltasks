from functools import partial
from operator import is_not
from datetime import date, timedelta, datetime
import time

def calendar_schedule_allocator(task, task_limit, threshold):
    '''determine the next available date to allocate the task'''
    calendar_days = list(task_limit.keys())
    calendar_days.sort()
    for cd in calendar_days:
        if task_limit[cd] < threshold:
            return cd

def get_current_calendar(tasks, threshold, start = "today", method = "blank"):
    # this is used to either create a blank slate or provide the current
    # breakdown of tasks as they exist today
    if start == "today":
        today = date(datetime.now().year, datetime.now().month, datetime.now().day)
    else:
        split_date = start.split("-")
        pdf = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        today = date(pdf.year, pdf.month, pdf.day)

    task_allocation = {}
    forward_range_days = int(round(len(tasks) / threshold, 0)) + 1
    forward_range = today + timedelta(days=forward_range_days)
    dd = forward_range - today
    calendar_dates = [today + timedelta(days=i) for i in range(dd.days + 1)]
    allocated_task_ids = []

    if method == "blank":
        for cd in calendar_dates:
            smart_date = cd.strftime("%Y-%m-%d")
            task_allocation[smart_date] = 0
    elif method == "current":
        for task in tasks:
            tdd = task["due"]["date"]
            if tdd in task_allocation.keys():
                task_allocation[tdd] += 1
            else:
                task_allocation[tdd] = 1

    return [task_allocation, calendar_dates]


def new_calendar(tasks, threshold, start = "today"):
    updated_tasks = []
    task_limit = get_current_calendar(tasks, threshold, start, method = "blank")

    cd_counter = 0
    for task in tasks:
        bootstrap = task_limit[1][cd_counter].strftime("%Y-%m-%d")
        new_due_date = calendar_schedule_allocator(task, task_limit[0], threshold)
        task_limit[0][new_due_date] += 1
        task["due"] = {"date": new_due_date}
        updated_tasks.append(task)

    return updated_tasks

def reassign_order(tasks):
    counter = 1
    for t in tasks:
        t["order"] = counter
        counter += 1
    return tasks

def get_incomplete(task_list):
    incomplete_cat = [x if x["completed"] == False else None for x in task_list]
    incomplete_list = [i for i in incomplete_cat if i is not None]
    return incomplete_list

def scheduler_reorder(tasks, method = "lifo"):
    """
    Overview:
    Given a certain threshold, distribute tasks from a queue across a calendar.

    Acceptance Criteria:
     - must be flexible for rescheduling 3 kinds of test cases:
        - LIFO
        - FIFO
        - SRTF
    """
    augmented_items = None
    rev_bool = False if method == "fifo" else True

    if method == "fifo" or method == "lifo":
        augmented_items = sorted(tasks, key=lambda k: k['order'], reverse=rev_bool)
    elif method == "srft":
        pass
    else:
        pass

    return augmented_items
