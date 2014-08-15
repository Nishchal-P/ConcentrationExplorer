import sqlite3 as lite
import sys
import pytz, datetime

def create_testdata_Session():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        q1 = """INSERT INTO Session(Datetime_from, Datetime_to,Description) VALUES("2013-12-28 08:00:00","2013-12-28 08:35:00","test_1")"""
        q2 = """INSERT INTO Session(Datetime_from, Datetime_to,Description) VALUES("2013-12-28 10:00:00","2013-12-28 11:15:00","test_2")"""
        q3 = """INSERT INTO Session(Datetime_from, Datetime_to,Description) VALUES("2014-02-13 20:00:00","2014-02-13 20:25:00","test_3")"""
        q4a = """INSERT INTO Session(Datetime_from, Datetime_to,Description) VALUES("2014-02-20 08:00:00","2014-02-20 08:30:00","test_4")"""
        q4b = """INSERT INTO Session(Datetime_from, Datetime_to,Description) VALUES("2014-02-20 09:00:00","2014-02-20 09:25:00","test_4")"""

        queries = [q1,q2,q3,q4a,q4b]

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()


def create_testdata_Actions():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()

        q = """INSERT INTO EyesDetected(DateTime, EyesDetected,Time_seconds)	VALUES("2013-12-28 08:0?:?.432000",1,5)"""
        q1 = 'INSERT INTO EyesDetected(DateTime, EyesDetected,Time_seconds) VALUES("2013-12-28 08:'
        q2 =':'
        q3 = '.432000",'
        q4 = ',5)'

        for minutes in ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","21","22","23","24","25","26","27","28","29","30"]:
            for seconds in ["00","05","10","15","20","25","30","35","40","45","50","55"]:
                #cursor.execute(q,(minutes,seconds))
                #connection.commit()
                result = ""
                if int(seconds) > 40 :
                    result = q1 + str(minutes) + q2 + str(seconds) + q3 + "0" + q4
                else:
                    result = q1 + str(minutes) + q2 + str(seconds) + q3 + "1" + q4
                cursor.execute(result)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()


def create_testdata_Meditation():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()

        q = """INSERT INTO Mindwave(Datetime_from, Datetime_to,Attention,Meditation)	VALUES(2013-12-28 08:00:00,2013-12-28 08:00:05, 0.5, 0.5)"""

        datetimePart = '"2013-12-28 08:'
        q1 = 'INSERT INTO Mindwave(Datetime_from, Datetime_to,Attention,Meditation,PoorSignal,BlinkStrength)	VALUES(' + datetimePart
        q2 =':'
        q3 = '.432000",'
        q4 = ',5)'

        minutesArray = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","21","22","23","24","25","26","27","28","29","30"];
        secondsArray = ["00","05","10","15","20","25","30","35","40","45","50","55"]

        attentionArray = [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1]
        meditationArray = [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1]

        index_attention = 0
        index_meditation = 0

        minute = 0
        second = 0

        while(minute < len(minutesArray)):
            while(second < (len(secondsArray)-1)):
                datetime_to = datetimePart + str(minutesArray[minute]) + q2 + str(secondsArray[second + 1]) + q3

                result = ""
                result += q1
                result += str(minutesArray[minute])
                result += q2
                result += str(secondsArray[second])
                result += q3
                result += datetime_to
                result += str(attentionArray[index_attention])
                result += ","
                result += str(meditationArray[index_meditation])
                result += ",0,0)"

                cursor.execute(result)
                if(index_attention < (len(attentionArray)-1)):
                    index_attention += 1
                    index_meditation +=1
                else:
                    index_attention = 0
                    index_meditation = 0

                second += 1

            minute += 1
            second = 0


        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def create_testdata_RescueTime():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()

        qA1 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:00:00", 200, "A","test","",1,1)	"""
        qC1 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:00:00", 100, "C","test","",1,1)	"""

        qA2 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:05:00", 200, "A","test","",1,1)	"""
        qC2 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:05:00", 100, "C","test","",1,1)	"""

        qA3 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:10:00", 300, "A","test","",1,1)	"""

        qB1 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:15:00", 100, "B","test","",1,1)	"""
        qA4 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:15:00", 200, "A","test","",1,1)	"""

        qB2 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:20:00", 300, "B","test","",1,1)	"""

        qB3 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:25:00", 200, "B","test","",1,1)	"""

        qB4 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 08:30:00", 300, "B","test","",1,1)	"""

        queries = [qA1,qC1,qA2,qC2,qA3,qB1,qA4,qB2,qB3,qB4]

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()


