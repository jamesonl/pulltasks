# Executing the Pipeline

In order to reorganize tasks, I have arranged the project into a format that will help to simplify the orchestration of two kinds of jobs:
 - Manual / Ad Hoc rescheduling
 - Automated rescheduling

Since automated rescheduling is covered through the use of a heroku application, the majority of this documentation will focus on describing how users can configure ad hoc runs.

## How to kick off a manual reload of tasks

  1. Load the `.venv` virtual environment.
  2. Within the terminal, write: `python main.py`.
  3. Based upon the number of tasks, the script will automatically reallocate tasks based on the predefined scheduling parameters that were set.
