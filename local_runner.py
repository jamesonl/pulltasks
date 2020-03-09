# from django.utils.encoding import smart_str, smart_unicode
from task_rebalancer import *
import time
import datetime
import pandas as pd
import json

start = time.time()

results = taskrefresher()

refresh_time = time.time()
print("Time to complete refresh: ", str(refresh_time - start))

# headers = ['priority', 'created', 'url', 'completed', 'section_id', 'id', 'content', 'comment_count', 'label_ids', 'project_id', 'order', 'due']
#
# data = []
#
# for task in results:
#     vals = task.values()
#     date_info = task.values()[9]["date"]
#     del vals[9]
#     new_vals = vals + [date_info]
#     val_list = [unicode(text) if isinstance(text, str) == True else unicode(text).strip("\u") for text in new_vals]
#     print(val_list)
#     data.append(val_list)
#
# df = pd.DataFrame(data, columns=headers)
#
# print(df.head(5))
# df.to_csv("task_info.csv", sep='\t', encoding='utf-8')

print(taskupdeter(results))

print("Time to complete sync: ", str(time.time() - refresh_time))
