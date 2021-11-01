
# Import custom pipeline functions
from pipeline.refresh_all_tasks import daily_refresh
from pipeline.functions.parse_tasks import *

# refresh all tasks
daily_task_threshold = 5
daily_refresh(daily_task_threshold)
