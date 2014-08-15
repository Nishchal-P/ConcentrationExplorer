
import sqlite3 as lite
import sys
import pytz, datetime

connection = None
class DASession:
    link = 'data_tier/database.db'
    def __init__(self,path_to_form_main):
        self.link = path_to_form_main + self.link

    def insert_row_session(self,datetime_from,datetime_to,description):
        try:
            connection = lite.connect(self.link)

            cursor = connection.cursor()

            q = """	INSERT INTO Session(Datetime_from, Datetime_to,Description) VALUES(?,?,?)	"""
            cursor.execute(q, (datetime_from,datetime_to,description))
            connection.commit()
            print("row added to Session")


        except lite.Error, e:

            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()


    def get_data_specific_period(self,datetime_from, datetime_to) :
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM Session
                    WHERE (Datetime_to >= ? AND Datetime_from <= ?)'"""

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

    def get_period_specific_date(self,date_time):
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM Session
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

    def get_session(self,session_id):
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM Session
                    WHERE rowid = ?"""

            all = cursor.execute(q,([str(session_id)]))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result

    def get_dates_session(self, session_id):
        session = self.get_session(session_id)

        try:
            datetime_from = datetime.datetime.strptime(session[0][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from = datetime.datetime.strptime(session[0][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to = datetime.datetime.strptime(session[0][2], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_to = datetime.datetime.strptime(session[0][2], "%Y-%m-%d %H:%M:%S")
        return datetime_from, datetime_to