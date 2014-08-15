
import sqlite3 as lite
import sys
import pytz, datetime

connection = None
class DAReading():
    link_voorvoegsel = ''
    def __init__(self,link_voorvoegsel):
        self.link_voorvoegsel = link_voorvoegsel

    def insert_row_reading(self,datetime_from,datetime_to,isReading,description):
        try:
            connection = lite.connect(self.link_voorvoegsel + 'data_tier/database.db')

            cursor = connection.cursor()

            q = """	INSERT INTO Reading(Datetime_from, Datetime_to,IsReading,Description) VALUES(?,?,?,?)	"""
            cursor.execute(q, (datetime_from,datetime_to,isReading,description))
            connection.commit()
            print("row added to Reading")


        except lite.Error, e:

            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()


    def get_data_specific_period(self,datetime_from, datetime_to) :
        result = []
        try:
            connection = lite.connect('data_tier/database.db')
            cursor = connection.cursor()
            q = """SELECT *
                    FROM Reading"""

            all = cursor.execute(q)
            for item in all :
                # datetime_from_userfeedback
                try:
                    try:
                        datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")

                    # datetime_to_userfeedback
                    try:
                        datetime_to_userfeedback = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        datetime_to_userfeedback = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S")
                    if (datetime_to_userfeedback >= datetime_from) and (datetime_from_userfeedback <= datetime_to):
                        result.append(item)
                except:
                    # als datums niet voldoen aan formaat, dan worden ze genegeerd
                    pass
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result

    def get_period_specific_date(self,date_time):
        result = []
        try:
            connection = lite.connect('data_tier/database.db')
            cursor = connection.cursor()
            q = """SELECT *
                    FROM Reading
                    WHERE (Datetime_from <= ? AND Datetime_to >= ?)"""

            all = cursor.execute(q,(date_time,date_time))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result