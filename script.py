from task_rebalancer import *
import time

starttime = time.time()

iter_num = 1
while True:
    time.sleep(3600.0 - ((time.time() - starttime) % 3600.0))
    refresh()
    print("Refresh Num: " + str(iter_num) + ", Running for: " + str(round((time.time() - starttime) / 60, 2)) + " minutes")
    iter_num += 1
