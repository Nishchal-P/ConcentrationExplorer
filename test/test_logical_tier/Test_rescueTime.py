import datetime

from logical_tier.rescueTime import Rescuetime_tracker




import unittest
from data_tier import DARescueTime_program_keys_SQLite

class TestSequenceFunctions(unittest.TestCase):
    key_RescueTime = 'B635gKkc4CrwWu5GgJfAOeUTBDoL2AxkD44nt6au'
    """
    def test_get_data(self):
        s = Service.Service()
        p = {}
        datetime_from = datetime.datetime.strptime("2014-03-13 12:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-03-13 16:00:00","%Y-%m-%d %H:%M:%S")
        k = AnalyticApiKey.AnalyticApiKey(self.key_RescueTime, s)
        p['restrict_begin'] = datetime_from
        p['restrict_end'] = datetime_to
        p['taxonomy'] = 'activity'
        #p['rt'] = 'activity'
        #p['tx'] = 'activity'
        p['taxon'] = 'acrord32'
        #p['tn'] = 'Adobe Reader'
        #p['rs'] = 'minute'
        p['by'] = 'interval'
        d = s.fetch_data(k,p)

        df = pd.DataFrame(d['rows'], columns=d['row_headers'])
        #print df[:100]

    def test_get_data_specific_program(self):
        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('../',self.key_RescueTime)
        datetime_from = datetime.datetime.strptime("2014-03-13 12:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-03-13 16:00:00","%Y-%m-%d %H:%M:%S")
        df = rescuetime_tracker_object.get_rescuetime_data_specific_program(datetime_from,datetime_to,'acrord32')
        self.assertTrue(len(df['Date'])> 0)
        print df[:10]

    def test_get_key_specific_program(self):
        program_key = 'Adobe Reader'
        daRescueTime_program_keys = DARescueTime_program_keys_SQLite.RescueTime_program_key('../')
        result = daRescueTime_program_keys.get_data_specific_key(program_key)
        print '---------------------'
        print result
        print '---------------------'

    def test_form_show_unique_activities(self):
        list_activities_important = []
        list_activities = []
        list_activities.append('A')
        list_activities.append('B')
        list_activities.append('C')
        list_activities.append('D')
        list_activities.append('E')

        dasubjects = DASubjects_SQLite.DASubjects('../')
        subjects = dasubjects.get_subjects()

        form_show_unique_activities.call_form(list_activities,list_activities_important,subjects)
    """
    """
    def test_extend_activity_list(self):
        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('../',self.key_RescueTime)
        datetime_from = datetime.datetime.strptime("2014-03-13 23:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-03-14 00:00:00","%Y-%m-%d %H:%M:%S")
        activities_list = rescuetime_tracker_object.get_rescuetime_data(datetime_from,datetime_to)
        unique_activities = rescuetime_tracker_object.get_unique_list(activities_list,datetime_from,datetime_to)
        extended_list = rescuetime_tracker_object.extend_list_activities_with_file_details(activities_list,unique_activities,datetime_from,datetime_to)
        print extended_list[:100]['Activity']
        rescuetime_tracker_object.add_to_database(extended_list,datetime_from,datetime_to)
       # rescuetime_tracker_object.add_to_database(activities_list,datetime_from,datetime_to)
    """
    """
    def test_extend_activity_list_2(self):
        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('../',self.key_RescueTime)
        datetime_from = datetime.datetime.strptime("2014-03-17 18:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-03-17 18:40:00","%Y-%m-%d %H:%M:%S")
        activities_list = rescuetime_tracker_object.get_rescuetime_data(datetime_from,datetime_to)
        unique_activities = rescuetime_tracker_object.get_unique_list(activities_list,datetime_from,datetime_to)
        extended_list = rescuetime_tracker_object.extend_list_activities_with_file_details(activities_list,unique_activities,datetime_from,datetime_to)
        print extended_list[:100]['Activity']
        rescuetime_tracker_object.add_to_database(extended_list,datetime_from,datetime_to)
        options_reason = [['Notes','I was taking notes',1], ['Document','I was searching/reading a document',1], ['Break','I took a break',0], ['Distracted','I was distracted',0], ['Screen','I was looking to the screen',1],['Other','Other',0]]
        treshold_important_unimportant = 30

        presentation_tier.show_results(datetime_from,datetime_to,options_reason,treshold_important_unimportant)
       # rescuetime_tracker_object.add_to_database(activities_list,datetime_from,datetime_to)
    """
    """
    def test_extend_activity_list_3(self):
        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('../',self.key_RescueTime)
        datetime_from = datetime.datetime.strptime("2014-03-26 10:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-03-26 12:00:00","%Y-%m-%d %H:%M:%S")
        activities_list = rescuetime_tracker_object.get_rescuetime_data(datetime_from,datetime_to)
        unique_activities = rescuetime_tracker_object.get_unique_list(activities_list,datetime_from,datetime_to)
        extended_list = rescuetime_tracker_object.extend_list_activities_with_file_details(activities_list,unique_activities,datetime_from,datetime_to)
        print extended_list[:100]['Activity']
        rescuetime_tracker_object.add_to_database(extended_list,datetime_from,datetime_to)
        options_reason = [['Notes','I was taking notes',1], ['Document','I was searching/reading a document',1], ['Break','I took a break',0], ['Distracted','I was distracted',0], ['Screen','I was looking to the screen',1],['Other','Other',0]]
        treshold_important_unimportant = 30

        presentation_tier.show_results(datetime_from,datetime_to,options_reason,treshold_important_unimportant)
       # rescuetime_tracker_object.add_to_database(activities_list,datetime_from,datetime_to)
    """
    """
    def test_load_data_rescueTime(self):
        key_RescueTime = 'B631JkKmVbnC5SsKSRhmuJnUmyTvQ4Gc_I2fpF6I'
        start_date_time = datetime.datetime.strptime("2014-04-16 20:39:58","%Y-%m-%d %H:%M:%S")
        end_date_time = datetime.datetime.strptime("2014-04-16 21:20:00","%Y-%m-%d %H:%M:%S")

        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('',key_RescueTime)
        rescuetime_tracker_object.notify_stopping_application(start_date_time, end_date_time)
        #df.to_csv('rt_data_interval_activity_20120901.csv', index=False)

        DASession_SQLite.insert_row_session(start_date_time,end_date_time,"prototype testing")
    """
    """
    def test_load_data_rescueTime_2(self):
        key_RescueTime = 'B631JkKmVbnC5SsKSRhmuJnUmyTvQ4Gc_I2fpF6I'
        start_date_time = datetime.datetime.strptime("2014-04-26 20:55:00","%Y-%m-%d %H:%M:%S")
        end_date_time = datetime.datetime.strptime("2014-04-26 22:20:00","%Y-%m-%d %H:%M:%S")
        program = 'acrord32'
        key = 'B631JkKmVbnC5SsKSRhmuJnUmyTvQ4Gc_I2fpF6I'

        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('',key)

        df = rescuetime_tracker_object.get_rescuetime_data_specific_program(start_date_time,end_date_time,program)
        print '*-*-*-*-*-*-*-*-*-*-*-*-'
        print df
        print '*-*-*-*-*-*-*-*-*-*-*-*-'
    """

    def test_load_data_rescueTime_4(self):
        key_RescueTime = 'B63fu4jC7_pq_Uv5AMcXwzmvtjKuLs6sbdIDgdEV'
        start_date_time = datetime.datetime.strptime("2014-05-08 11:09:30.509000", "%Y-%m-%d %H:%M:%S.%f")
        end_date_time = datetime.datetime.strptime("2014-05-08 11:37:00.412000", "%Y-%m-%d %H:%M:%S.%f")

        rescuetime_tracker_object = Rescuetime_tracker.RescueTimeTracker('',key_RescueTime)
        rescuetime_tracker_object.notify_stopping_application(start_date_time, end_date_time)

    """
    def test_load_data_rescueTime_3(self):
        daRescueTimeProgramKey = DARescueTime_program_keys_SQLite.RescueTime_program_key('../../')

        start_date_time = datetime.datetime.strptime("2014-04-23 14:43:32.509000", "%Y-%m-%d %H:%M:%S.%f")
        end_date_time = datetime.datetime.strptime("2014-04-23 15:19:15.412000", "%Y-%m-%d %H:%M:%S.%f")
        program = 'acrord32'
        key = 'B631JkKmVbnC5SsKSRhmuJnUmyTvQ4Gc_I2fpF6I'
        programs_list = daRescueTimeProgramKey.get_all()
        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('../../',key)


        df_normal = rescuetime_tracker_object.get_rescuetime_data(start_date_time,end_date_time)
        df_acrord = []
        for item in programs_list:
            df_acrord.append(rescuetime_tracker_object.get_rescuetime_data_specific_program(start_date_time,end_date_time,item[1]))

        unique_activities = rescuetime_tracker_object.get_unique_list(df_normal,start_date_time,end_date_time)
        df_extended_list = rescuetime_tracker_object.extend_list_activities_with_file_details_V2(df_normal,unique_activities,start_date_time,end_date_time)

        index_n = 0
        index_e = 0

        while index_e < len(df_extended_list) and index_n < len(df_normal):
            checked = False
            for index_pl in range(0,len(programs_list)):
                if df_extended_list['ActivityGeneral'][index_e] == programs_list[index_pl][2]:
                    sum_time_spent = 0
                    total = 0
                    for index_a in range(0,len(df_acrord[index_pl])):
                        if df_acrord[index_pl]['Date'][index_a] == df_normal['Date'][index_n]:
                            sum_time_spent += df_acrord[index_pl]['Time Spent (seconds)'][index_a]
                            total += 1
                    self.assertEqual(sum_time_spent, df_normal['Time Spent (seconds)'][index_n])
                    self.assertEqual(df_normal['Activity'][index_n], df_extended_list['ActivityGeneral'][index_e] )
                    if total > 0:
                        # total - 1 omdat, als total 1 is, mag die niet verhoogd worden. Dan is "Activity" van df_normal gewoon vergangen door 1 "Activity" van df_acrord
                        index_e += (total - 1)
                    checked = True
            if checked == False:
                self.assertEqual(df_normal['Date'][index_n],df_extended_list['Date'][index_e])
                self.assertEqual(df_normal['Time Spent (seconds)'][index_n],df_extended_list['Time Spent (seconds)'][index_e])
                #self.assertEqual(df_normal['Activity'][index_n],df_extended_list['Activity'][index_e])
                self.assertEqual(df_normal['Activity'][index_n],df_extended_list['ActivityGeneral'][index_e])
            index_n += 1
            index_e += 1
            print "--------------------"
            print df_extended_list
            print "--------------------"

    def test_testing_proposed_method_RescueTime(self):
        key_RescueTime = 'B63fu4jC7_pq_Uv5AMcXwzmvtjKuLs6sbdIDgdEV'
        start_date_time = datetime.datetime.strptime("2014-04-23 14:43:32.509000", "%Y-%m-%d %H:%M:%S.%f")
        end_date_time = datetime.datetime.strptime("2014-04-23 15:19:15.412000", "%Y-%m-%d %H:%M:%S.%f")
        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('../../',key_RescueTime)

        df_normal = rescuetime_tracker_object.get_rescuetime_data_proposed_method(start_date_time,end_date_time)
        #unique_activities = rescuetime_tracker_object.get_unique_list(df_normal,start_date_time,end_date_time)
        #df_extended_list = rescuetime_tracker_object.extend_list_activities_with_file_details(df_normal,unique_activities,start_date_time,end_date_time)
       # print df_normal

        program_id = df_normal['Lookup ID'][0]
        df_specific = rescuetime_tracker_object.get_rescuetime_data_proposed_method_specific_program(start_date_time,end_date_time,program_id)

        rescuetime_tracker_object = rescuetime_tracker.RescueTime_tracker('../../',key_RescueTime)
        #print df_specific



    """
    """
    def test_get_data_saving_database(self):
        s = Service.Service()
        p = {}
        datetime_from = datetime.datetime.strptime("2014-03-14 23:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-03-14 23:59:00","%Y-%m-%d %H:%M:%S")
        k = AnalyticApiKey.AnalyticApiKey(self.key_RescueTime, s)
        p['restrict_begin'] = datetime_from
        p['restrict_end'] = datetime_to
        p['taxonomy'] = 'activity'
        #p['rt'] = 'activity'
        #p['rt'] = 'Adobe Reader'
        #p['tn'] = 'Adobe Reader'
        p['rs'] = 'minute'
        p['by'] = 'interval'
        d = s.fetch_data(k,p)

        df = pd.DataFrame(d['rows'], columns=d['row_headers'])

        rescuetime_tracker.add_to_database(df, datetime_from, datetime_to,'../')

        print df[:100]
    """
if __name__ == '__main__':
    unittest.main()