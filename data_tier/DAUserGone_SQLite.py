

import sqlite3 as lite
import sys
import pytz, datetime

connection = None

def insert_row_user_gone(datetime_from,datetime_to,reason,description,isContributing):
    try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	INSERT INTO UserGone(Datetime_from, Datetime_to, Reason,Description,isContributing) VALUES(?,?,?,?,?)	"""
        cursor.execute(q, (datetime_from,datetime_to,reason,description,isContributing))
        connection.commit()
        print("row added to UserGone")


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
                FROM UserGone
                WHERE (Datetime_to >= ? AND Datetime_from <= ?) AND Reason != 'Screen'"""

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

def get_data_specific_period_specific_reason(datetime_from, datetime_to,reason) :
    result = []
    try:
        connection = lite.connect('data_tier/database.db')
        cursor = connection.cursor()
        q = """SELECT *
                FROM UserGone
                WHERE (Datetime_to >= ? AND Datetime_from <= ?) AND Reason = ?"""

        all = cursor.execute(q,(datetime_from,datetime_to,reason))
        for item in all :
            result.append(item)
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

    return result

def get_unique_reasons(datetime_from, datetime_to) :
    result = []
    try:
        connection = lite.connect('data_tier/database.db')
        cursor = connection.cursor()
        q = """SELECT Reason FROM UserGone WHERE (Datetime_to >= ? AND Datetime_from <= ?) GROUP BY Reason"""

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
