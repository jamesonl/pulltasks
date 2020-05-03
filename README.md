# Todidnt

## Prerequisites
You'll need to save a secret key as .secret. This will change in the future as I make the service more generalized for users other than myself.

## Introduction
Sorting algorithms were one of the first things that I learned about when studying computer science. This interaction with algorithms was one of the first reasons I fell in love with programming - they demonstrated how thought could be turned into reality, and how different conceptions of thought could constrain or free you.

Scheduling algorithms followed a little later, and were a point of interest that had far reaching implications / consequences for everything from organizing my day to designing industrial level applications.

Since then, life happened... and along the way, I figured out that my methods of getting things done wasn't as effective as I had once thought.

After introducing Todoist into my life, I finally had a single place to log everything I needed to... well... get done! But while I now had a place to put all my things, the next (even greater) complexity was figuring out: 1) when I would do them, and 2) how long they would take.

## What is this repository for?
Todidnt is a series of scheduling models meant to experiment with different workflows for organizing, redistributing, and enriching tasks that I need to execute.

## Scheduling Implementations
Threshold Scheduler | February 15, 2020
Grabbing all tasks, this scheduler distributes work items across days (at random) while ensuring that only a certain number of tasks are allocated to each day.

## Providing Feedback
(Please note that I develop this application independently and in my free time.)

Though this tool is primarily built for myself, I want to collect use cases from people who live by their todo lists. Should you want to add a use case, open up an issue and clearly state: what you want to accomplish, how you are doing it today (or not able to), and what this change would enable you to do!


# Notes about Usage

## Todoist Limitations

Citing their page regarding [utilization](https://developer.todoist.com/rest/v1/#limits):

>### **Requests per Minute**
>You can make a total of 50 requests per minute per user when using the REST API.

Given an example:
 - **200 tasks** will take **4 minutes** to complete

As a matter of best practice:
 - My goal should be to reduce the number of times that tasks must be rescheduled
 - My total collection of tasks should never exceed a certain number
    - This means the balance between ingesting new tasks and completing existing tasks

# Lessons Learned

## Things to consider for future worker functions

 -
