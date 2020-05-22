# API notes:

# Requests per Minute
# You can make a total of 50 requests per minute per user when using the
# Sync API. This can be further increased when commands are batched where
# it is possible to use up to 100 batched commands can per request,
# giving us 5000 commands in this instance.

# Import general functions
import time
import datetime
import sys
import pprint
import json
pp = pprint.PrettyPrinter(indent=4)

# Import custom functions
from functions.task_rebalancer import taskrefresher, taskupdater, get_active_tasks, api_token
from functions.rebalancing_functions import get_incomplete

# Import test data
from data.test_old_dates import test_task

# Begin the sequence for refreshing the status of tasks
starttime = time.time()
daily_task_threshold = 10

print("started process at: ", str(datetime.datetime.now()))
print("kicking off assembly of dynamic scheduling")

all_tasks = get_incomplete(json.loads(get_active_tasks(api_token).text))
ntasks = len(all_tasks)

print("There are {tasks} tasks that will be rescheduled. \
       Expected runtime is {minutes}".format(tasks = ntasks, \
                                             minutes = round(ntasks / 50, 3)))

calendar = taskrefresher(all_tasks, daily_task_threshold)
status = taskupdater(calendar, ntasks)
print(status)
