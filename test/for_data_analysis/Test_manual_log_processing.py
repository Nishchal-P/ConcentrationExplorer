import datetime
from for_data_analysis import Manual_log_processing
import unittest
import numpy as np
from for_data_analysis import Calculate_statistics_enumeration

class test_manualLogProcessing(unittest.TestCase):
    def test_get_list_concentration_differences_manual_log(self):
        manualLogDataProcessing = Manual_log_processing.ManualLog_data_processing('../../')
        dates = []
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:01","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:02","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:03","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:04","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:05","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:06","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:07","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:08","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:09","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:10","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:11","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:12","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:13","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:14","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:15","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:16","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:17","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:18","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:19","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:20","%Y-%m-%d %H:%M:%S"))

        mindwave_data = []

        mindwave_data.append([dates[0],dates[1],0.2,0.2,0,0])
        mindwave_data.append([dates[1],dates[2],0.4,0.5,0,0])
        mindwave_data.append([dates[2],dates[3],0.8,0.2,0,0])
        mindwave_data.append([dates[3],dates[4],0.1,0.5,0,0])
        mindwave_data.append([dates[4],dates[5],0.9,0.1,0,0])
        mindwave_data.append([dates[5],dates[6],0.4,0.8,0,0])
        mindwave_data.append([dates[6],dates[7],0.8,0.3,0,0])
        mindwave_data.append([dates[7],dates[8],0.2,0.6,0,0])
        mindwave_data.append([dates[8],dates[9],0.0,1.0,0,0])
        mindwave_data.append([dates[9],dates[10],0.4,0.5,0,0])

        mindwave_data.append([dates[10],dates[11],0.2,0.2,0,0])
        mindwave_data.append([dates[11],dates[12],0.4,0.5,0,0])
        mindwave_data.append([dates[12],dates[13],0.8,0.2,0,0])
        mindwave_data.append([dates[13],dates[14],0.1,0.5,0,0])
        mindwave_data.append([dates[14],dates[15],0.9,0.1,0,0])
        mindwave_data.append([dates[15],dates[16],0.4,0.8,0,0])
        mindwave_data.append([dates[16],dates[17],0.8,0.3,0,0])
        mindwave_data.append([dates[17],dates[18],0.2,0.6,0,0])
        mindwave_data.append([dates[18],dates[19],0.0,1.0,0,0])
        mindwave_data.append([dates[19],dates[20],0.4,0.5,0,0])

        manual_log_list = []
        manual_log_list.append([dates[6],dates[7],"testing"])
        manual_log_list.append([dates[9],dates[10],"testing"])
        manual_log_list.append([dates[17],dates[18],"testing"])


        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")

        result_x, result_y = manualLogDataProcessing.get_list_concentration_differences_manual_log(manual_log_list,mindwave_data)

        self.assertEqual(round(result_y[0],2),-0.16)
        self.assertEqual(round(result_y[1],2),-0.10)
        self.assertEqual(round(result_y[2],2),0)
        print "result x:"
        print result_x

        print "result y"
        print result_y

    def test_get_statistics_attention_userstates(self):
        manualLogDataProcessing = Manual_log_processing.ManualLog_data_processing('../../')
        dates = []
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:01","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:02","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:03","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:04","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:05","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:06","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:07","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:08","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:09","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:10","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:11","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:12","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:13","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:14","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:15","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:16","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:17","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:18","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:19","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:20","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:21","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:22","%Y-%m-%d %H:%M:%S"))

        mindwave_data = []

        mindwave_data.append([dates[0],dates[1],0.2,0.2,0,0])
        mindwave_data.append([dates[1],dates[2],0.4,0.5,0,0])
        mindwave_data.append([dates[2],dates[3],0.8,0.2,0,0])
        mindwave_data.append([dates[3],dates[4],0.1,0.5,0,0])
        mindwave_data.append([dates[4],dates[5],0.9,0.1,0,0])
        mindwave_data.append([dates[5],dates[6],0.4,0.8,0,0])
        mindwave_data.append([dates[6],dates[7],0.8,0.3,0,0])
        mindwave_data.append([dates[7],dates[8],0.2,0.6,0,0])
        mindwave_data.append([dates[8],dates[9],0.0,1.0,0,0])
        mindwave_data.append([dates[9],dates[10],0.4,0.5,0,0])

        mindwave_data.append([dates[10],dates[11],0.2,0.2,0,0])
        mindwave_data.append([dates[11],dates[12],0.4,0.5,0,0])
        mindwave_data.append([dates[12],dates[13],0.8,0.2,0,0])
        mindwave_data.append([dates[13],dates[14],0.1,0.5,0,0])
        mindwave_data.append([dates[14],dates[15],0.9,0.1,0,0])
        mindwave_data.append([dates[15],dates[16],0.4,0.8,0,0])
        mindwave_data.append([dates[16],dates[17],0.8,0.3,0,0])
        mindwave_data.append([dates[17],dates[18],0.2,0.6,0,0])
        mindwave_data.append([dates[18],dates[19],0.0,1.0,0,0])
        mindwave_data.append([dates[19],dates[20],0.4,0.5,0,0])

        lezen = "lezen"
        typen = "typen"
        activities = [lezen,typen]
        manual_log_list = []
        manual_log_list.append([dates[6],dates[9],lezen])
        manual_log_list.append([dates[12],dates[15],typen])
        manual_log_list.append([dates[15],dates[18],typen])
        manual_log_list.append([dates[21],dates[22],lezen])


        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")
        lezen_list = []
        lezen_list.append(mindwave_data[6][2])
        lezen_list.append(mindwave_data[7][2])
        lezen_list.append(mindwave_data[8][2])

        typen_list = []
        typen_list.append(mindwave_data[12][2])
        typen_list.append(mindwave_data[13][2])
        typen_list.append(mindwave_data[14][2])
        typen_list.append(mindwave_data[15][2])
        typen_list.append(mindwave_data[16][2])
        typen_list.append(mindwave_data[17][2])

        #window van de functie moet op 5 ingesteld zijn!!
        result_x_avg, result_y_avg = manualLogDataProcessing.get_statistics_attention_userstates(activities,manual_log_list,mindwave_data,Calculate_statistics_enumeration.AVG)

        self.assertEqual(result_y_avg[0],round(np.mean(lezen_list),2))
        self.assertEqual(result_y_avg[1],round(np.mean(typen_list),2))
        self.assertEqual(len(result_y_avg),2)

        result_x_std, result_y_std = manualLogDataProcessing.get_statistics_attention_userstates(activities,manual_log_list,mindwave_data,Calculate_statistics_enumeration.STD)

        self.assertEqual(result_y_std[0],np.std(lezen_list))
        self.assertEqual(result_y_std[1],np.std(typen_list))
        self.assertEqual(len(result_y_avg),2)

    def test_get_list_concentration_differences_manual_log_specific_switch(self):
        manualLogDataProcessing = Manual_log_processing.ManualLog_data_processing('')
        dates = []
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:01","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:02","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:03","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:04","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:05","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:06","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:07","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:08","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:09","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:10","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:11","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:12","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:13","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:14","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:15","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:16","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:17","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:18","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:19","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:20","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:21","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:22","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:23","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:24","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:25","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:26","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:27","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:28","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:29","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:30","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:31","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:32","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:33","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:34","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:35","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:36","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:37","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:38","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:39","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:40","%Y-%m-%d %H:%M:%S"))

        mindwave_data = []

        mindwave_data.append([dates[0],dates[1],0.2,0.2,0,0])
        mindwave_data.append([dates[1],dates[2],0.4,0.5,0,0])
        mindwave_data.append([dates[2],dates[3],0.8,0.2,0,0])
        mindwave_data.append([dates[3],dates[4],0.1,0.5,0,0])
        mindwave_data.append([dates[4],dates[5],0.9,0.1,0,0])
        mindwave_data.append([dates[5],dates[6],0.4,0.8,0,0])
        mindwave_data.append([dates[6],dates[7],0.8,0.3,0,0])
        mindwave_data.append([dates[7],dates[8],0.2,0.6,0,0])
        mindwave_data.append([dates[8],dates[9],0.0,1.0,0,0])
        mindwave_data.append([dates[9],dates[10],0.4,0.5,0,0])

        mindwave_data.append([dates[10],dates[11],0.2,0.2,0,0])
        mindwave_data.append([dates[11],dates[12],0.4,0.5,0,0])
        mindwave_data.append([dates[12],dates[13],0.8,0.2,0,0])
        mindwave_data.append([dates[13],dates[14],0.1,0.5,0,0])
        mindwave_data.append([dates[14],dates[15],0.9,0.1,0,0])
        mindwave_data.append([dates[15],dates[16],0.4,0.8,0,0])
        mindwave_data.append([dates[16],dates[17],0.8,0.3,0,0])
        mindwave_data.append([dates[17],dates[18],0.2,0.6,0,0])
        mindwave_data.append([dates[18],dates[19],0.0,1.0,0,0])
        mindwave_data.append([dates[19],dates[20],0.4,0.5,0,0])
        mindwave_data.append([dates[20],dates[21],0.4,0.5,0,0])
        mindwave_data.append([dates[21],dates[22],0.3,0.5,0,0])
        mindwave_data.append([dates[22],dates[23],0.2,0.5,0,0])
        mindwave_data.append([dates[23],dates[24],0.1,0.5,0,0])
        mindwave_data.append([dates[24],dates[25],0.2,0.5,0,0])
        mindwave_data.append([dates[25],dates[26],0.8,0.5,0,0])
        mindwave_data.append([dates[26],dates[27],0.7,0.5,0,0])
        mindwave_data.append([dates[27],dates[28],0.6,0.5,0,0])
        mindwave_data.append([dates[28],dates[29],0.4,0.5,0,0])
        mindwave_data.append([dates[29],dates[30],0.5,0.5,0,0])
        mindwave_data.append([dates[30],dates[31],0.2,0.5,0,0])
        mindwave_data.append([dates[31],dates[32],0.1,0.5,0,0])
        mindwave_data.append([dates[32],dates[33],0.9,0.5,0,0])
        mindwave_data.append([dates[33],dates[34],0.8,0.5,0,0])
        mindwave_data.append([dates[34],dates[35],0.5,0.5,0,0])
        mindwave_data.append([dates[35],dates[36],0.9,0.5,0,0])
        mindwave_data.append([dates[36],dates[37],0.5,0.5,0,0])
        mindwave_data.append([dates[37],dates[38],0.1,0.5,0,0])
        mindwave_data.append([dates[38],dates[39],0.3,0.5,0,0])
        mindwave_data.append([dates[39],dates[40],0.8,0.5,0,0])

        manual_log_list = []
        manual_log_list.append([dates[6],dates[7],"testing_1"])
        manual_log_list.append([dates[7],dates[10],"testing_2"])
        manual_log_list.append([dates[10],dates[18],"testing_1"])
        manual_log_list.append([dates[18],dates[24],"testing_2"])
        manual_log_list.append([dates[24],dates[27],"testing_1"])
        manual_log_list.append([dates[27],dates[31],"testing_3"])
        manual_log_list.append([dates[31],dates[35],"testing_1"])
        manual_log_list.append([dates[35],dates[38],"testing_2"])


        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")
        #window moet op 5 staan!!
        result_x, result_y = manualLogDataProcessing.get_list_concentration_differences_manual_log_specific_switch(manual_log_list,mindwave_data,"testing_1","testing_2")

        print "result x specialised:"
        print result_x

        print "result y specialised:"
        print result_y

        self.assertEqual(round(result_y[0],2),-0.28)
        self.assertEqual(round(result_y[1],2),-0.22)
        self.assertEqual(round(result_y[2],2),-0.04)

if __name__ == '__main__':
    unittest.main()