from rebalancing_functions import *

ex_1 = {'id': 1, 'project_id': 1, 'section_id': 0, 'order': 1, 'content': '', 'completed': True, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-02-18T01:55:49Z', 'url': 'https://todoist.com/showTask?id=1'}
ex_2 = {'id': 2, 'project_id': 1, 'section_id': 0, 'order': 3, 'content': 'rescheduled:2', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-02-18T02:09:49Z', 'url': 'https://todoist.com/showTask?id=2'}
ex_3 = {'id': 3, 'project_id': 1, 'section_id': 0, 'order': 2, 'content': '', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-02-18T02:17:50Z', 'url': 'https://todoist.com/showTask?id=3'}
ex_4 = {'id': 4, 'project_id': 1, 'section_id': 0, 'order': 4, 'content': '', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-02-18T16:49:31Z', 'url': 'https://todoist.com/showTask?id=4'}
ex_5 = {'id': 5, 'project_id': 1, 'section_id': 0, 'order': 5, 'content': 'rescheduled:3', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-02-21T17:53:19Z', 'url': 'https://todoist.com/showTask?id=5'}
ex_6 = {'id': 6, 'project_id': 1, 'section_id': 0, 'order': 6, 'content': '', 'completed': True, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-02-18T01:55:49Z', 'url': 'https://todoist.com/showTask?id=6'}
ex_7 = {'id': 7, 'project_id': 1, 'section_id': 0, 'order': 7, 'content': '', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-03-18T02:09:49Z', 'url': 'https://todoist.com/showTask?id=7'}
ex_8 = {'id': 8, 'project_id': 1, 'section_id': 0, 'order': 8, 'content': '', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-03-18T02:17:50Z', 'url': 'https://todoist.com/showTask?id=8'}
ex_9 = {'id': 9, 'project_id': 1, 'section_id': 0, 'order': 9, 'content': '', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-03-18T16:49:31Z', 'url': 'https://todoist.com/showTask?id=9'}
ex_10 = {'id': 10, 'project_id': 1, 'section_id': 0, 'order': 10, 'content': '', 'completed': False, 'label_ids': [], 'priority': 1, 'comment_count': 0, 'created': '2020-03-21T17:53:19Z', 'url': 'https://todoist.com/showTask?id=10'}

five_tasks = [ex_1, ex_2, ex_3, ex_4, ex_5]
ten_tasks = [ex_1, ex_2, ex_3, ex_4, ex_5, ex_6, ex_7, ex_8, ex_9, ex_10]

# completion unit tests
state_1 = [ex_2, ex_3]
state_2 = [ex_3, ex_4]

def test_incomplete():
    assert len(get_incomplete(five_tasks)) == 4

def test_fifo():
    """
    In the order that they are received, assign a due date
    (with a low daily threshold) to generate a new calendar of delivery.
    """
    incompleted_items = get_incomplete(five_tasks)
    fifo_reordering = scheduler_reorder(incompleted_items, method = "fifo")
    new_order = [x["id"] for x in fifo_reordering]
    assert new_order == [3, 2, 4, 5]

def test_fifo_order():
    incompleted_items = get_incomplete(five_tasks)
    fifo_reordering = scheduler_reorder(incompleted_items, method = "fifo")
    new_priority = reassign_order(fifo_reordering)
    reorder = [x["order"] for x in new_priority]
    assert reorder == [1, 2, 3, 4]

def test_lifo():
    incompleted_items = get_incomplete(five_tasks)
    fifo_reordering = scheduler_reorder(incompleted_items, method = "lifo")
    new_order = [x["id"] for x in fifo_reordering]
    assert new_order == [5, 4, 2, 3]

def test_lifo_order():
    incompleted_items = get_incomplete(five_tasks)
    lifo_reordering = scheduler_reorder(incompleted_items, method = "lifo")
    new_priority = reassign_order(lifo_reordering)
    reorder = [x["order"] for x in new_priority]
    assert reorder == [1, 2, 3, 4]

def test_new_cal_fifo():
    incompleted_items = get_incomplete(five_tasks)
    fifo_reordering = scheduler_reorder(incompleted_items, method = "fifo")
    new_priority = reassign_order(fifo_reordering)

def test_new_cal_lifo():
    incompleted_items = get_incomplete(five_tasks)
    lifo_reordering = scheduler_reorder(incompleted_items, method = "lifo")
    new_priority = reassign_order(lifo_reordering)
    new_cal = new_calendar(new_priority, threshold = 1, start = "2020-01-01")
    assert [x["due"]["date"] for x in new_cal] == ['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04']

def test_ten_tasks_order():
    incompleted_items = get_incomplete(ten_tasks)
    lifo_reordering = scheduler_reorder(incompleted_items, method = "lifo")
    new_priority = reassign_order(lifo_reordering)
    reorder = [x["order"] for x in new_priority]
    assert reorder == [1 + x for x in range(8)]

def test_ten_tasks_comment_number():
    incompleted_items = get_incomplete(five_tasks)
    lifo_reordering = scheduler_reorder(incompleted_items, method = "lifo")
    new_priority = reassign_order(lifo_reordering)
    new_cal = new_calendar(new_priority, threshold = 1, start = "2020-01-01")
    new_com = [x["content"] for x in new_cal]
    assert new_com == ['rescheduled:2', 'rescheduled:4', 'rescheduled:2', 'rescheduled:5']

def test_five_rpfo():
    incompleted_items = get_incomplete(five_tasks)
    lifo_reordering = scheduler_reorder(incompleted_items, method = "rpfo")
    new_priority = reassign_order(lifo_reordering)
    reorder = [x["order"] for x in new_priority]
    assert reorder == [1, 2, 3, 4]
