from task_rebalancer import *
import time
import datetime
import sys
starttime = time.time()

iter_num = 1
print("started process at: ", str(datetime.datetime.now()))
sys.stdout.flush()

# while True:
#     print("Refresh Num: " + str(iter_num) + ", Running for: " + str(round((time.time() - starttime) / 60, 2)) + " minutes")
#     refresh()
#     iter_num += 1
#     time.sleep(3600.0 - ((time.time() - starttime) % 3600.0))

counter = 0
single_run = 0

while True:
    if datetime.datetime.now().minute == 0 and datetime.datetime.now().microsecond == 0 and single_run == 0:
        single_run == 1
        counter += 1
        print(datetime.datetime.now())
        print("Refresh Num: " + str(iter_num) + ", Running for: " + str(round((time.time() - starttime) / 60, 2)) + " minutes")
        sys.stdout.flush()
        refresh()
        iter_num += 1
        with open("info.txt", "w") as txt:
            txt.write(str(counter))
        txt.close()
        single_run == 0
