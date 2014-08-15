#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import pytz, datetime
connection = None
class RescueTime_program_key():

    link = 'data_tier/database.db'
    def __init__(self,path_to_form_main):
        self.link = path_to_form_main + self.link

    def insert_row_rescuetime_program_key(self,program_key, program_name):
        connection = None
        try:
            connection = lite.connect(self.link)

            cursor = connection.cursor()

            q = """	INSERT INTO RescueTime_program_key(ProgramKey, ProgramName)	VALUES(?, ?)	"""
            cursor.execute(q, (program_key, program_name))
            connection.commit()
            print("row added to table RescueTime_program_key")


        except lite.Error, e:

            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()


    def get_all(self) :
        connection = None
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            all = cursor.execute('SELECT * FROM RescueTime_program_key')
            result = []
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result

    def get_data_specific_key(self,program_name) :
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT * FROM RescueTime_program_key where ProgramName = ?"""
            all = cursor.execute(q,([program_name]))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result