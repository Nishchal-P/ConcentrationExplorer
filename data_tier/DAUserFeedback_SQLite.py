#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import pytz, datetime

connection = None

def insert_row_userFeedback(date_time,attention_level, meditation_level,time_seconds):
    """local = pytz.timezone ("Europe/Brussels")
    #naive = datetime.datetime.strptime (DateTime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(DateTime, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)"""

    try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES(?, ?, ?,?)	"""
        cursor.execute(q, (date_time, attention_level, meditation_level,time_seconds))
        connection.commit()
        print("row added to user_feedback")


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def get_data_specific_period(datetime_from, datetime_to) :
    result = []
    try:
        connection = lite.connect('data_tier/database.db')
        cursor = connection.cursor()
        q = """SELECT *
                FROM UserFeedback"""

        all = cursor.execute(q)
        for item in all :
            try:
                datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
            datetime_to_userfeedback =  datetime_from_userfeedback + datetime.timedelta(seconds=item[4])
            if (datetime_to_userfeedback >= datetime_from) and (datetime_from_userfeedback <= datetime_to):
                result.append(item)
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

    return result