def create_testdata_UserFeedback():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()

        q0 = """INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2013-12-28 08:00:00.502000", 0.8, 0,600)	"""
        q1 = """INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2013-12-28 08:10:00.502000", 0.8, 0,600)	"""
        q2 = """INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2013-12-28 08:20:00.502000", 0.7, 0,600)	"""
        q3 = """INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2013-12-28 08:30:00.502000", 0.8, 0,600)	"""
        q4 = """INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2013-12-28 08:40:00.502000", 0.8, 0,600)	"""
        q5 = """INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2013-12-28 08:50:00.502000", 0.5, 0,600)	"""
        q6 = """INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2013-12-28 09:00:00.502000", 0.2, 0,600)	"""

        queries = [q0,q1,q2,q3,q4,q5,q6]

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def create_testdata_UserGone():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        q1 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 07:20:00.502000", "2013-12-28 07:40:00.502000", "afgeleid","afgeleid",0)	"""
        q2 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 07:58:00.502000", "2013-12-28 08:05:00.502000", "afgeleid","afgeleid",0)	"""
        q3 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 08:07:00.502000", "2013-12-28 08:09:00.502000", "notities","notities",1)	"""
        q4 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 08:12:00.502000", "2013-12-28 08:16:00.502000", "pauze","pauze",0)	"""
        q5 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 08:18:00.502000", "2013-12-28 08:20:00.502000", "notities","nototies",1)	"""
        q6 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 08:21:00.502000", "2013-12-28 08:23:00.502000", "afgeleid","afgeleid",0)	"""
        q7 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 08:25:00.502000", "2013-12-28 08:27:00.502000", "afgeleid","afgeleid",0)	"""
        q8 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 08:28:00.502000", "2013-12-28 08:40:00.502000", "afgeleid","afgeleid",0)	"""
        q9 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 08:28:50.502000", "2013-12-28 09:00:00.502000", "Screen","Screen",1)	"""
        q10 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 09:05:00.502000", "2013-12-28 09:10:00.502000", "Screen","Screen",1)	"""


        queries = [q1,q2,q3,q4,q5,q6,q7,q8]

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

#-------------------------------------------------------------------------------------------------------------------------

def create_testdata_RescueTime_2():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()

        q1a = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:00:00", 200, "A","test","",1,1)	"""
        q1b = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:00:00", 100, "C","test","",1,1)	"""

        q2a = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:05:00", 200, "A","test","",1,1)	"""
        q2b = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:05:00", 100, "B","test","",0,1)	"""

        q3 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:10:00", 180, "A","test","",1,1)	"""

        q4 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:25:00", 180, "A","test","",1,1)	"""

        q5 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:40:00", 120, "A","test","",1,1)	"""

        q6a = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:45:00", 200, "A","test","",1,1)	"""
        q6b = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:45:00", 100, "C","test","",1,1)	"""

        q7a = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:50:00", 200, "B","test","",0,1)	"""
        q7b = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:50:00", 100, "A","test","",1,1)	"""


        q8a = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:55:00", 200, "B","test","",0,1)	"""
        q8b = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 10:55:00", 100, "D","test","",0,1)	"""

        q9 = """INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2013-12-28 11:10:00", 200, "A","test","",1,1)	"""

        queries = [q1a,q1b,q2a,q2b,q3,q4,q5,q6a,q6b,q7a,q7b,q8a,q8b,q9]

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def create_testdata_UserGone_2():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        q1 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 10:13:00.502000", "2013-12-28 10:28:00.502000", "afgeleid","afgeleid",0)	"""
        q2 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 10:28:00.502000", "2013-12-28 10:35:00.502000", "notities","notities",1)	"""
        q3 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 10:35:00.502000", "2013-12-28 10:43:00.502000", "notities","notities",1)	"""
        q4 = """INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2013-12-28 11:00:00.502000", "2013-12-28 11:12:00.502000", "afgeleid","afgeleid",0)	"""


        queries = [q1,q2,q3,q4]

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

#-------------------------------------------------------------------------------------------------------------------------
def create_testdata_RescueTime_3():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        queries = []
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:00:00", 100, "D","test","",0,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:00:00", 100, "A","test","",1,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:00:00", 100, "E","test","",0,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:05:00", 200, "D","test","",0,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:05:00", 100, "E","test","",0,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:10:00", 300, "A","test","",1,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:15:00", 300, "D","test","",0,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:20:00", 200, "D","test","",0,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-13 20:20:00", 100, "A","test","",1,1)	""")

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def create_testdata_Mindwave_3():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        queries = []



        #queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:00:00.102000","2014-02-13 20:05:00.102000",0.80,0.20,0,0)""")
        #queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:05:00.202000","2014-02-13 20:10:00.202000",0.60,0.30,0,0)""")
        #queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:10:00.302000","2014-02-13 20:15:00.302000",0.50,0.50,0,0)""")
        #queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:15:00.402000","2014-02-13 20:20:00.402000",0.20,0.40,0,0)""")
        #queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:20:00.502000","2014-02-13 20:25:00.502000",0.40,0.80,0,0)""")

        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:00:00","2014-02-13 20:05:00",0.80,0.20,0,0)""")
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:05:00","2014-02-13 20:10:00",0.60,0.30,0,0)""")
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:10:00","2014-02-13 20:15:00",0.50,0.50,0,0)""")
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:15:00","2014-02-13 20:20:00",0.20,0.40,0,0)""")
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-13 20:20:00","2014-02-13 20:25:00",0.40,0.80,0,0)""")


        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

