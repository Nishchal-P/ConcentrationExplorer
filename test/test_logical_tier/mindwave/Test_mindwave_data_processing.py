from logical_tier import Data_processing

__author__ = 'Peter'

from presentation_tier import Output
import datetime
import unittest
import numpy as np
import math
from logical_tier.mindwave import Mindwave_data_processing


class TestSequenceFunctions(unittest.TestCase):

    def test_convert_mindwave_data_to_RescueTime_intervals(self):
        list_dates_Rescuetime = [["2014-04-24 14:00:00"],["2014-04-24 14:05:00"],["2014-04-24 14:10:00"]]
        list_mindwave_data = []
        list_mindwave_data.append([0,"2014-04-24 14:00:00",None,0.50,0.40,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:01:00",None,0.10,0.20,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:02:00",None,0.60,0.30,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:03:00",None,0.80,0.50,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:04:00",None,0.10,0.50,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:05:00",None,0.10,0.10,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:06:00",None,0.50,0.90,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:07:00",None,0.60,0.40,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:08:00",None,0.80,0.60,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:09:00",None,0.40,0.20,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:10:00",None,0.60,0.30,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:11:00",None,0.20,0.60,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:12:00",None,0.80,0.80,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:13:00",None,0.10,0.60,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:14:00",None,0.30,0.10,None,None])
        list_mindwave_data.append([0,"2014-04-24 14:15:00",None,0.50,0.20,None,None])

        attention_data_original = []
        meditation_data_original = []

        for item in list_mindwave_data:
            attention_data_original.append(item[3])
            meditation_data_original.append(item[4])

        x_axix,attention_data,meditation_data = Mindwave_data_processing.convert_mindwave_data_to_RescueTime_intervals(list_mindwave_data, list_dates_Rescuetime)

        self.assertEqual(round(attention_data[0],2),round(np.mean(attention_data_original[0:6]),2))
        self.assertEqual(round(attention_data[1],2),round(np.mean(attention_data_original[6:11]),2))
        self.assertEqual(round(attention_data[2],2),round(np.mean(attention_data_original[11:16]),2))

        self.assertEqual(round(meditation_data[0],2),round(np.mean(meditation_data_original[0:6]),2))
        self.assertEqual(round(meditation_data[1],2),round(np.mean(meditation_data_original[6:11]),2))
        self.assertEqual(round(meditation_data[2],2),round(np.mean(meditation_data_original[11:16]),2))

    def test_get_attention_meditation_buckets(self):
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

        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")

        attention_bucket, meditation_bucket = Mindwave_data_processing.get_attention_meditation_buckets(datetime_from,datetime_to,mindwave_data)

        self.assertEqual(attention_bucket[0],0.20)
        self.assertEqual(attention_bucket[1],0.20)
        self.assertEqual(attention_bucket[2],0.30)
        self.assertEqual(attention_bucket[3],0.0)
        self.assertEqual(attention_bucket[4],0.3)

        self.assertEqual(meditation_bucket[0],0.1)
        self.assertEqual(meditation_bucket[1],0.3)
        self.assertEqual(meditation_bucket[2],0.3)
        self.assertEqual(meditation_bucket[3],0.1)
        self.assertEqual(meditation_bucket[4],0.2)

        print str("attention_bucket")
        print attention_bucket
        print str("meditation_bucket")
        print meditation_bucket

    def test_merge_buckets(self):
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

        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")

        attention_bucket, meditation_bucket = Mindwave_data_processing.get_attention_meditation_buckets(datetime_from,datetime_to,mindwave_data)

        attention_bucket_array = [attention_bucket, attention_bucket]
        meditation_bucket_array = [meditation_bucket, meditation_bucket]

        attention_bucket_result, meditation_bucket_result = Mindwave_data_processing.merge_buckets(attention_bucket_array, meditation_bucket_array)

        self.assertEqual(attention_bucket_result[0],0.20)
        self.assertEqual(attention_bucket_result[1],0.20)
        self.assertEqual(attention_bucket_result[2],0.30)
        self.assertEqual(attention_bucket_result[3],0.0)
        self.assertEqual(attention_bucket_result[4],0.3)

        self.assertEqual(meditation_bucket_result[0],0.1)
        self.assertEqual(meditation_bucket_result[1],0.3)
        self.assertEqual(meditation_bucket_result[2],0.3)
        self.assertEqual(meditation_bucket_result[3],0.1)
        self.assertEqual(meditation_bucket_result[4],0.2)

        print str("attention_bucket")
        print attention_bucket_result
        print str("meditation_bucket")
        print meditation_bucket_result

    def test_get_sublist(self):
        dates = []
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:01.630000","%Y-%m-%d %H:%M:%S.%f"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:02.630000","%Y-%m-%d %H:%M:%S.%f"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:03","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:04","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:05","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:06","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:07","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:08","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:09","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:10","%Y-%m-%d %H:%M:%S"))
        mindwave_data = []

        mindwave_data.append([dates[0],dates[1],0.2,0.2])
        mindwave_data.append([dates[1],dates[2],0.4,0.5])
        mindwave_data.append([dates[2],dates[3],0.8,0.2])
        mindwave_data.append([dates[3],dates[4],0.1,0.5])
        mindwave_data.append([dates[4],dates[5],0.9,0.1])
        mindwave_data.append([dates[5],dates[6],0.4,0.8])
        mindwave_data.append([dates[6],dates[7],0.8,0.3])
        mindwave_data.append([dates[7],dates[8],0.2,0.6])
        mindwave_data.append([dates[8],dates[9],0.0,1.0])
        mindwave_data.append([dates[9],dates[10],0.4,0.5])

        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:02","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:00:10","%Y-%m-%d %H:%M:%S")

        sublist = Mindwave_data_processing.get_sublist(mindwave_data,datetime_from,datetime_to)

        self.assertEqual(sublist[0][0],dates[2])
        self.assertEqual(sublist[len(sublist)-1][1],dates[10])
        self.assertEqual(len(sublist),8)

    def test_calculate_avg_attention_meditation(self):
        dates = []
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:01.630000","%Y-%m-%d %H:%M:%S.%f"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:02.630000","%Y-%m-%d %H:%M:%S.%f"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:03","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:04","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:05","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:06","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:07","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:08","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:09","%Y-%m-%d %H:%M:%S"))
        dates.append(datetime.datetime.strptime("2013-12-28 08:00:10","%Y-%m-%d %H:%M:%S"))
        mindwave_data = []

        mindwave_data.append([dates[0],dates[1],0.2,0.2])
        mindwave_data.append([dates[1],dates[2],0.4,0.5])
        mindwave_data.append([dates[2],dates[3],0.8,0.2])
        mindwave_data.append([dates[3],dates[4],0.1,0.5])
        mindwave_data.append([dates[4],dates[5],0.9,0.1])
        mindwave_data.append([dates[5],dates[6],0.4,0.8])

        attention_avg, meditation_avg = Mindwave_data_processing.calculate_avg_attention_meditation(mindwave_data)
        self.assertEqual(round(attention_avg,2),0.47)
        self.assertEqual(round(meditation_avg,2),0.38)

if __name__ == '__main__':
    unittest.main()