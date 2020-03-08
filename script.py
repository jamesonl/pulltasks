from task_rebalancer import *
import time
import datetime

starttime = time.time()

iter_num = 1
print("started process at: ", str(datetime.datetime.now()))

while True:
    print("Refresh Num: " + str(iter_num) + ", Running for: " + str(round((time.time() - starttime) / 60, 2)) + " minutes")
    refresh()
    iter_num += 1
    time.sleep(3600.0 - ((time.time() - starttime) % 3600.0))
