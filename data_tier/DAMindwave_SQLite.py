#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import pytz, datetime

connection = None


def insert_row_mindwave(date_time_from,date_time_to, attention, meditation,poorSignal, blinkStrength):
    try:
        connection = lite.connect('data_tier/database.db')

        cursor = connection.cursor()

        q = """	INSERT INTO Mindwave(Datetime_from, Datetime_to,Attention,Meditation,PoorSignal, BlinkStrength)	VALUES(?,?,?,?,?,?)	"""
        cursor.execute(q, (date_time_from, date_time_to,attention,meditation,poorSignal,blinkStrength))
        connection.commit()
        print("row added to Mindwave table")


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()


# Warning, als de opgegeven periode overlapt met een periode in de database, wordt die ook terug gegeven.
# Bv: datetime_from = "2014-02-15 12:00:00", datetime_to = "2014-02-15 12:00:05
# row fount in database: datetime_from = "2014-02-15 12:00:02", datetime_to = "2014-02-15 12:07:00"
# row fount in database: datetime_from = "2014-02-15 11:55:00", datetime_to = "2014-02-15 12:02:00"
# row fount in database: datetime_from = "2014-02-15 11:55:00", datetime_to = "2014-02-15 12:07:00"
# Deze 3 rijen worden teruggegeven, omdat er overlap is.

# Het is geen bug dat datetime_from en datetime_to in de functie zijn omgedraaid. Hierdoor worden overlapte periodes ook teruggegeven
def get_data_specific_period(datetime_from, datetime_to) :
    result = []
    try:
        connection = lite.connect('data_tier/database.db')
        cursor = connection.cursor()
        q = """SELECT *
                FROM Mindwave
                WHERE Datetime_to >= ? AND Datetime_from <= ?
                ORDER BY Datetime_from"""

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