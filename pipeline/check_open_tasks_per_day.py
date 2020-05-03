from functions.task_rebalancer import *
from functions.rebalancing_functions import *
import time
import datetime
import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

all_tasks = get_incomplete(json.loads(get_active_tasks(api_token).text))
curr_tasks = get_current_calendar(all_tasks, threshold = 10, start = "today", method = "current")[0]
ctk = list(curr_tasks.keys())
ctv = list(curr_tasks.values())

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Pulltasks Product Demo'),

    html.Div(children='''
        Visualizing the current queue of tasks.
    '''),

    dcc.Graph(
        id='tasks-per-day',
        figure={
            'data': [
                {'x': ctk, 'y': ctv, 'type': 'bar', 'name': 'Tasks'}
            ],
            'layout': {
                'title': 'Tasks by Day'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
