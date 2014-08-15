#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import pytz, datetime
from data_tier import DASubjects_SQLite

connection = None
class RescueTime():

    link = 'data_tier/database.db'
    def __init__(self,path_to_form_main):
        self.link = path_to_form_main + self.link

    def insert_row_rescuetime(self,date_time,time_spent_seconds, activityDetail, category, productivity,isImportant,activityGeneral,subject_ID):
        connection = None
        try:
            connection = lite.connect(self.link)

            cursor = connection.cursor()

            q = """	INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,ActivityGeneral,Subject_ID)	VALUES(?, ?, ?,?,?,?,?,?)	"""
            cursor.execute(q, (date_time, time_spent_seconds,activityDetail,category,productivity,isImportant,activityGeneral,subject_ID))
            connection.commit()
            print("row added to table rescuetime")


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
            all = cursor.execute('SELECT * FROM RescueTime')
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

    def get_data_specific_period(self,datetime_from, datetime_to) :
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
            FROM RescueTime
            WHERE DateTime >= ? AND DateTime < ? ORDER BY Time_spent_seconds"""

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

    def get_data_important_activities_specific_period(self,datetime_from, datetime_to) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime
                    WHERE IsImportant = 1 AND DateTime BETWEEN ? AND ?"""
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

    def get_data_important_activities_specific_period_specific_subject(self,datetime_from, datetime_to,subject_ID) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime
                    WHERE IsImportant = 1 AND DateTime BETWEEN ? AND ? AND RescueTime.Subject_ID = ?"""
            all = cursor.execute(q,(datetime_from,datetime_to,subject_ID))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:
            if connection:
                connection.close()

        return result

    def get_data_important_activities_specific_period_activity(self,datetime_from, datetime_to,activityDetail) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime
                    WHERE IsImportant = 1 AND (DateTime BETWEEN ? AND ?) AND ActivityDetail = ?"""

            all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
            for item in all :
                result.append(item)
        except lite.Error, e:
            try:
                connection = lite.connect(self.link)
                cursor = connection.cursor()
                q = """SELECT *
                        FROM RescueTime
                        WHERE IsImportant = 1 AND (DateTime BETWEEN ? AND ?) AND Activity = ?"""

                all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
                for item in all :
                    result.append(item)
            except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result



    def get_important_activities_specific_period(self,datetime_from, datetime_to) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT ActivityDetail
                    FROM RescueTime
                    WHERE IsImportant = 1 AND DateTime BETWEEN ? AND ?
                    Group By ActivityDetail"""
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

    def get_unique_activities_specific_period(self,datetime_from, datetime_to) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT ActivityDetail
                    FROM RescueTime
                    WHERE DateTime BETWEEN ? AND ?
                    Group By ActivityDetail"""
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

    def get_unique_important_unimportant_activities_specific_period(self,datetime_from, datetime_to,IsImportant) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT ActivityDetail
                    FROM RescueTime
                    WHERE DateTime BETWEEN ? AND ? AND IsImportant = ?
                    Group By ActivityDetail"""
            all = cursor.execute(q,(datetime_from,datetime_to,IsImportant))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result

    def get_all_data_activities_importance_specific_period(self,datetime_from, datetime_to,importance) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime
                    WHERE IsImportant = ? AND DateTime BETWEEN ? AND ?
                    """
            all = cursor.execute(q,(importance,datetime_from,datetime_to))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result

    def get_data_important_activities_specific_period_group_by_activity(self,datetime_from, datetime_to) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT SUM(Time_spent_seconds), ActivityDetail,Subject_ID
                    FROM RescueTime
                    WHERE IsImportant = 1 AND DateTime BETWEEN ? AND ?
                    GROUP BY ActivityDetail"""
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

    def get_data_unimportant_activities_specific_period_group_by_activity(self,datetime_from, datetime_to) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT SUM(Time_spent_seconds), ActivityDetail
                    FROM RescueTime
                    WHERE IsImportant = 0 AND DateTime BETWEEN ? AND ?
                    GROUP BY ActivityDetail"""
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

    def get_data_unimportant_activities_specific_period_activity(self,datetime_from, datetime_to,activityDetail) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime
                    WHERE IsImportant = 0 AND (DateTime BETWEEN ? AND ?) AND ActivityDetail = ?"""

            all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
            for item in all :
                result.append(item)
        except lite.Error, e:
            try:
                connection = lite.connect(self.link)
                cursor = connection.cursor()
                q = """SELECT *
                        FROM RescueTime
                        WHERE IsImportant = 0 AND (DateTime BETWEEN ? AND ?) AND Activity = ?"""

                all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
                for item in all :
                    result.append(item)
            except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)
        finally:

            if connection:
                connection.close()

        return result

    def gat_data_specific_activity_with_treshold(self,datetime_from, datetime_to,activityDetail,treshold_time_sec) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime
                    WHERE (DateTime BETWEEN ? AND ?) AND ActivityDetail = ? AND Time_spent_seconds >= ?"""

            all = cursor.execute(q,(datetime_from,datetime_to,activityDetail,treshold_time_sec))
            for item in all :
                result.append(item)
        except lite.Error, e:
            try:
                connection = lite.connect(self.link)
                cursor = connection.cursor()
                q = """SELECT *
                        FROM RescueTime
                        WHERE (DateTime BETWEEN ? AND ?) AND Activity = ? AND Time_spent_seconds >= ?"""

                all = cursor.execute(q,(datetime_from,datetime_to,activityDetail,treshold_time_sec))
                for item in all :
                    result.append(item)
            except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)
        finally:

            if connection:
                connection.close()

        return result

    def gat_sum_time_secnds_specific_activity_with_treshold(self,datetime_from, datetime_to,activityDetail) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT DateTime, Sum(Time_Spent_seconds)
                    FROM RescueTime
                    WHERE (DateTime BETWEEN ? AND ?) AND ActivityDetail = ?
                    GROUP BY DateTime"""

            all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
            for item in all :
                result.append(item)
        except lite.Error, e:
            try:
                connection = lite.connect(self.link)
                cursor = connection.cursor()
                q = """SELECT DateTime, Sum(Time_Spent_seconds)
                        FROM RescueTime
                        WHERE (DateTime BETWEEN ? AND ?) AND Activity = ?
                        GROUP BY DateTime"""

                all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
                for item in all :
                    result.append(item)
            except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)
        finally:

            if connection:
                connection.close()

        return result

    def gat_data_specific_activity(self,datetime_from, datetime_to,activityDetail) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime
                    WHERE (DateTime BETWEEN ? AND ?) AND ActivityDetail = ?"""

            all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
            for item in all :
                result.append(item)
        except lite.Error, e:
            try:
                connection = lite.connect(self.link)
                cursor = connection.cursor()
                q = """SELECT *
                        FROM RescueTime
                        WHERE (DateTime BETWEEN ? AND ?) AND Activity = ?"""

                all = cursor.execute(q,(datetime_from,datetime_to,activityDetail))
                for item in all :
                    result.append(item)
            except lite.Error, e:
                print "Error %s:" % e.args[0]
                sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result


    def get_dates(self,datetime_from, datetime_to) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT DateTime
                    FROM RescueTime
                    WHERE DateTime BETWEEN ? AND ?
                    GROUP BY DateTime"""
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

    def get_period(self,date_time):
        connection = None
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT *
                    FROM RescueTime"""
            all = cursor.execute(q)
            for item in all :
                datetime_from_rescuetime = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")

                datetime_to_rescuetime =  datetime_from_rescuetime + datetime.timedelta(minutes=5)
                if (datetime_from_rescuetime < date_time) and datetime_to_rescuetime > date_time:
                    return item
            return None
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

    def get_subject_period(self,datetime_from, datetime_to) :
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT RescueTime.Subject_ID, Subjects.Name
            FROM RescueTime LEFT JOIN Subjects ON RescueTime.Subject_ID = Subjects.rowid
            WHERE DateTime >= ? AND DateTime < ?
            GROUP BY Subject_ID"""
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

    def get_subject_period_only_subjectName(self,datetime_from, datetime_to) :
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT Subjects.Name
            FROM RescueTime LEFT JOIN Subjects ON RescueTime.Subject_ID = Subjects.rowid
            WHERE DateTime >= ? AND DateTime < ?
            GROUP BY Subject_ID"""
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

    def get_subjects_period_all_fields(self,datetime_from, datetime_to):
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT R.rowid, DateTime, SUM(Time_spent_seconds), S.Name,COUNT(Category),COUNT(Productivity),MAX(isImportant),S.Name,S.rowid
            FROM RescueTime AS R INNER JOIN Subjects AS S ON Subject_ID == S.rowid
            WHERE DateTime >= ? AND DateTime < ? AND isImportant == 1
            GROUP BY DateTime, Subject_id"""
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

    def get_unique_dates_activities_importance(self,datetime_from, datetime_to,importance) :
        connection = None
        result = []
        try:
            connection = lite.connect(self.link)
            cursor = connection.cursor()
            q = """SELECT DateTime
                    FROM RescueTime
                    WHERE DateTime BETWEEN ? AND ? AND isImportant = ?
                    GROUP BY DateTime"""
            all = cursor.execute(q,(datetime_from,datetime_to,importance))
            for item in all :
                result.append(item)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)

        finally:

            if connection:
                connection.close()

        return result

