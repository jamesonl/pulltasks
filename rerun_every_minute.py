import time
import datetime
now = time.time()

print(datetime.datetime.now())

counter = 0
single_run = 0

while True:
    if datetime.datetime.now().second % 15 == 0 and datetime.datetime.now().microsecond == 0 and single_run == 0:
        single_run == 1
        print(datetime.datetime.now())
        counter += 1
        with open("info.txt", "w") as txt:
            txt.write(str(counter))
        txt.close()
        single_run == 0
