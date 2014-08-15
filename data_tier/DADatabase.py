#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import pytz, datetime

connection = None


def insert_row_action(date_time,eyes_detected):
    local = pytz.timezone ("Europe/Brussels")
    #naive = datetime.datetime.strptime (DateTime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(date_time, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)

    try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	INSERT INTO Actions(DateTime, EyesDetected)	VALUES(?,?)	"""
        cursor.execute(q, (utc_dt, eyes_detected))
        connection.commit()
        print("row added")


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()


def insert_row_rescuetime(date_time,time_spent_seconds, activity, category, productivity,isImportant):
    local = pytz.timezone ("Europe/Brussels")
    #naive = datetime.datetime.strptime (DateTime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(date_time, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)

    try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	INSERT INTO RescueTime(DateTime, Time_spent_seconds, Activity, Category, Productivity,isImportant)	VALUES(?, ?, ?,?,?,?)	"""
        cursor.execute(q, (utc_dt, time_spent_seconds,activity,category,productivity,isImportant))
        connection.commit()
        print("row added to table rescuetime")


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()


def insert_row_userFeedback(DateTime,attention_level, meditation_level):
    local = pytz.timezone ("Europe/Brussels")
    #naive = datetime.datetime.strptime (DateTime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(DateTime, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)

    try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level)	VALUES(?, ?, ?)	"""
        cursor.execute(q, (utc_dt, attention_level, meditation_level))
        connection.commit()
        print("row added to user_feedback")


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def get_last_added_row_RescueTime() :
     try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	select top 1 * from TABLE_NAME  order by ID desc	"""
        connection.commit()
        print("row added to user_feedback")


     except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

     finally:

        if connection:
            connection.close()

