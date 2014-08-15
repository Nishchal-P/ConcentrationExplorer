
import sqlite3 as lite
import sys
import pytz, datetime

connection = None
class DASubjects():
    link = 'data_tier/database.db'
    def __init__(self,link_voorvoegsel):
        self.link = link_voorvoegsel + self.link

    def insert_subject(self,name):
        try:
            connection = lite.connect(self.link)

            cursor = connection.cursor()

            q = """	INSERT INTO Subjects(Name) VALUES(?)	"""
            cursor.execute(q, (name))
            connection.commit()
            print("row added to Subjects")


        except lite.Error, e:

            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

    def get_subjects(self) :
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM Subjects"""

            all = cursor.execute(q)
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()
        return result

    def get_subject_ID(self,name) :
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM Subjects
                    WHERE Name = ?"""


            all = cursor.execute(q,(name))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()
        return result[0]