#----------------------------------------------------------------------------------------------------------------------
def create_testdata_RescueTime_4():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        queries = []

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 08:00:00", 100, 			"A","test","",	1,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 08:00:00", 200, 			"D","test","",	0,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 08:05:00", 300, 			"B","test","",	1,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:00:00", 300, 			"A","test","",	1,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:05:00", 100, 			"D","test","",	0,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:05:00", 200, 			"E","test","",	0,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:10:00", 300, 			"A","test","",	1,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:15:00", 295, 			"A","test","",	1,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:15:00", 5, 			"D","test","",	0,1)	""")

        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:20:00", 295, 			"A","test","",	1,1)	""")
        queries.append("""INSERT INTO RescueTime(DateTime, Time_spent_seconds, ActivityDetail, Category, Productivity,isImportant,Subject_ID)	VALUES("2014-02-20 09:20:00", 5, 			"B","test","",	1,1)	""")

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()


def create_testdata_Mindwave_4():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        queries = []

        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 08:00:00",		"2014-02-20 08:04:00",		0.80,		0.20,0,0)""")
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 08:04:00",		"2014-02-20 08:08:00",		0.70,		0.30,0,0)        """)
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 08:08:00",		"2014-02-20 08:12:00",		0.50,		0.10,0,0)        """)
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 08:12:00",		"2014-02-20 08:16:00",		0.60,		0.40,0,0)        """)
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 09:02:00",		"2014-02-20 09:06:00",		0.20,		0.80,0,0)        """)
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 09:06:00",		"2014-02-20 09:10:00",		0.30,		0.90,0,0)        """)
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 09:10:00",		"2014-02-20 09:14:00",		0.90,		0.70,0,0)        """)
        queries.append("""INSERT INTO Mindwave(Datetime_from, Datetime_to, Attention, Meditation, PoorSignal,BlinkStrength)	VALUES("2014-02-20 09:14:00",		"2014-02-20 09:16:00",		1.00,		0.50,0,0)        """)


        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def create_testdata_UserGone_4():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()

        queries = []
        queries.append("""INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2014-02-20 08:08:00.502000", 		"2014-02-20 08:30:00.502000", "break",		"break",0)	""")
        queries.append("""INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2014-02-20 09:16:00.502000", 		"2014-02-20 09:18:00.502000", "notes",		"notes",1)	""")
        queries.append("""INSERT INTO UserGone(Datetime_from, Datetime_to, Reason, Description, isContributing) VALUES("2014-02-20 09:20:00.502000", 		"2014-02-20 09:20:10.502000", "screen",		"screen",1)	""")

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def create_testdata_UserFeedback_4():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        queries = []
        queries.append("""INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2014-02-20 08:00:00.502000", 0.8, 			0.2,			720)	""")
        queries.append("""INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2014-02-20 08:12:00.502000", 0.6, 			0.4,			720)	""")
        queries.append("""INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2014-02-20 09:00:00.502000", 0.2, 			0.8,			1200)	""")
        queries.append("""INSERT INTO UserFeedback(DateTime, Attention_level, Meditation_level,Time_seconds)	VALUES("2014-02-20 09:20:00.502000", 0.9, 			0.1,			1200)	""")

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

def create_subjects():
    connection = None
    try:
        connection = lite.connect('database.db')
        cursor = connection.cursor()
        queries = []
        queries.append("""INSERT INTO Subjects(Name)	VALUES("subject_1")	""")

        for query in queries :
            cursor.execute(query)

        connection.commit()


    except lite.Error, e:

        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:

        if connection:
            connection.close()

create_testdata_Meditation()
create_testdata_Actions()
create_testdata_RescueTime()
create_testdata_UserFeedback()
create_testdata_UserGone()

create_testdata_RescueTime_2()
create_testdata_UserGone_2()

create_testdata_RescueTime_3()
create_testdata_Mindwave_3()

create_testdata_RescueTime_4()
create_testdata_Mindwave_4()
create_testdata_UserGone_4()
create_testdata_UserFeedback_4()

create_testdata_Session()
create_subjects()

print 'testgegevens inserted'