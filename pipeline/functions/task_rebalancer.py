import random
import requests
import json
import uuid
import todoist
import time
from collections import OrderedDict
from datetime import datetime, timedelta
from .rebalancing_functions import calendar_schedule_allocator, new_calendar, reassign_order, get_incomplete, scheduler_reorder


with open(".secret") as file:
    api_token = str(file.read().strip("\n"))
file.close()

def get_projects(api_token):
    data = {
              "token": api_token,
              "sync_token": "*",
              "resource_types": ["projects"]
           }
    response = requests.post("https://api.todoist.com/sync/v8/sync", data=data)
    return response

# get_projects()
def get_active_tasks(api_token):
    headers = {"Authorization": "Bearer " + str(api_token)}

    response = requests.get("https://api.todoist.com/rest/v1/tasks", headers=headers)
    return response

def create_task_test(api_token):
    temp_uuid = str(uuid.uuid4()).upper()
    headers = {
        'Content-Type': 'application/json',
        'X-Request-Id': '$(' + temp_uuid + ')',
        'Authorization': 'Bearer ' + str(api_token),
    }

    # template
    data = '{"content": "Appointment with Pedro", "due_string": "today", "due_lang": "en", "priority": 4}'

    response = requests.post('https://api.todoist.com/rest/v1/tasks', headers=headers, data=data)

    return response

def get_unassigned_tasks(task_list):
    unassigned_tasks = []
    for x in task_list:
        if "due" in x.keys():
            pass
        else:
            unassigned_tasks.append(x)
    return unassigned_tasks

def assign_date(all_tasks, task, api_token):
    temp_uuid = str(uuid.uuid4()).upper()

    headers = {
        'Content-Type': 'application/json',
        'X-Request-Id': '$(' + temp_uuid + ')',
        'Authorization': 'Bearer ' + str(api_token),
    }

    task["due_str"] = "today"
    task_num = str(task["id"])
    update_info = {"task_id": task["id"], "content": task["content"], "date_str": "today"}
    api_task_address = 'https://api.todoist.com/rest/v1/tasks/' + task_num

    response = requests.post(api_task_address, headers=headers, data=update_info)
    return dir(response)

def get_single_task(task, api_token):
    headers = {"Authorization": "Bearer " + str(api_token)}
    task_num = task["id"]
    api_task_address = 'https://api.todoist.com/rest/v1/tasks/' + str(task_num)
    response = requests.get(api_task_address, headers=headers)
    return response.text

def update_single_task(api_token, task_id, target_date):
    temp_uuid = str(uuid.uuid4()).upper()
    headers = {
        'Content-Type': 'application/json',
        'X-Request-Id': '$(' + temp_uuid + ')',
        'Authorization': 'Bearer ' + str(api_token),
    }

    update_info = '{"due_date": ' + "\"" + target_date + "\"}"
    api_task_address = 'https://api.todoist.com/rest/v1/tasks/' + str(task_id)
    response = requests.post(api_task_address, headers=headers, data=update_info)
    return response.text

def scheduling_balancer(all_tasks, threshold = 5):
    # count the unassigned tasks by date
    cal_tasks = {}
    today = datetime.now()
    print("total tasks: ", str(len(all_tasks)))

    for task in all_tasks:
        try:
            due_date_info = task["due"]["date"]
        except:
            task["due"] = {"date":today.strftime("%Y-%m-%d")}

        if due_date_info not in cal_tasks.keys():
            cal_tasks[due_date_info] = 1
        else:
            cal_tasks[due_date_info] += 1

    risk_dates = []
    for workload in cal_tasks.keys():
        if cal_tasks[workload] > threshold:
            risk_dates.append(workload)

    # push tasks forward one by one
    days_to_complete = int(len(all_tasks) / threshold) + 1
    new_task_schedule = {}
    min_date = min(cal_tasks.keys()).split("-")

    smin = (int(min_date[0]), int(min_date[1]), int(min_date[2]))
    sdate = datetime(*smin)
    max_date = max(cal_tasks.keys()).split("-")

    emax = int(max_date[0]), int(max_date[1]), int(max_date[2])
    edate = datetime(*emax) + timedelta(days = days_to_complete)
    delta = edate - sdate

    date_range = [(sdate + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(delta.days + 1)]

    reassignment = OrderedDict()
    # create a list of all the dates in the upcoming days that I
    # expect to reallocate tasks
    for point in date_range:
        reassignment[point] = []

    # for each task, find the day that makes the most sense to allocate
    for point in date_range:
        for tt in all_tasks:
            if point in risk_dates:
                if tt["due"]["date"] == point and point in risk_dates and cal_tasks[point] > threshold:
                    tcs = point.split("-")
                    temp_date_obj = datetime(int(tcs[0]), int(tcs[1]), int(tcs[2]))
                    if temp_date_obj < today:
                        reassignment_date = today + timedelta(days = random.randint(1,10))
                        reassignment[today.strftime("%Y-%m-%d")].append(tt)
                    else:
                        reassignment_date = temp_date_obj + timedelta(days = random.randint(1,10))
                        reassignment[reassignment_date.strftime("%Y-%m-%d")].append(tt)

                else:
                    if tt["due"]["date"] == point and cal_tasks[point] < threshold:
                        if temp_date_obj < today:
                            reassignment_date = today
                            reassignment[today.strftime("%Y-%m-%d")].append(tt)
                        else:
                            reassignment[point].append(tt)
            else:
                if tt["due"]["date"] == point:
                    tcs = point.split("-")
                    temp_date_obj = datetime(int(tcs[0]), int(tcs[1]), int(tcs[2]))
                    if temp_date_obj <= today:
                        reassignment_date = today
                        reassignment[today.strftime("%Y-%m-%d")].append(tt)
                    else:
                        reassignment[point].append(tt)

    # convert reassignment back to a flat list of tasks
    flat_list = []
    for ra in reassignment:
        obj_list = reassignment[ra]
        if len(obj_list) == 0:
            pass
        else:
            for obj in obj_list:
                obj["due"] = {"date":ra}
                flat_list.append(obj)

    if len(risk_dates) == 0:
        pass
    else:
        # print("reassignment rules insufficient... entering loop")
        distributed_ra = scheduling_balancer(flat_list, threshold)

    return flat_list

def taskrefresher(tasks, threshold, method = "lifo"):
    reordered_tasks = scheduler_reorder(tasks, method)
    new_priority = reassign_order(reordered_tasks)
    new_cal = new_calendar(new_priority, threshold = 10)
    return new_cal

# credit: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def taskupdater(new_cal, ntasks, throttle = 50):
    # the todoist api throttles calls by 50, so I will adjust my rescheduler to
    # only make 50 calls per minute.

    binned_tasks = list(divide_chunks(new_cal, 50))

    print("Total bins: ", str(len(binned_tasks)))
    bin_num = 1
    for bin in binned_tasks:
        for tt in bin:
            # print("updated: ", str([tt["id"], tt["content"], tt["due"]["date"]]))
            update_single_task(api_token, tt["id"], tt["due"]["date"])
        print("Completed Bin: ", str(bin_num))
        bin_num += 1
        time.sleep(60)

    updated_tasks = len(new_cal)
    return "updated tasks: {%s}" % (updated_tasks)
