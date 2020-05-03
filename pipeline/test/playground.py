from test_rebalancing import *

incompleted_items = get_incomplete(five_tasks)
lifo_reordering = scheduler_reorder(incompleted_items, method = "rpfo")
new_priority = reassign_order(lifo_reordering)
reorder = [x["order"] for x in new_priority]
print(reorder)
