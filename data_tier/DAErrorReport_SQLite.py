#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import pytz, datetime

connection = None


def insert_row_action(date_time,source,description):
    try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	INSERT INTO ErrorReport(Datetime, Source, Description)	VALUES(?,?,?)	"""
        cursor.execute(q, (date_time, source,description))
        connection.commit()
        print("row added to ErrorReport")


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
                FROM ErrorReport
                WHERE DateTime BETWEEN ? AND ?"""

        all = cursor.execute(q,(datetime_from,datetime_to))
        for item in all :
            result.append(item)
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

    return result