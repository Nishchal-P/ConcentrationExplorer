import unittest
import datetime
from logical_tier import List_operations
from logical_tier.read_detection import Read_detection_tracking

class TestStatistics(unittest.TestCase):
    treshold_length_array_x_coordinates_iris = 20

    treshold_read_samples_line = 4
    treshold_ratio_pos_neg_read_samples = 1.2

    treshold_readLines_positive = 2
    treshold_readLines_negative = 2
    treshold_from_neg_to_pos = 2

    treshold_window_selection = 3
    treshold_second_derivative = 1.0

    # tresholds for window selection
    treshold_window_selection_total_pos = 1.0
    treshold_window_selection_relative_marge_difference_amount_pos = 0.1

    readDetection = Read_detection_tracking.ReadDetection('../../')

    readDetection.set_tresholds(treshold_from_neg_to_pos, treshold_length_array_x_coordinates_iris,
                      treshold_ratio_pos_neg_read_samples, treshold_readLines_negative, treshold_readLines_positive,
                      treshold_read_samples_line, treshold_second_derivative, treshold_window_selection,
                      treshold_window_selection_relative_marge_difference_amount_pos,
                      treshold_window_selection_total_pos)

    def test_read_detection(self):
        input_list = [-1, 102.0, 205.0, 308, 306, 305, 310, 310, 309, 309, 308, 309, 311, 312.0, 313, 313, 313, 314, 314, 314, 314, 313, 313, 312, 312, 311, 312, 311, 311, 310, 310, 311, 310, 308, 309, 306, 307, 305, 303.0, 301, 302, 301.5, 301, 297, 298, 300, 299, 296, 298, 296, 295, 294, 297, 303, 307, 311, 311, 312.0, 313, 313, 312, 312, 312, 311, 311, 309, 309.0, 309, 309, 309, 309, 308, 304.5, 301, 305, 304.6666666666667, 304.33333333333337, 304, 304, 304, 302, 302, 298, 301, 298, 299, 296, 300, 299, 298, 297, 296, 296, 295, 292, 294, 292, 291, 302, 307, 313, 315, 317, 314, 315, 313, 306, 307, 309, 309, 307, 310, 307.5, 305, 302, 289, 306, 306, 305, 304, 304, 302, 302, 301, 300, 302, 299, 298, 298, 296, 298, 295, 295, 292, 291, 292, 289, 289, 289.0, 289, 305, 313, 315, 315, 315, 314, 312.5, 311, 311, 310, 310, 309, 309, 309, 308, 308, 306, 305, 303, 303, 302, 301, 300, 299.0, 298, 301, 300, 299, 297.5, 296, 295, 292, 290, 290, 290.0, 290, 288, 288, 288, 287, 293, 298, 306, 312.0, 318, 315.0, 312, 312, 311, 311, 309, 308, 309, 307.5, 306, 309, 307, 305, 307, 306, 305, 305, 306, 305, 304, 304, 303.0, 302, 301, 300, 301, 300, 299, 296, 294, 294, 293.0, 292, 292, 291, 289, 289, 292, 293, 302, 317, 314.5, 312.0, 309.5, 307, 309, 302, 303.6666666666667, 305.33333333333337, 307, 296, 294.6666666666667, 293.33333333333337, 292, 304, 306, 306, 302, 303, 302, 302, 301, 301, 301, 299, 298, 295, 294, 295, 293, 293, 292, 293, 291, 292, 291, 288, 287, 288, 287, 294, 293, 303, 309, 314, 317, 298, 316, 315, 312, 312, 310, 309, 308.0, 307, 305, 305, 304, 302, 302, 302, 299, 300, 299, 298, 298.0, 298, 296, 294, 294, 293, 293, 289, 289, 286]
        input_list = input_list + input_list[3:(len(input_list) - 1)]+ input_list[3:(len(input_list) - 1)]+ input_list[3:(len(input_list) - 1)]
        input_list_dates = []

        for i in range(0,len(input_list)):
            input_list_dates.append(i)

        self.assertEqual(len(input_list),len(input_list_dates))

        dataset = self.readDetection.analyse_list_for_reading_patterns_2(input_list,input_list_dates,"reading_1")
        #self.assertEqual(dataset[0][0],60)
        #self.assertEqual(dataset[0][1],299)
        print 'dataset 1'
        print dataset

    def test_read_detection_2(self):
        input_list = [-1, 102.0, 205.0, 308, 306, 305, 310, 310, 309, 309, 308, 309, 311, 312.0, 313, 313, 313, 314, 314, 314, 314, 313, 313, 312, 312, 311, 312, 311, 311, 310, 310, 311, 310, 308, 309, 306, 307, 305, 303.0, 301, 302, 301.5, 301, 297, 298, 300, 299, 296, 298, 296, 295, 294, 297, 303, 307, 311, 311, 312.0, 313, 313, 312, 312, 312, 311, 311, 309, 309.0, 309, 309, 309, 309, 308, 304.5, 301, 305, 304.6666666666667, 304.33333333333337, 304, 304, 304, 302, 302, 298, 301, 298, 299, 296, 300, 299, 298, 297, 296, 296, 295, 292, 294, 292, 291, 302, 307, 313, 315, 317, 314, 315, 313, 306, 307, 309, 309, 307, 310, 307.5, 305, 302, 289, 306, 306, 305, 304, 304, 302, 302, 301, 300, 302, 299, 298, 298, 296, 298, 295, 295, 292, 291, 292, 289, 289, 289.0, 289, 305, 313, 315, 315, 315, 314, 312.5, 311, 311, 310, 310, 309, 309, 309, 308, 308, 306, 305, 303, 303, 302, 301, 300, 299.0, 298, 301, 300, 299, 297.5, 296, 295, 292, 290, 290, 290.0, 290, 288, 288, 288, 287, 293, 298, 306, 312.0, 318, 315.0, 312, 312, 311, 311, 309, 308, 309, 307.5, 306, 309, 307, 305, 307, 306, 305, 305, 306, 305, 304, 304, 303.0, 302, 301, 300, 301, 300, 299, 296, 294, 294, 293.0, 292, 292, 291, 289, 289, 292, 293, 302, 317, 314.5, 312.0, 309.5, 307, 309, 302, 303.6666666666667, 305.33333333333337, 307, 296, 294.6666666666667, 293.33333333333337, 292, 304, 306, 306, 302, 303, 302, 302, 301, 301, 301, 299, 298, 295, 294, 295, 293, 293, 292, 293, 291, 292, 291, 288, 287, 288, 287, 294, 293, 303, 309, 314, 317, 298, 316, 315, 312, 312, 310, 309, 308.0, 307, 305, 305, 304, 302, 302, 302, 299, 300, 299, 298, 298.0, 298, 296, 294, 294, 293, 293, 289, 289, 286,50,80,60,50,30,80,70,50,60,90,50,200,80,690,40,60,850,60,520,60,850,60,90,80,960,90,80,90,80,90,50,80,90,560,80,690,850]
        input_list_dates = []

        for i in range(0,len(input_list)):
            input_list_dates.append(i)

        self.assertEqual(len(input_list),len(input_list_dates))

        dataset = self.readDetection.analyse_list_for_reading_patterns_2(input_list,input_list_dates,"reading_2")
        #self.assertEqual(dataset[0][0],60)
        #self.assertEqual(dataset[0][1],241)
        print 'dataset 2'
        print dataset

    def test_read_detection_3(self):
        input_list = [-1, 102.0, 205.0, 308, 306, 305, 310, 310, 309, 309, 308, 309, 311, 312.0, 313, 313, 313, 314, 314, 314, 314, 313, 313, 312, 312, 311, 312, 311, 311, 310, 310, 311, 310, 308, 309, 306, 307, 305, 303.0, 301, 302, 301.5, 301, 297, 298, 300, 299, 296, 298, 296, 295, 294, 297, 303, 307, 311, 311, 312.0, 313, 313, 312, 312, 312, 311, 311, 309, 309.0, 309, 309, 309, 309, 308, 304.5, 301, 305, 304.6666666666667, 304.33333333333337, 304, 304, 304, 302, 302, 298, 301, 298, 299, 296, 300, 299, 298, 297, 296, 296, 295, 292, 294, 292, 291, 302, 307, 313, 315, 317, 314, 315, 313, 306, 307, 309, 309, 307, 310, 307.5, 305, 302, 289, 306, 306, 305, 304, 304, 302, 302, 301, 300, 302, 299, 298, 298, 296, 298, 295, 295, 292, 291, 292, 289, 289, 289.0, 289, 305, 313, 315, 315, 315, 314, 312.5, 311, 311, 310, 310, 309, 309, 309, 308, 308, 306, 305, 303, 303, 302, 301, 300, 299.0, 298, 301, 300, 299, 297.5, 296, 295, 292, 290, 290, 290.0, 290, 288, 288, 288, 287, 293, 298, 306, 312.0, 318, 315.0, 312, 312, 311, 311, 309, 308, 309, 307.5, 306, 309, 307, 305, 307, 306, 305, 305, 306, 305, 304, 304, 303.0, 302, 301, 300, 301, 300, 299, 296, 294, 294, 293.0, 292, 292, 291, 289, 289, 292, 293, 302, 317, 314.5, 312.0, 309.5, 307, 309, 302, 303.6666666666667, 305.33333333333337, 307, 296, 294.6666666666667, 293.33333333333337, 292, 304, 306, 306, 302, 303, 302, 302, 301, 301, 301, 299, 298, 295, 294, 295, 293, 293, 292, 293, 291, 292, 291, 288, 287, 288, 287, 294, 293, 303, 309, 314, 317, 298, 316, 315, 312, 312, 310, 309, 308.0, 307, 305, 305, 304, 302, 302, 302, 299, 300, 299, 298, 298.0, 298, 296, 294, 294, 293, 293, 289, 289, 286,50,80,60,50,30,80,70,50,60,90,50,200,80,690,40,60,850,60,520,60,850,60,90,80,960,90,80,90,80,90,50,80,90,560,80,690,850]
        input_list_dates = []

        for i in range(0,len(input_list)):
            input_list_dates.append(i)

        self.assertEqual(len(input_list),len(input_list_dates))

        dataset = self.readDetection.analyse_list_for_reading_patterns_2(input_list,input_list_dates,"reading_2")
        #self.assertEqual(dataset[0][0],60)
        #self.assertEqual(dataset[0][1],241)
        print 'dataset 2'
        print dataset


    def generate_datetime_array_35_entries(self,seconds, minutes):
        index_minutes = 0
        input_list_dates = []
        while index_minutes <= minutes:
            index_seconds = 0
            while index_seconds <= seconds:
                if index_seconds < 10:
                    input_list_dates.append(datetime.datetime.strptime("1989-12-12 08:0" + str(index_minutes) + ":0" + str(index_seconds),"%Y-%m-%d %H:%M:%S"))
                else:
                    input_list_dates.append(datetime.datetime.strptime("1989-12-12 08:" + str(index_minutes) + ":" + str(index_seconds),"%Y-%m-%d %H:%M:%S"))
                index_seconds += 1
            index_minutes += 1
        return input_list_dates


if __name__ == '__main__':
    unittest.main()
