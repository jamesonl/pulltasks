from functools import partial
from operator import is_not
from datetime import date, timedelta, datetime
import time

def calendar_schedule_allocator(task, task_limit, threshold):
    '''determine the next available date to allocate the task'''
    calendar_days = task_limit.keys()
    calendar_days.sort()
    for cd in calendar_days:
        if task_limit[cd] < threshold:
            return cd

def new_calendar(tasks, threshold = 2, start = "today", forward_range_days = 60):
    if start == "today":
        today = date(datetime.now().year, datetime.now().month, datetime.now().day)
    else:
        split_date = start.split("-")
        param_date_format = date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
        today = date(param_date_format.year, param_date_format.month, param_date_format.day)

    updated_tasks = []
    task_limit = {}

    forward_range = today + timedelta(days=forward_range_days)
    delta_days = forward_range - today
    calendar_dates = [today + timedelta(days=i) for i in range(delta_days.days + 1)]
    allocated_task_ids = []

    for cd in calendar_dates:
        smart_date = cd.strftime("%Y-%m-%d")
        task_limit[smart_date] = 0

    cd_counter = 0
    for task in tasks:
        bootstrap = calendar_dates[cd_counter].strftime("%Y-%m-%d")
        new_due_date = calendar_schedule_allocator(task, task_limit, threshold)
        task_limit[new_due_date] += 1
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
