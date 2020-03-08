from task_rebalancer import *
import time
import datetime

starttime = time.time()

iter_num = 1
print("started process at: ", str(datetime.datetime.now()))

while True:
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))
    # refresh()
    print("Refresh Num: " + str(iter_num) + ", Running for: " + str(round((time.time() - starttime) / 60, 2)) + " minutes")
    iter_num += 1
