from logical_tier import Data_processing

import datetime
import unittest

# For this class the python file 'Testdata_database should be executed first
class TestSequenceFunctions(unittest.TestCase):
    link_to_main = ''

    def test_getListImportantActivities(self):
        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]
        result = Data_processing.getListImportantActivities(datetime_from,datetime_to,options_reason,self.link_to_main)
        """
        string_result = ""
        for line in result:
            for item in line:
                string_result += str(item) + "\t"
            string_result += "\n"
        print string_result
        """
        # afgeleid attribute
        self.assertEqual(result[0][4][0][1],0.25)
        self.assertEqual(result[1][4][0][1],0.55)
        self.assertEqual(result[2][4][0][1],0.50)

        # notities attribute, A
        self.assertEqual(result[0][4][1][1],0.20)

        # notities attribute, B
        self.assertEqual(result[1][4][1][1],0.10)

        # Mindwave
        # A
        self.assertEqual(round(result[0][5],2),0.55)

    def test_get_average_reason(self):
        datetime_from = datetime.datetime.strptime("2013-12-28 08:25:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]

       # print data_processing.get_average_reason(datetime_from,datetime_to,options_reason[0][0])

    def test_show_results(self):
        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]
        #presentation_tier.show_results(datetime_from,datetime_to,options_reason,15)
        #presentation_tier.showgraph(datetime_from,datetime_to,options_reason)

        result_list_work_sessions = Data_processing.get_list_work_sessions(datetime_from,datetime_to,options_reason,50,self.link_to_main)

    def test_list_work_session(self):
        datetime_from = datetime.datetime.strptime("2013-12-28 10:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 11:15:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]
        result_list = Data_processing.get_list_work_sessions(datetime_from,datetime_to,options_reason,50,self.link_to_main)

        #presentation_tier.show_results(datetime_from,datetime_to,options_reason)
        print '*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-'
        print result_list
        print '*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-'

        # rij 0
        self.assertEqual(result_list[0][0],datetime.datetime(2013, 12, 28, 10, 0))
        self.assertEqual(result_list[0][1],datetime.datetime(2013, 12, 28, 10, 05))
        self.assertEqual(result_list[0][3],True)

        # rij 1
        self.assertEqual(result_list[1][0],datetime.datetime(2013, 12, 28, 10, 05))
        self.assertEqual(result_list[1][1],datetime.datetime(2013, 12, 28, 10, 10))
        self.assertEqual(result_list[1][3],False)

        # rij 2
        self.assertEqual(result_list[2][0],datetime.datetime(2013, 12, 28, 10, 10))
        self.assertEqual(result_list[2][1],datetime.datetime(2013, 12, 28, 10, 13,0,502000))
        self.assertEqual(result_list[2][3],True)

        # rij 3
        self.assertEqual(result_list[3][0],datetime.datetime(2013, 12, 28, 10, 13,0,502000))
        self.assertEqual(result_list[3][1],datetime.datetime(2013, 12, 28, 10, 28,0,502000))
        self.assertEqual(result_list[3][3],False)

        # rij 4
        self.assertEqual(result_list[4][0],datetime.datetime(2013, 12, 28, 10, 28,0,502000))
        self.assertEqual(result_list[4][1],datetime.datetime(2013, 12, 28, 10, 35,0,502000))
        self.assertEqual(result_list[4][3],True)

        # rij 5
        self.assertEqual(result_list[5][0],datetime.datetime(2013, 12, 28, 10, 35,0,502000))
        self.assertEqual(result_list[5][1],datetime.datetime(2013, 12, 28, 10, 43,0,502000))
        self.assertEqual(result_list[5][3],True)

        # rij 6
        self.assertEqual(result_list[6][0],datetime.datetime(2013, 12, 28, 10, 43,0,502000))
        self.assertEqual(result_list[6][1],datetime.datetime(2013, 12, 28, 10, 50))
        self.assertEqual(result_list[6][3],True)

        # rij 7
        self.assertEqual(result_list[7][0],datetime.datetime(2013, 12, 28, 10, 50))
        self.assertEqual(result_list[7][1],datetime.datetime(2013, 12, 28, 11, 00,0,502000))
        self.assertEqual(result_list[7][3],False)

        # rij 8
        self.assertEqual(result_list[8][0],datetime.datetime(2013, 12, 28, 11, 00,0,502000))
        self.assertEqual(result_list[8][1],datetime.datetime(2013, 12, 28, 11, 12,0,502000))
        self.assertEqual(result_list[8][3],False)

        # rij 9
        self.assertEqual(result_list[9][0],datetime.datetime(2013, 12, 28, 11, 12,0,502000))
        self.assertEqual(result_list[9][1],datetime.datetime(2013, 12, 28, 11, 15))
        self.assertEqual(result_list[9][3],True)


    def test_get_list_workSession_amount_details(self):
        datetime_from = datetime.datetime.strptime("2013-12-28 10:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 11:15:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]
        result_list_work_sessions = Data_processing.get_list_work_sessions(datetime_from,datetime_to,options_reason,50,self.link_to_main)

        result_list = Data_processing.get_list_workSession_amount_details(result_list_work_sessions,options_reason)

        #print result_list
        # total
        self.assertEqual(result_list[0][2],1978)
        self.assertEqual(result_list[1][2],900)
        self.assertEqual(result_list[2][2],1620)

        # amount
        self.assertEqual(result_list[0][3],4)
        self.assertEqual(result_list[1][3],2)
        self.assertEqual(result_list[2][3],2)

        # average
        self.assertEqual(result_list[0][4],494)
        self.assertEqual(result_list[1][4],450)
        self.assertEqual(result_list[2][4],810)

        # min
        self.assertEqual(result_list[0][5],179)
        self.assertEqual(result_list[1][5],300)
        self.assertEqual(result_list[2][5],720)

        # max
        self.assertEqual(result_list[0][6],1319)
        self.assertEqual(result_list[1][6],600)
        self.assertEqual(result_list[2][6],900)


    """
    def test_linegraph(self):
        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")
        presentation_tier.show_graph_attention_data_mindwave(datetime_from,datetime_to)
        presentation_tier.show_barchart_attention_data_mindwave(datetime_from,datetime_to)
    """
    def test_getListUnimportantActivities(self):
        datetime_from = datetime.datetime.strptime("2014-02-13 20:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-02-13 20:30:00","%Y-%m-%d %H:%M:%S")
        result = Data_processing.getListUnimportantActivities(datetime_from,datetime_to,self.link_to_main)
        """
        print '---------------------'
        print result
        print '---------------------'
        """
        # D
        self.assertEqual(result[0][0],'D')
        self.assertEqual(result[0][1],800)
        self.assertEqual(round(result[0][2],2),0.50)
        self.assertEqual(round(result[0][3],3),0.425)

        # E
        self.assertEqual(result[1][0],'E')
        self.assertEqual(result[1][1],200)
        self.assertEqual(round(result[1][2],2),0.70)
        self.assertEqual(round(result[1][3],2),0.25)

    def test_calculate_average_mindwave(self):
        list_mindwave_data = []
        list_mindwave_data.append([0,"2014-02-13 08:00:00","2014-02-13 08:02:00",0.2,0.8])
        list_mindwave_data.append([0,"2014-02-13 08:02:00","2014-02-13 08:04:00",0.4,0.6])
        list_mindwave_data.append([0,"2014-02-13 08:04:00","2014-02-13 08:06:00",0.6,0.4])

        start_datetime_activitydetail = datetime.datetime.strptime("2014-02-13 08:00:00","%Y-%m-%d %H:%M:%S")
        end_datetime_activitydetail = datetime.datetime.strptime("2014-02-13 08:05:00","%Y-%m-%d %H:%M:%S")

        attention_avg, meditation_avg = Data_processing.calculate_average_mindwave(start_datetime_activitydetail,end_datetime_activitydetail,list_mindwave_data)

        self.assertEqual(round(attention_avg,2),0.36)
        self.assertEqual(round(meditation_avg,2),0.64)

    def test_calculate_average_mindwave_2(self):
        list_mindwave_data = []
        list_mindwave_data.append([0,"2014-02-13 07:55:00","2014-02-13 08:10:00",0.2,0.8])
        list_mindwave_data.append([0,"2014-02-13 08:10:00","2014-02-13 08:25:00",0.4,0.6])
        list_mindwave_data.append([0,"2014-02-13 08:25:00","2014-02-13 08:40:00",0.6,0.4])

        start_datetime_activitydetail = datetime.datetime.strptime("2014-02-13 08:00:00","%Y-%m-%d %H:%M:%S")
        end_datetime_activitydetail = datetime.datetime.strptime("2014-02-13 08:05:00","%Y-%m-%d %H:%M:%S")

        attention_avg, meditation_avg = Data_processing.calculate_average_mindwave(start_datetime_activitydetail,end_datetime_activitydetail,list_mindwave_data)

        self.assertEqual(round(attention_avg,2),0.20)
        self.assertEqual(round(meditation_avg,2),0.80)
   # def test_input_long_period(self):
   #     start_datetime_activitydetail = datetime.datetime.strptime("2014-02-13 08:00:00","%Y-%m-%d %H:%M:%S")
   #     datetime_to =  datetime.datetime.strptime("2013-12-28 11:15:00","%Y-%m-%d %H:%M:%S")

    def test_calculate_average_mindwave_3(self):
        list_mindwave_data = []
        list_mindwave_data.append([0,"2014-02-20 09:02:00","2014-02-20 09:06:00",0.2,0.8])
        list_mindwave_data.append([0,"2014-02-20 09:06:00","2014-02-20 09:10:00",0.4,0.6])
        list_mindwave_data.append([0,"2014-02-20 09:10:00","2014-02-20 09:14:00",0.6,0.4])

        start_datetime_activitydetail = datetime.datetime.strptime("2014-02-20 09:00:00","%Y-%m-%d %H:%M:%S")
        end_datetime_activitydetail = datetime.datetime.strptime("2014-02-20 09:05:00","%Y-%m-%d %H:%M:%S")

        attention_avg, meditation_avg = Data_processing.calculate_average_mindwave(start_datetime_activitydetail,end_datetime_activitydetail,list_mindwave_data)

        self.assertEqual(round(attention_avg,2),0.20)
        self.assertEqual(round(meditation_avg,2),0.80)
   # def test_input_long_period(self):
   #     start_datetime_activitydetail = datetime.datetime.strptime("2014-02-13 08:00:00","%Y-%m-%d %H:%M:%S")
   #     datetime_to =  datetime.datetime.strptime("2013-12-28 11:15:00","%Y-%m-%d %H:%M:%S")


    def test_create_list_important_activities(self):
        datetime_from = datetime.datetime.strptime("2014-02-20 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-02-20 10:10:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]
        #output.show_results(datetime_from,datetime_to,options_reason,15)
        listImportantActivities = Data_processing.getListImportantActivities(datetime_from,datetime_to,options_reason,self.link_to_main)

        """
        print "================="
        print listImportantActivities
        print "================="
        """

        self.assertEqual(listImportantActivities[0][0],'A')
        self.assertEqual(listImportantActivities[0][1],1290)
        self.assertEqual(round(listImportantActivities[0][2],2),0.46)
        #Attention + Meditation
        self.assertEqual(round(listImportantActivities[0][5],2),-1)
        self.assertEqual(round(listImportantActivities[0][6],2),-1)

        self.assertEqual(listImportantActivities[1][0],'B')
        self.assertEqual(listImportantActivities[1][1],305)
        self.assertEqual(round(listImportantActivities[1][2],2),0.85)

        #Attention + Meditation
        self.assertEqual(round(listImportantActivities[1][5],2),-1)
        self.assertEqual(round(listImportantActivities[1][6],2),-1)

    def test_create_list_unimportant_activities(self):
        datetime_from = datetime.datetime.strptime("2014-02-20 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-02-20 10:10:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]

        #presentation_tier.show_results(datetime_from,datetime_to,options_reason,15)
        listUnImportantActivities = Data_processing.getListUnimportantActivities(datetime_from,datetime_to,self.link_to_main)
        """
        print "================="
        print listUnImportantActivities
        print "================="
        """
        self.assertEqual(listUnImportantActivities[0][0],'D')
        self.assertEqual(listUnImportantActivities[0][1],305)
        #Attention + Meditation
        self.assertEqual(round(listUnImportantActivities[0][2],2),0.69)
        self.assertEqual(round(listUnImportantActivities[0][3],2),0.53)

        self.assertEqual(listUnImportantActivities[1][0],'E')
        self.assertEqual(listUnImportantActivities[1][1],200)
        #Attention + Meditation
        self.assertEqual(round(listUnImportantActivities[1][2],2),0.28)
        self.assertEqual(round(listUnImportantActivities[1][3],2),0.88)

    def test_worksessions(self):
        datetime_from = datetime.datetime.strptime("2014-02-20 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2014-02-20 10:10:00","%Y-%m-%d %H:%M:%S")
        options_reason = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]
        list_worksessions = Data_processing.get_list_work_sessions(datetime_from,datetime_to,options_reason,10,self.link_to_main)
        print '=+=+=+=+=+=+=+=+=+=+=+=+=+='
        print list_worksessions
        print '=+=+=+=+=+=+=+=+=+=+=+=+=+='

        self.assertEqual(list_worksessions[0][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 08:00:00")
        self.assertEqual(list_worksessions[0][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 08:05:00")
        #self.assertEqual(list_worksessions[0][2],'studying')
        self.assertEqual(list_worksessions[0][3],False)
        self.assertEqual(list_worksessions[0][4],300)

        self.assertEqual(list_worksessions[1][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 08:05:00")
        self.assertEqual(list_worksessions[1][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 08:08:00")
        #self.assertEqual(list_worksessions[1][2],'studying')
        self.assertEqual(list_worksessions[1][3],True)
        self.assertEqual(list_worksessions[1][4],180)

        self.assertEqual(list_worksessions[2][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 08:08:00")
        self.assertEqual(list_worksessions[2][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 08:30:00")
        self.assertEqual(list_worksessions[2][2],'break')
        self.assertEqual(list_worksessions[2][3],False)
        self.assertEqual(list_worksessions[2][4],1320)

        self.assertEqual(list_worksessions[3][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 08:30:00")
        self.assertEqual(list_worksessions[3][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:00:00")
        self.assertEqual(list_worksessions[3][2],'no tracking info')
        self.assertEqual(list_worksessions[3][3],False)
        self.assertEqual(list_worksessions[3][4],1799)

        self.assertEqual(list_worksessions[4][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:00:00")
        self.assertEqual(list_worksessions[4][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:05:00")
        #self.assertEqual(list_worksessions[4][2],'studying')
        self.assertEqual(list_worksessions[4][3],True)
        self.assertEqual(list_worksessions[4][4],300)

        self.assertEqual(list_worksessions[5][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:05:00")
        self.assertEqual(list_worksessions[5][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:10:00")
        #self.assertEqual(list_worksessions[5][2],'studying')
        self.assertEqual(list_worksessions[5][3],False)
        self.assertEqual(list_worksessions[5][4],300)

        self.assertEqual(list_worksessions[6][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:10:00")
        self.assertEqual(list_worksessions[6][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:16:00")
        #self.assertEqual(list_worksessions[6][2],'notes')
        self.assertEqual(list_worksessions[6][3],True)
        self.assertEqual(list_worksessions[6][4],360)

        self.assertEqual(list_worksessions[7][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:16:00")
        self.assertEqual(list_worksessions[7][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:18:00")
        self.assertEqual(list_worksessions[7][2],'notes')
        self.assertEqual(list_worksessions[7][3],True)
        self.assertEqual(list_worksessions[7][4],120)

        self.assertEqual(list_worksessions[8][0].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:18:00")
        self.assertEqual(list_worksessions[8][1].strftime("%Y-%m-%d %H:%M:%S"),"2014-02-20 09:25:00")
        self.assertEqual(list_worksessions[8][2],'')
        self.assertEqual(list_worksessions[8][3],True)
        self.assertEqual(list_worksessions[8][4],419)

        list_worksessions_amount_details = Data_processing.get_list_workSession_amount_details(list_worksessions,options_reason)
        print '/-/-/-/-/-/-/-//-/'
        print list_worksessions_amount_details
        print '/-/-/-/-/-/-/-//-/'

        # studying
        # total
        self.assertEqual(list_worksessions_amount_details[0][2],1380)
        # amount
        self.assertEqual(list_worksessions_amount_details[0][3],3)
        # gemiddeld
        self.assertEqual(list_worksessions_amount_details[0][4],460)
        # min
        self.assertEqual(list_worksessions_amount_details[0][5],180)
        # max
        self.assertEqual(list_worksessions_amount_details[0][6],900)


if __name__ == '__main__':
    unittest.main()