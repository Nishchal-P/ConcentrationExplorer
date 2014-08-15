#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
import DARescueTime_program_keys_SQLite
import DASubjects_SQLite
con = lite.connect('database.db')


def generate_program_keys():
    global daRescuetime_program_key
    daRescuetime_program_key = DARescueTime_program_keys_SQLite.RescueTime_program_key('../')
    daRescuetime_program_key.insert_row_rescuetime_program_key('acrord32', 'Adobe Reader')

def generate_default_subjects():
    dasubjects = DASubjects_SQLite.DASubjects('../')
    dasubjects.insert_subject(['Other'])
    dasubjects.insert_subject(['Thesis'])
    dasubjects.insert_subject(['Computer Vision'])
    dasubjects.insert_subject(['Pattern Recognition'])
    dasubjects.insert_subject(['Network Security'])

with con:
    
    cur = con.cursor()
    try:
        cur.execute("DROP TABLE EyesDetected")
    except:
        print "table 'EyesDetected' doesn't exist"

    try:
        cur.execute("DROP TABLE RescueTime")
    except:
        print "table 'RescueTime' doesn't exist"

    try:
        cur.execute("DROP TABLE RescueTime_program_key")
    except:
        print "table 'RescueTime_program_key' doesn't exist"

    try:
        cur.execute("DROP TABLE Subjects")
    except:
        print "table 'Subjects' doesn't exist"

    try:
        cur.execute("DROP TABLE UserFeedback")
    except:
        print "table 'UserFeedback' doesn't exist"

    try:
        cur.execute("DROP TABLE UserGone")
    except:
        print "table 'UserGone' doesn't exist"

    try:
        cur.execute("DROP TABLE Mindwave")
    except:
        print "table 'Mindwave' doesn't exist"

    try:
        cur.execute("DROP TABLE ErrorReport")
    except:
        print "table 'ErrorReposrt' doesn't exist"
    try:
        cur.execute("DROP TABLE Session")
    except:
        print "table 'Session' doesn't exist"

    try:
        cur.execute("DROP TABLE Reading")
    except:
        print "table 'Reading' doesn't exist"


    #DateTime = UTC, number of seconds since 01-01-1970 00:00:00 UTC
    cur.execute("CREATE TABLE EyesDetected(rowid INTEGER PRIMARY KEY AUTOINCREMENT, DateTime INTEGER, EyesDetected BOOL, Time_seconds INTEGER)")
    print "table EyesDetected created"

    cur.execute("CREATE TABLE RescueTime_program_key(rowid INTEGER PRIMARY KEY AUTOINCREMENT, ProgramKey TEXT, ProgramName TEXT)")
    generate_program_keys()
    print "table RescueTime_program_key created"

    cur.execute("CREATE TABLE Subjects (rowid INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT)")
    #generate_default_subjects()
    print "table Subjects created"

    cur.execute("CREATE TABLE RescueTime(rowid INTEGER PRIMARY KEY AUTOINCREMENT, DateTime INTEGER, Time_spent_seconds INTEGER, ActivityDetail TEXT, Category TEXT, Productivity INTEGER,isImportant BOOL, ActivityGeneral TEXT, Subject_ID INTEGER)")
    print "table RescueTime created"

    cur.execute("CREATE TABLE UserFeedback(rowid INTEGER PRIMARY KEY AUTOINCREMENT, DateTime INTEGER, Attention_level REAL, Meditation_level REAL,Time_seconds INTEGER)")
    print "table UserFeedback created"

    cur.execute("CREATE TABLE UserGone(rowid INTEGER PRIMARY KEY AUTOINCREMENT, Datetime_from INTEGER,Datetime_to INTEGER, Reason TEXT, Description TEXT, isContributing BOOL)")
    print "table UserGone created"

    cur.execute("CREATE TABLE Mindwave (rowid INTEGER PRIMARY KEY AUTOINCREMENT, Datetime_from INTEGER, Datetime_to INTEGER, Attention REAL, Meditation REAL, PoorSignal REAL, BlinkStrength REAL)")
    print "table Mindwave created"

    cur.execute("CREATE TABLE ErrorReport (rowid INTEGER PRIMARY KEY AUTOINCREMENT, Datetime INTEGER, Source TEXT, Description TEXT)")
    print "table Mindwave created"

    cur.execute("CREATE TABLE Session (rowid INTEGER PRIMARY KEY AUTOINCREMENT, Datetime_from INTEGER, Datetime_to INTEGER, Description TEXT)")
    print "table Session created"

    cur.execute("CREATE TABLE Reading (rowid INTEGER PRIMARY KEY AUTOINCREMENT, Datetime_from INTEGER, Datetime_to INTEGER, IsReading BOOL, Description TEXT)")
    print "table Reading created"

