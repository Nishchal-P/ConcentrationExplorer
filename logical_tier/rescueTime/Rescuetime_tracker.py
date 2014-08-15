# coding: utf-8
import datetime
import pandas as pd
from rescuetime.api.service import Service
from rescuetime.api.access import AnalyticApiKey
from data_tier import DARescueTime_SQLite
from data_tier import DASubjects_SQLite
from data_tier import DARescueTime_program_keys_SQLite
#from mongodb_dataaccess import DARescueTime_mongodb

from presentation_tier import Form_show_unique_activities


class RescueTimeTracker():


    daRescueTime_program_keys = None
    darescuetime = None
    key_Rescuetime = ''
    link_to_form_main = ''

    def __init__(self,link_to_form_main,key_rescueTime):
        self.daRescueTime_program_keys = DARescueTime_program_keys_SQLite.RescueTime_program_key(link_to_form_main)
        self.darescuetime = DARescueTime_SQLite.RescueTime(link_to_form_main)
        self.key_Rescuetime = key_rescueTime
        self.link_to_form_main = link_to_form_main

    #{'restrict_end': datetime.datetime(2014, 4, 23, 15, 19, 15, 412000), 'via': 'pyrt', 'restrict_begin': datetime.datetime(2014, 4, 23, 14, 43, 32, 509000), 'taxonomy': 'activity', 'format': 'json', 'taxon': u'acrord32', 'rtapi_key': '1234', 'by': 'rank', 'request_ids': 'true'}
    def get_rescuetime_data_proposed_method(self,datetime_from,dstetime_to):
        s = Service.Service()
        p = {}
        k = AnalyticApiKey.AnalyticApiKey(self.key_Rescuetime, s)
        p['restrict_end'] = dstetime_to
        p['via'] = 'pyrt'
        p['restrict_begin'] = datetime_from
        p['taxonomy'] = 'activity'
        p['format'] = 'json'
        p['by'] = 'rank'
        p['request_ids'] = 'true'

        d = s.fetch_data(k,p)

        df = pd.DataFrame(d['rows'], columns=d['row_headers'])
        return df

    #{'restrict_end': datetime.datetime(2014, 4, 23, 15, 19, 15, 412000), 'via': 'pyrt', 'restrict_begin': datetime.datetime(2014, 4, 23, 14, 43, 32, 509000), 'taxonomy': 'activity', 'format': 'json', 'taxon': u'acrord32', 'rtapi_key': '1234', 'by': 'rank', 'request_ids': 'true'}
    def get_rescuetime_data_proposed_method_specific_program(self,datetime_from,dstetime_to,program_id):
        s = Service.Service()
        p = {}
        k = AnalyticApiKey.AnalyticApiKey(self.key_Rescuetime, s)
        p['restrict_end'] = dstetime_to
        p['via'] = 'pyrt'
        p['restrict_begin'] = datetime_from
        p['taxonomy'] = 'activity'
        p['format'] = 'json'
        p['taxon'] = program_id
        p['rs'] = 'minute'
        p['by'] = 'interval'
        p['find_by_id'] = 'true'

        d = s.fetch_data(k,p)

        df = pd.DataFrame(d['rows'], columns=d['row_headers'])
        return df
   # {'restrict_end': datetime.datetime(2014, 4, 23, 15, 19, 15, 412000), 'via': 'pyrt', 'restrict_begin': datetime.datetime(2014, 4, 23, 14, 43, 32, 509000), 'rs': 'minute', 'taxonomy': 'activity', 'format': 'json', 'taxon': '999999', 'rtapi_key': '1234', 'by': 'interval', 'find_by_id':'true'}

    def get_rescuetime_data(self,datetime_from,dstetime_to):
        s = Service.Service()
        p = {}
        k = AnalyticApiKey.AnalyticApiKey(self.key_Rescuetime, s)
        p['restrict_begin'] = datetime_from
        p['restrict_end'] = dstetime_to
        p['taxonomy'] = 'activity'
        p['rs'] = 'minute'
        p['by'] = 'interval'

        d = s.fetch_data(k,p)
        df = pd.DataFrame(d['rows'], columns=d['row_headers'])

        return df

    def get_rescuetime_data_specific_program(self,datetime_from,dstetime_to,program):
        s = Service.Service()
        p = {}
        k = AnalyticApiKey.AnalyticApiKey(self.key_Rescuetime, s)
        p['restrict_begin'] = datetime_from
        p['restrict_end'] = dstetime_to
        p['taxonomy'] = 'activity'
        p['taxon'] = program
        p['rs'] = 'minute'
        p['by'] = 'interval'

        d = s.fetch_data(k,p)
        df = pd.DataFrame(d['rows'], columns=d['row_headers'])

        print d['row_headers']
        for row in d['rows']:
            row_str = ""
            for item in row:
                row_str += str(item) + '\t'
            print row_str
        print d['rows']
        return df
    
    """
    @param activities_list | json with activities from RescueTime, "Activity" is a program or a website. Not a document
    @param unique_activities | list with the activities (unique) used during the specified period
    @param datetime_from
    @param datetime_to

    @return df | "DataFrame", json object where all programs of the activities (listed in table "RescueTime_program_key" are changed by the used documents
    """
    def extend_list_activities_with_file_details(self,activities_list,unique_activities,datetime_from, datetime_to):
        result = []

        list_specific_program = []
        list_activitiesGeneral_activitiesDetail = []
        for item in unique_activities:
            # rescueTime_key_program[key,program]
            rescueTime_key_program = self.daRescueTime_program_keys.get_data_specific_key(item)
            if (len(rescueTime_key_program)!=0):
                #data_specific_program = [Date, Time_Spent_sec, Nb_of_people, Activity, Category, Productivity]
                item_specific_program = self.get_rescuetime_data_specific_program(datetime_from,datetime_to,rescueTime_key_program[0][1])
                list_specific_program.append([item,item_specific_program])
                index = 0
                while index < len(item_specific_program['Activity']):
                    try:
                        list_activitiesGeneral_activitiesDetail.append([rescueTime_key_program[0][2],item_specific_program['Activity'][index]])
                    except:
                        None
                    index += 1

        index_a_l = 0
        list_added_activities = []
        while index_a_l < len(activities_list['Date']):

            start_datetime = activities_list['Date'][index_a_l]
            activity = activities_list['Activity'][index_a_l]

            #teller_test = 0
            for item_specific_program in list_specific_program:
            #    teller_test += 1
            #    print str("tellet_test after for item_specific_program in ... " + str(teller_test))
                index_s_p = 0
                while index_s_p < len(item_specific_program[1]):
                    start_datetime_specific_program = item_specific_program[1]['Date'][index_s_p]
                    generalActivity_specific_program = item_specific_program[0]
                    if start_datetime_specific_program == start_datetime and activity == generalActivity_specific_program:
                        row = {}
                        row['Date'] = item_specific_program[1]['Date'][index_s_p]
                        row['Time Spent (seconds)'] = item_specific_program[1]['Time Spent (seconds)'][index_s_p]
                        row['Activity'] = item_specific_program[1]['Activity'][index_s_p]
                        row['Category'] = item_specific_program[1]['Category'][index_s_p]
                        row['Productivity'] = item_specific_program[1]['Productivity'][index_s_p]

                        hasAdded_ActivityGeneral = False
                        for item in list_activitiesGeneral_activitiesDetail:
                            if item[1] == item_specific_program[1]['Activity'][index_s_p]:
                                row['ActivityGeneral'] = item[0]
                                list_added_activities.append(item[0])
                                hasAdded_ActivityGeneral = True
                                break
                        if hasAdded_ActivityGeneral == False:
                            row['ActivityGeneral'] = 'unknown'
                        result.append(row)
                    index_s_p += 1
            add_row = False
            activity = activities_list['Activity'][index_a_l]
            if (activity in list_added_activities) == False:
                row = {}
                row['Date'] = activities_list['Date'][index_a_l]
                row['Time Spent (seconds)'] = activities_list['Time Spent (seconds)'][index_a_l]
                row['Activity'] = activities_list['Activity'][index_a_l]
                row['Category'] =  activities_list['Category'][index_a_l]
                row['Productivity'] = activities_list['Productivity'][index_a_l]
                row['ActivityGeneral'] = activities_list['Activity'][index_a_l]
                result.append(row)
            index_a_l += 1

        columns = ['Date', 'Time Spent (seconds)', 'Number of People', 'Activity', 'Category', 'Productivity']
        df = pd.DataFrame(result)
        return df


    """
    @param activities_list | json with activities from RescueTime, "Activity" is a program or a website. Not a document
    @param unique_activities | list with the activities (unique) used during the specified period
    @param datetime_from
    @param datetime_to

    @return df | "DataFrame", json object where all programs of the activities (listed in table "RescueTime_program_key" are changed by the used documents
    """
    def extend_list_activities_with_file_details_V2(self,activities_list,unique_activities,datetime_from, datetime_to):
        result = []

        list_specific_program = []
        list_activitiesGeneral_activitiesDetail = []
        program_ranks = self.get_rescuetime_data_proposed_method(datetime_from,datetime_to)
        for i in range(0,len(program_ranks['Lookup ID'])):
            program_id = program_ranks['Lookup ID'][i]
            item_specific_program = self.get_rescuetime_data_proposed_method_specific_program(datetime_from,datetime_to,
                                                                                              program_id)
            list_specific_program.append([program_ranks['Activity'][i],item_specific_program])
            index = 0
            while index < len(item_specific_program['Activity']):
                try:
                    list_activitiesGeneral_activitiesDetail.append([item_specific_program['Activity'][i],item_specific_program['Activity'][index]])
                except:
                    None
                index += 1

        index_a_l = 0
        list_added_activities = []
        while index_a_l < len(activities_list['Date']):

            start_datetime = activities_list['Date'][index_a_l]
            activity = activities_list['Activity'][index_a_l]

            #teller_test = 0
            for item_specific_program in list_specific_program:
            #    teller_test += 1
            #    print str("tellet_test after for item_specific_program in ... " + str(teller_test))
                index_s_p = 0
                while index_s_p < len(item_specific_program[1]):
                    start_datetime_specific_program = item_specific_program[1]['Date'][index_s_p]
                    generalActivity_specific_program = item_specific_program[0]
                    if start_datetime_specific_program == start_datetime and activity == generalActivity_specific_program:
                        row = {}
                        row['Date'] = item_specific_program[1]['Date'][index_s_p]
                        row['Time Spent (seconds)'] = item_specific_program[1]['Time Spent (seconds)'][index_s_p]
                        specific_program = item_specific_program[1]['Activity'][index_s_p]
                        row['Activity'] = specific_program
                        row['Category'] = item_specific_program[1]['Category'][index_s_p]
                        row['Productivity'] = item_specific_program[1]['Productivity'][index_s_p]

                        hasAdded_ActivityGeneral = False
                        for item in list_activitiesGeneral_activitiesDetail:
                            if item[1] == item_specific_program[1]['Activity'][index_s_p]:
                                row['ActivityGeneral'] = item[0]
                                list_added_activities.append(item[0])
                                hasAdded_ActivityGeneral = True
                                break
                        if hasAdded_ActivityGeneral == False:
                            row['ActivityGeneral'] = 'unknown'
                        result.append(row)
                    index_s_p += 1
            add_row = False
            activity = activities_list['Activity'][index_a_l]
            if (activity in list_added_activities) == False:
                row = {}
                row['Date'] = activities_list['Date'][index_a_l]
                row['Time Spent (seconds)'] = activities_list['Time Spent (seconds)'][index_a_l]
                row['Activity'] = activities_list['Activity'][index_a_l]
                row['Category'] =  activities_list['Category'][index_a_l]
                row['Productivity'] = activities_list['Productivity'][index_a_l]
                row['ActivityGeneral'] = activities_list['Activity'][index_a_l]
                result.append(row)
            index_a_l += 1

        columns = ['Date', 'Time Spent (seconds)', 'Number of People', 'Activity', 'Category', 'Productivity']
        df = pd.DataFrame(result)
        return df


     # Hier wordt er geïtereerd over de lijst df, die de records bevat van RescueTime.
     # Er wordt ook bijgehouden welk gebruikt programma/website belangrijk was. Dit wordt ook in de data_tier opgeslagen met een True/False veld
    def add_to_database(self,df,datetime_from,datetime_to):
        #df.to_csv('rt_data_interval_activity_20120901.csv', index=False)

        teller = 0
        list_activities = self.get_unique_list(df,datetime_from,datetime_to)
        list_activities_important = []
        dasubjects = DASubjects_SQLite.DASubjects(self.link_to_form_main)
        subjects = dasubjects.get_subjects()

        Form_show_unique_activities.call_form(list_activities,list_activities_important,subjects,self.link_to_form_main)

        #form_show_unique_activities.call_form(list_activities,list_activities_important)
        while(teller < len(df['Date'])):
            isImportant = False
            subject_id = 1
            for activity_item in list_activities_important:
                if(activity_item[0] == df['Activity'][teller]):
                    isImportant = True
                    subject_id = activity_item[1]
            date_time =  datetime.datetime.strptime(df['Date'][teller],"%Y-%m-%dT%H:%M:%S")
            if datetime_from <= date_time <= datetime_to:
                # SQL Lite
                try:
                    self.darescuetime.insert_row_rescuetime(date_time,int(df['Time Spent (seconds)'][teller]), df['Activity'][teller], df['Category'][teller], int(df['Productivity'][teller]),isImportant,df['ActivityGeneral'][teller],subject_id)
                except Exception, e:
                    self.darescuetime.insert_row_rescuetime(date_time,int(df['Time Spent (seconds)'][teller]), df['Activity'][teller], df['Category'][teller], int(df['Productivity'][teller]),isImportant,df['ActivityGeneral'][teller],subject_id)
                    print str(e)

                # Mongodb
                #DARescueTime_mongodb.insert_row_rescuetime(date_time,int(df['Time Spent (seconds)'][teller]), df['Activity'][teller], df['Category'][teller], int(df['Productivity'][teller]),isImportant)
            teller += 1

    """
    @param df | dataframe containing all the activities retrieved from RescueTime
    @param datetime_from
    @param datetime_to

    @return unique_activity_list | a list with all the (unique) activities in df (field "Activity")
    """
    def get_unique_list(self,df,datetime_from,datetime_to):
        teller = 0
        unique_activity_list = []
        while(teller < len(df['Date'])):
            date_time =  datetime.datetime.strptime(df['Date'][teller],"%Y-%m-%dT%H:%M:%S")
            if datetime_from <= date_time <= datetime_to:
                if (unique_activity_list.__contains__(df['Activity'][teller]) == False):
                    unique_activity_list.append(df['Activity'][teller])
            teller += 1

        return unique_activity_list

    """
    @param datetime_from
    @param datetime_to
    @effect activities will be retrieved from RescueTime and saved to the database. For each program listed in the table "RescueTime_program_key", all the programs in the list will be changed by the used documents.
    """
    def notify_stopping_application(self,datetime_from, datetime_to):
        activities_list = self.get_rescuetime_data(datetime_from,datetime_to)
        unique_activities = self.get_unique_list(activities_list,datetime_from,datetime_to)
        extended_list = self.extend_list_activities_with_file_details(activities_list,unique_activities,datetime_from,datetime_to)
        self.add_to_database(extended_list,datetime_from,datetime_to)




    """
    p['restrict_begin'] = '2013-12-08TI12:00:00'
    p['restrict_end'] = '2013-12-08TI17:00:00'
    p['restrict_kind'] = 'activity'
    p['perspective'] = 'interval'
    d = s.fetch_data(k,p)

    df = pd.DataFrame(d['rows'], columns=d['row_headers'])

    print df
    print df[:10]
    print df['Date'].unique()
    df.to_csv('rt_data_interval_activity_20120901.csv', index=False)
    """