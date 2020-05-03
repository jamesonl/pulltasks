from functions.task_rebalancer import *
from functions.rebalancing_functions import *
import time
import datetime
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Begin the sequence for refreshing the status of tasks
starttime = time.time()
threshold = 10
iter_num = 1
print("started process at: ", str(datetime.datetime.now()))
print("kicking off assembly of dynamic scheduling")
calendar = taskrefresher(threshold, method = "lifo")
status = taskupdater(calendar)
