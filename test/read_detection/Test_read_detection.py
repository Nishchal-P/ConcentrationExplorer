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
    #readDetection = Read_detection_tracking.ReadDetection('')

    readDetection.set_tresholds(treshold_from_neg_to_pos, treshold_length_array_x_coordinates_iris,
                      treshold_ratio_pos_neg_read_samples, treshold_readLines_negative, treshold_readLines_positive,
                      treshold_read_samples_line, treshold_second_derivative, treshold_window_selection,
                      treshold_window_selection_relative_marge_difference_amount_pos,
                      treshold_window_selection_total_pos)
    def test_statistics(self):
        input_list = [1,3,3,4,5,7,9,10,11,15,16]
        window_size = 4
        output_list = List_operations.movingaverage(input_list,window_size)
        print output_list

    def test_filter_list(self):
        input_list = [1,2,3,4,-1,-1,-1,8,9]
        result = self.readDetection.filter_list(input_list)
        self.assertEqual(result[0],1)
        self.assertEqual(result[1],2)
        self.assertEqual(result[2],3)
        self.assertEqual(result[3],4)
        self.assertEqual(result[4],5)
        self.assertEqual(result[5],6)
        self.assertEqual(result[6],7)
        self.assertEqual(result[7],8)
        self.assertEqual(result[8],9)

    def test_filter_list_2(self):
        input_list = [-1,2,3,4,-1,-1,-1,8,9]
        result = self.readDetection.filter_list(input_list)
        self.assertEqual(result[0],-1)
        self.assertEqual(result[1],2)
        self.assertEqual(result[2],3)
        self.assertEqual(result[3],4)
        self.assertEqual(result[4],5)
        self.assertEqual(result[5],6)
        self.assertEqual(result[6],7)
        self.assertEqual(result[7],8)
        self.assertEqual(result[8],9)

    def test_filter_list_3(self):
        input_list = [1,-1,3,4,-1,-1,7,-1]
        result = self.readDetection.filter_list(input_list)
        self.assertEqual(result[0],1)
        self.assertEqual(result[1],2)
        self.assertEqual(result[2],3)
        self.assertEqual(result[3],4)
        self.assertEqual(result[4],5)
        self.assertEqual(result[5],6)
        self.assertEqual(result[6],7)
        self.assertEqual(result[7],-1)

    def test_derivative(self):
        input_list = [1,2,5,4,7,2]
        result = self.readDetection.calculate_derivative(input_list)
        self.assertEqual(result[0],0)
        self.assertEqual(result[1],1)
        self.assertEqual(result[2],3)
        self.assertEqual(result[3],-1)
        self.assertEqual(result[4],3)
        self.assertEqual(result[5],-5)

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

    def test_reading_1(self):
        input_list = [8,7,6,5,4,3,2,5,7,8,7,6,5,4,3,2,5,7,8,7,6,5,4,3,2,5,7,8,7,6,5,4,3,2,1]

        input_list_dates = self.generate_datetime_array_35_entries(34,0)

        self.assertEqual(len(input_list),len(input_list_dates))
        dataset = self.readDetection.analyse_list_for_reading_patterns_smooth_list(input_list,input_list_dates)


        self.assertEqual(len(dataset),1)
        self.assertEqual(dataset[0][0],input_list_dates[0])
        self.assertEqual(dataset[0][1],input_list_dates[34])

    def test_reading_2(self):
        input_list = [2,1,2,3,7,1,5,4,3,5,7,6,5,4,3,2,5,7,8,7,6,5,4,3,2,5,7,8,7,6,5,4,3,2,1]

        input_list_dates = self.generate_datetime_array_35_entries(34,0)

        self.assertEqual(len(input_list),len(input_list_dates))
        dataset = self.readDetection.analyse_list_for_reading_patterns_smooth_list(input_list,input_list_dates)


        self.assertEqual(len(dataset),1)
        self.assertEqual(dataset[0][0],input_list_dates[12])
        self.assertEqual(dataset[0][1],input_list_dates[34])

    def test_reading_3(self):

        input_list = [8,7,6,5,4,3,2,5,7,8,7,6,5,4,3,2,5,5,3,2,3,5,4,5,4,5,4,5,4,5,7,8,7,6,5,4,3,2,5,7,8,7,6,5,4,3,2,1,3,7,8,7,6,5,4,7,8,7,6,5]

        input_list_dates = self.generate_datetime_array_35_entries(59,0)

        self.assertEqual(len(input_list),len(input_list_dates))
        dataset = self.readDetection.analyse_list_for_reading_patterns_smooth_list(input_list,input_list_dates)
        print 'dataset 3'
        print dataset

        self.assertEqual(len(dataset),2)
        self.assertEqual(dataset[0][0],input_list_dates[0])
        #self.assertEqual(dataset[0][1],input_list_dates[20])
        self.assertEqual(dataset[0][1],input_list_dates[22])

        self.assertEqual(dataset[1][0],input_list_dates[33])
        self.assertEqual(dataset[1][1],input_list_dates[59])

    def test_reading_4(self):
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

        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        readDetection_2.set_tresholds(treshold_from_neg_to_pos, treshold_length_array_x_coordinates_iris,
                      treshold_ratio_pos_neg_read_samples, treshold_readLines_negative, treshold_readLines_positive,
                      treshold_read_samples_line, treshold_second_derivative, treshold_window_selection,
                      treshold_window_selection_relative_marge_difference_amount_pos,
                      treshold_window_selection_total_pos)

        input_list = [5,8,1,3,9,5,6,4,2,8,2,4,8,7,6,5,4,3,4,7,8,7,6,5,4,3,7,8,7,6,5,4,3,6,5,8,9,78,5,5,4,5,8,8,9,6,5,86,5,4,5,2,65,89,7,5,5,8,45,69,8,4,5,52,5,4,5,6,8,5,8,5,8,5,6,2,5,6,8,9,8,5,4,5,8,2,7,8,7,6,5,4,3,5,7,6,5,4,3,6,8,7,6,5,4,7,8,7,6,5,4,3,5,7,9,8,7,6,5,4]
        input_list_dates = self.generate_datetime_array_35_entries(59,1)

        self.assertEqual(len(input_list),len(input_list_dates))
        dataset = readDetection_2.analyse_list_for_reading_patterns_smooth_list(input_list,input_list_dates)
        print 'dataset 4'
        print dataset

        self.assertEqual(len(dataset),2)
        self.assertEqual(dataset[0][0],input_list_dates[14])
        # In dit geval klopt het dat deze niet slaagt omdat er een hele reeks 5,4,5,4,5,4 voor de eigenlijke "leesdata" komt, maar int echt komt dit zelden voor
        # Heeft met de second derivative te maken
        #self.assertEqual(dataset[0][1],input_list_dates[34])
        self.assertEqual(dataset[1][0],input_list_dates[89])
        self.assertEqual(dataset[1][1],input_list_dates[119])


    def test_reading_5(self):

        treshold_length_array_x_coordinates_iris = 20

        treshold_read_samples_line = 3
        treshold_ratio_pos_neg_read_samples = 1.2

        treshold_readLines_positive = 2
        treshold_readLines_negative = 5
        treshold_from_neg_to_pos = 2

        treshold_window_selection = 6
        treshold_second_derivative = 1.0

        # tresholds for window selection
        treshold_window_selection_total_pos = 2.0
        treshold_window_selection_relative_marge_difference_amount_pos = 0.5

        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        readDetection_2.set_tresholds(treshold_from_neg_to_pos, treshold_length_array_x_coordinates_iris,
                      treshold_ratio_pos_neg_read_samples, treshold_readLines_negative, treshold_readLines_positive,
                      treshold_read_samples_line, treshold_second_derivative, treshold_window_selection,
                      treshold_window_selection_relative_marge_difference_amount_pos,
                      treshold_window_selection_total_pos)
        input_list_temp = [-1, 102.0, 205.0, 308, 306, 305, 310, 310, 309, 309, 308, 309, 311, 312.0, 313, 313, 313, 314, 314, 314, 314, 313, 313, 312, 312, 311, 312, 311, 311, 310, 310, 311, 310, 308, 309, 306, 307, 305, 303.0, 301, 302, 301.5, 301, 297, 298, 300, 299, 296, 298, 296, 295, 294, 297, 303, 307, 311, 311, 312.0, 313, 313, 312, 312, 312, 311, 311, 309, 309.0, 309, 309, 309, 309, 308, 304.5, 301, 305, 304.6666666666667, 304.33333333333337, 304, 304, 304, 302, 302, 298, 301, 298, 299, 296, 300, 299, 298, 297, 296, 296, 295, 292, 294, 292, 291, 302, 307, 313, 315, 317, 314, 315, 313, 306, 307, 309, 309, 307, 310, 307.5, 305, 302, 289, 306, 306, 305, 304, 304, 302, 302, 301, 300, 302, 299, 298, 298, 296, 298, 295, 295, 292, 291, 292, 289, 289, 289.0, 289, 305, 313, 315, 315, 315, 314, 312.5, 311, 311, 310, 310, 309, 309, 309, 308, 308, 306, 305, 303, 303, 302, 301, 300, 299.0, 298, 301, 300, 299, 297.5, 296, 295, 292, 290, 290, 290.0, 290, 288, 288, 288, 287, 293, 298, 306, 312.0, 318, 315.0, 312, 312, 311, 311, 309, 308, 309, 307.5, 306, 309, 307, 305, 307, 306, 305, 305, 306, 305, 304, 304, 303.0, 302, 301, 300, 301, 300, 299, 296, 294, 294, 293.0, 292, 292, 291, 289, 289, 292, 293, 302, 317, 314.5, 312.0, 309.5, 307, 309, 302, 303.6666666666667, 305.33333333333337, 307, 296, 294.6666666666667, 293.33333333333337, 292, 304, 306, 306, 302, 303, 302, 302, 301, 301, 301, 299, 298, 295, 294, 295, 293, 293, 292, 293, 291, 292, 291, 288, 287, 288, 287, 294, 293, 303, 309, 314, 317, 298, 316, 315, 312, 312, 310, 309, 308.0, 307, 305, 305, 304, 302, 302, 302, 299, 300, 299, 298, 298.0, 298, 296, 294, 294, 293, 293, 289, 289, 286]
        input_list = []
        for i in range(0,300):
            if i % 2 == 0:
                input_list.append(input_list_temp[i])
        input_list_dates = []

        for i in range(0,150):
            input_list_dates.append(i)
        self.assertEqual(len(input_list),len(input_list_dates))

        dataset = readDetection_2.analyse_list_for_reading_patterns(input_list,input_list_dates,"reading_5")
        print 'dataset 5'
        print dataset

        self.assertEqual(len(dataset),1)
        self.assertEqual(dataset[0][0],input_list_dates[13])
        self.assertEqual(dataset[0][1],input_list_dates[149])


    def test_reading_6(self):
        treshold_length_array_x_coordinates_iris = 20

        treshold_read_samples_line = 3
        treshold_ratio_pos_neg_read_samples = 1.2

        treshold_readLines_positive = 2
        treshold_readLines_negative = 6
        treshold_from_neg_to_pos = 2

        treshold_window_selection = 12
        treshold_second_derivative = 2.0

        # tresholds for window selection
        treshold_window_selection_total_pos = 2.0
        treshold_window_selection_relative_marge_difference_amount_pos = 0.5
        input_list = [-1, 102.0, 205.0, 308, 306, 305, 310, 310, 309, 309, 308, 309, 311, 312.0, 313, 313, 313, 314, 314, 314, 314, 313, 313, 312, 312, 311, 312, 311, 311, 310, 310, 311, 310, 308, 309, 306, 307, 305, 303.0, 301, 302, 301.5, 301, 297, 298, 300, 299, 296, 298, 296, 295, 294, 297, 303, 307, 311, 311, 312.0, 313, 313, 312, 312, 312, 311, 311, 309, 309.0, 309, 309, 309, 309, 308, 304.5, 301, 305, 304.6666666666667, 304.33333333333337, 304, 304, 304, 302, 302, 298, 301, 298, 299, 296, 300, 299, 298, 297, 296, 296, 295, 292, 294, 292, 291, 302, 307, 313, 315, 317, 314, 315, 313, 306, 307, 309, 309, 307, 310, 307.5, 305, 302, 289, 306, 306, 305, 304, 304, 302, 302, 301, 300, 302, 299, 298, 298, 296, 298, 295, 295, 292, 291, 292, 289, 289, 289.0, 289, 305, 313, 315, 315, 315, 314, 312.5, 311, 311, 310, 310, 309, 309, 309, 308, 308, 306, 305, 303, 303, 302, 301, 300, 299.0, 298, 301, 300, 299, 297.5, 296, 295, 292, 290, 290, 290.0, 290, 288, 288, 288, 287, 293, 298, 306, 312.0, 318, 315.0, 312, 312, 311, 311, 309, 308, 309, 307.5, 306, 309, 307, 305, 307, 306, 305, 305, 306, 305, 304, 304, 303.0, 302, 301, 300, 301, 300, 299, 296, 294, 294, 293.0, 292, 292, 291, 289, 289, 292, 293, 302, 317, 314.5, 312.0, 309.5, 307, 309, 302, 303.6666666666667, 305.33333333333337, 307, 296, 294.6666666666667, 293.33333333333337, 292, 304, 306, 306, 302, 303, 302, 302, 301, 301, 301, 299, 298, 295, 294, 295, 293, 293, 292, 293, 291, 292, 291, 288, 287, 288, 287, 294, 293, 303, 309, 314, 317, 298, 316, 315, 312, 312, 310, 309, 308.0, 307, 305, 305, 304, 302, 302, 302, 299, 300, 299, 298, 298.0, 298, 296, 294, 294, 293, 293, 289, 289, 286]
        input_list_dates = []

        for i in range(0,300):
            input_list_dates.append(i)
        self.assertEqual(len(input_list),len(input_list_dates))

        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        dataset = readDetection_2.analyse_list_for_reading_patterns(input_list,input_list_dates,"reading_6")
        print 'dataset 6'
        print dataset

        self.assertEqual(len(dataset),1)
        self.assertEqual(dataset[0][0],input_list_dates[22])
        self.assertEqual(dataset[0][1],input_list_dates[299])

    def test_reading_7(self):
        treshold_length_array_x_coordinates_iris = 20

        treshold_read_samples_line = 3
        treshold_ratio_pos_neg_read_samples = 1.2

        treshold_readLines_positive = 2
        treshold_readLines_negative = 6
        treshold_from_neg_to_pos = 2

        treshold_window_selection = 12
        treshold_second_derivative = 10.0

        # tresholds for window selection
        treshold_window_selection_total_pos = 2.0
        treshold_window_selection_relative_marge_difference_amount_pos = 0.5
        input_list = [-1, 102.0, 205.0, 308, 306, 305, 310, 310, 309, 309, 308, 309, 311, 312.0, 313, 313, 313, 314, 314, 314, 314, 313, 313, 312, 312, 311, 312, 311, 311, 310, 310, 311, 310, 308, 309, 306, 307, 305, 303.0, 301, 302, 301.5, 301, 297, 298, 300, 299, 296, 298, 296, 295, 294, 297, 303, 307, 311, 311, 312.0, 313, 313, 312, 312, 312, 311, 311, 309, 309.0, 309, 309, 309, 309, 308, 304.5, 301, 305, 304.6666666666667, 304.33333333333337, 304, 304, 304, 302, 302, 298, 301, 298, 299, 296, 300, 299, 298, 297, 296, 296, 295, 292, 294, 292, 291, 302, 307, 313, 315, 317, 314, 315, 313, 306, 307, 309, 309, 307, 310, 307.5, 305, 302, 289, 306, 306, 305, 304, 304, 302, 302, 301, 300, 302, 299, 298, 298, 296, 298, 295, 295, 292, 291, 292, 289, 289, 289.0, 289, 305, 313, 315, 315, 315, 314, 312.5, 311, 311, 310, 310, 309, 309, 309, 308, 308, 306, 305, 303, 303, 302, 301, 300, 299.0, 298, 301, 300, 299, 297.5, 296, 295, 292, 290, 290, 290.0, 290, 288, 288, 288, 287, 293, 298, 306, 312.0, 318, 315.0, 312, 312, 311, 311, 309, 308, 309, 307.5, 306, 309, 307, 305, 307, 306, 305, 305, 306, 305, 304, 304, 303.0, 302, 301, 300, 301, 300, 299, 296, 294, 294, 293.0, 292, 292, 291, 289, 289, 292, 293, 302, 317, 314.5, 312.0, 309.5, 307, 309, 302, 303.6666666666667, 305.33333333333337, 307, 296, 294.6666666666667, 293.33333333333337, 292, 304, 306, 306, 302, 303, 302, 302, 301, 301, 301, 299, 298, 295, 294, 295, 293, 293, 292, 293, 291, 292, 291, 288, 287, 288, 287, 294, 293, 303, 309, 314, 317, 298, 316, 315, 312, 312, 310, 309, 308.0, 307, 305, 305, 304, 302, 302, 302, 299, 300, 299, 298, 298.0, 298, 296, 294, 294, 293, 293, 289, 289, 286,50,80,60,50,30,80,70,50,60,90,50,200,80,690,40,60,850,60,520,60,850,60,90,80,960,90,80,90,80,90,50,80,90,560,80,690,850]
        input_list_dates = []

        for i in range(0,337):
            input_list_dates.append(i)
        self.assertEqual(len(input_list),len(input_list_dates))

        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        dataset = readDetection_2.analyse_list_for_reading_patterns(input_list,input_list_dates,"reading_7")
        print 'dataset 7'
        print dataset

        self.assertEqual(len(dataset),1)
        self.assertEqual(dataset[0][0],input_list_dates[22])
        self.assertEqual(dataset[0][1],input_list_dates[273])
        # Dit is normaal juist, maar het is begrijpbaar dat het algoritme vroeger "stop reading" detecteerd door noise in de data
        #self.assertEqual(dataset[0][1],input_list_dates[312])


    def test_reading_8_reading_stop_reading(self):
        treshold_length_array_x_coordinates_iris = 20

        treshold_read_samples_line = 3
        treshold_ratio_pos_neg_read_samples = 1.2

        treshold_readLines_positive = 2
        treshold_readLines_negative = 2
        treshold_from_neg_to_pos = 2

        treshold_window_selection = -1
        treshold_second_derivative = 1.0

        # tresholds for window selection
        treshold_window_selection_total_pos = 2.0
        treshold_window_selection_relative_marge_difference_amount_pos = 0.5


        input_list = [427, 423, -1, -1, 430, 429, 430, -1, -1, -1, -1, -1, -1, -1, 421, 413, 416, 418, 414, 412, 409, 408, 405, 400, 395, -1, 412, 414, 412, 409, 405, 404, 403, 396, 397, 395, 390, 386, 398, 412, 413, 408, 408, 406, 403, 403, -1, -1, 392, 389, 386, 404, 407, 407, 405, 402, 401, 398, 388, 394, 395, 392, 392, -1, 409, 414, 413, 409, 407, 402, 400, 398, 395, 394, 392, -1, 410, 411, 408, 405, 405, 401, 399, 397, 394, 391, 394, 400, 401, 401, 401, 401, 400, -1, -1, 398, 400, 400, 399, 399, 399, 399, 397, 398, 398, 400, 398, 398, 401, -1, 399, 400, 397, 399, 402, 405, 411, 409, 405, 402, 401, 398, 394, 393, 391, 394, 402, 411, 408, 407, 400, 401, 398, 396, 392, 391, -1, 409, 410, 411, 409, 408, 407, 405, 397, 397, 388, 394, 401, 410, 410, 407, 400, 400, 396, 398, 396, 396, 396, 397, 397]
        #filtered_list = self.readDetection.filter_list(input_list)
        #smoothed_list = self.readDetection.smooth_list(filtered_list)
        input_list_dates = []
        for i in range(0,len(input_list)):
            input_list_dates.append(i)
        #self.assertEqual(len(input_list[0:len(smoothed_list)]),len(smoothed_list))
        #self.readDetection.show_plot(input_list_dates,filtered_list[0:len(smoothed_list)],smoothed_list,"reading_10")

        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        dataset = readDetection_2.analyse_list_for_reading_patterns(input_list,input_list_dates,"reading_8_reading_stop_reading")
        print '---------------'
        print 'dataset 8'
        print dataset
        print '---------------'
        self.assertEqual(dataset[0][0],8)
        self.assertEqual(dataset[0][1],98)
        self.assertEqual(dataset[1][0],118)
        self.assertEqual(dataset[1][1],160)


    def test_reading_9_reading_wide_small(self):
        treshold_length_array_x_coordinates_iris = 20

        treshold_read_samples_line = 3
        treshold_ratio_pos_neg_read_samples = 1.2

        treshold_readLines_positive = 2
        treshold_readLines_negative = 2
        treshold_from_neg_to_pos = 2

        treshold_window_selection = -1
        treshold_second_derivative = 1.0

        # tresholds for window selection
        treshold_window_selection_total_pos = 2.0
        treshold_window_selection_relative_marge_difference_amount_pos = 0.5


        input_list = [-1, 405, -1, -1, -1, -1, 413, 413, -1, 409, 418, 415, 413, 414, -1, 416, 418, 418, 416, 417, 421, 427, 426, 426, 425, 423, 423, 420, 419, 413, -1, 406, -1, 401, 400, -1, 426, 430, 429, 427, 423, 422, 420, -1, 417, 413, 412, 410, 407, 398, -1, 400, -1, 419, 420, 419, 418, 416, 414, 411, 409, 407, 404, 402, -1, 400, 393, 394, -1, 414, 421, 420, 417, 417, 414, 413, 410, 408, -1, -1, 399, 398, 397, 393, -1, 420, 424, 424, 419, 410, 414, 410, 408, 407, 406, 402, 400, -1, 400, 414, 422, 424, 423, 421, 419, 417, 413, 418, 424, 425, -1, 422, 419, 416, 413, 422, 424, 419, 418, -1, 421, 424, 422, 417, 414, -1, 415, 424, 421, 421, 418, 413, 413, 413, 422, 424, 421, 418, 414, 409, 410, 409, 406, 406, 405]
        #filtered_list = self.readDetection.filter_list(input_list)
        #smoothed_list = self.readDetection.smooth_list(filtered_list)
        input_list_dates = []
        for i in range(0,len(input_list)):
            input_list_dates.append(i)
        #self.assertEqual(len(input_list[0:len(smoothed_list)]),len(smoothed_list))
        #self.readDetection.show_plot(input_list_dates,filtered_list[0:len(smoothed_list)],smoothed_list,"reading_10")

        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        dataset = readDetection_2.analyse_list_for_reading_patterns(input_list,input_list_dates,"reading_9_reading_wide_small")
        print '---------------'
        print 'dataset 9'
        print dataset
        print '---------------'
        self.assertEqual(dataset[0][0],26)
        self.assertEqual(dataset[0][1],111)



    def test_smooth_list(self):
        input_list = [-1, 102.0, 205.0, 308, 306, 305, 310, 310, 309, 309, 308, 309, 311, 312.0, 313, 313, 313, 314, 314, 314, 314, 313, 313, 312, 312, 311, 312, 311, 311, 310, 310, 311, 310, 308, 309, 306, 307, 305, 303.0, 301, 302, 301.5, 301, 297, 298, 300, 299, 296, 298, 296, 295, 294, 297, 303, 307, 311, 311, 312.0, 313, 313, 312, 312, 312, 311, 311, 309, 309.0, 309, 309, 309, 309, 308, 304.5, 301, 305, 304.6666666666667, 304.33333333333337, 304, 304, 304, 302, 302, 298, 301, 298, 299, 296, 300, 299, 298, 297, 296, 296, 295, 292, 294, 292, 291, 302, 307, 313, 315, 317, 314, 315, 313, 306, 307, 309, 309, 307, 310, 307.5, 305, 302, 289, 306, 306, 305, 304, 304, 302, 302, 301, 300, 302, 299, 298, 298, 296, 298, 295, 295, 292, 291, 292, 289, 289, 289.0, 289, 305, 313, 315, 315, 315, 314, 312.5, 311, 311, 310, 310, 309, 309, 309, 308, 308, 306, 305, 303, 303, 302, 301, 300, 299.0, 298, 301, 300, 299, 297.5, 296, 295, 292, 290, 290, 290.0, 290, 288, 288, 288, 287, 293, 298, 306, 312.0, 318, 315.0, 312, 312, 311, 311, 309, 308, 309, 307.5, 306, 309, 307, 305, 307, 306, 305, 305, 306, 305, 304, 304, 303.0, 302, 301, 300, 301, 300, 299, 296, 294, 294, 293.0, 292, 292, 291, 289, 289, 292, 293, 302, 317, 314.5, 312.0, 309.5, 307, 309, 302, 303.6666666666667, 305.33333333333337, 307, 296, 294.6666666666667, 293.33333333333337, 292, 304, 306, 306, 302, 303, 302, 302, 301, 301, 301, 299, 298, 295, 294, 295, 293, 293, 292, 293, 291, 292, 291, 288, 287, 288, 287, 294, 293, 303, 309, 314, 317, 298, 316, 315, 312, 312, 310, 309, 308.0, 307, 305, 305, 304, 302, 302, 302, 299, 300, 299, 298, 298.0, 298, 296, 294, 294, 293, 293, 289, 289, 286]
        input_list_dates = []

        smoothed_list = self.readDetection.smooth_list(input_list)
        for i in range(0,len(smoothed_list)):
            input_list_dates.append(i)
        self.assertEqual(len(input_list[0:len(smoothed_list)]),len(smoothed_list))

        #self.readDetection.show_plot(input_list_dates,input_list[0:len(smoothed_list)],smoothed_list)

    def test_smooth_list_2(self):
        input_list = [9,8,7,6,5,4,6,8,7,6,5,4,6,8,7,6,5,4,6,8,7,6,5,4]
        result = self.readDetection.smooth_list(input_list)

    def test_smooth_list_3(self):
        input_list = [-1, 58.833333333333336, 118.66666666666667, 178.5, 238.33333333333334, 298.1666666666667, 358, 357.0, 356, 355, 354, 356, 356, 356.0, 356, 354, 352, 352, 349, 355, 355, 355, 354.5, 354, 354, 353, 353, 353, 353, 353, 354, 353, 351, 345, 352, 351.0, 350.0, 349, 352, 352, 356, 353, 351, 351, 350, 352, 352, 350, 351, 352, 350, 351, 349, 352, 351, 349, 349.5, 350, 350, 349, 344, 348, 348, 351, 349, 350, 346, 348, 347.6666666666667, 347.33333333333337, 347, 348, 350, 348, 348, 347.6666666666667, 347.33333333333337, 347, 349, 348, 347.0, 346, 347, 347, 347, 348.0, 349, 349, 351, 350.5, 350, 349, 348, 348.5, 349, 350, 350, 350, 348.5, 347, 338.0, 329.0, 320, 492, 482.5, 473, 476, 475.0, 474.0, 473, 482, 474, 478, 475, 472, 474, 468, 475.0, 482, 466, 467, 478, 468, 467, 466, 463, 466, 470, 470, 459, 455.0, 451, 453, 468, 467, 470, 469, 476, 459, 475, 462, 461, 456, 466, 466, 464, 466, 463, 474, 456, 458, 464, 461, 463, 459, 458, 467, 452, 451, 451, 453, 447, 443, 451, 446, 444, 458, 459, 476.3333333333333, 493.66666666666663, 511, 502.6666666666667, 494.33333333333337, 486, 488, 489, 489, 488, 482, 479.5, 477, 481, 90, 481, 484, 484, 492, 484, 483, 484, 481, 484, 486, 480, 488, 489, 485, 488, 486.0, 484, 483.5, 483, 484.0, 485, 485, 486.5, 488, 483, 483, 492, 480, 484, 473.0, 462, 489, 478, 484, 478.6666666666667, 473.33333333333337, 468, 468, 468, 462, 457.5, 453, 374, 373.5, 373, 373.5, 374, 373.5, 373, 378.5, 384, 377, 354, 374, 378.5, 383, 378.5, 374, 383, 380.0, 377, 375, 371, 373.5, 376, 375, 374, 379, 377.5, 376, 370, 377, 374, 374, 375.0, 376, 376, 373, 370, 374, 367, 372, 372.5, 373.0, 373.5, 374, 376, 383, 391, 364, 365, 370.75, 376.5, 382.25, 388, 372, 369, 364, 368, 373, 373, 374, 370, 362, 362, 360, 366, 380, 381, 378, 376, 374, 375, 372, 372, 369, 363, 367, 366, 374.5, 383, 380, 377, 376, 374, 372, 370, 368, 362, 366, 376, 377, 375, 372, 371, 362, 364, 362, 361, 381, 294, 293, 298.5, 304.0, 309.5, 315.0, 320.5, 326, 321, 320.0, 319, 317.5, 316, 316.0, 316.0, 316.0, 316.0, 316.0, 316, 315.6666666666667, 315.33333333333337, 315.00000000000006, 314.66666666666674, 314.3333333333334, 314, 312, 324, 323.3333333333333, 322.66666666666663, 322, 321, 315.3333333333333, 309.66666666666663, 304, 304, 309.6, 315.20000000000005, 320.80000000000007, 326.4000000000001, 332, 324.5, 317, 332, 315, 315, 312, 310.0, 308, 306, 305.0, 304, 304.5, 305, 302, 303, 302.0, 301, 306.3333333333333, 311.66666666666663, 317, 317.0, 317, 315, 314, 310.0, 306, 307.5, 309, 303.6666666666667, 298.33333333333337, 293, 302, 308, 313, 311.5, 310.0, 308.5, 307.0, 305.5, 304, 301.8, 299.6, 297.40000000000003, 295.20000000000005, 293, 296.0, 299, 300, 306, 307, 307, 309, 301, 301, 319, 315, 313.3333333333333, 311.66666666666663, 310, 313.5, 317, 314.75, 312.5, 310.25, 308, 306.5, 305, 304, 302, 302, 301, 299, 300.0, 301, 297.75, 294.5, 291.25, 288, 291.0, 294.0, 297.0, 300, 299.3333333333333, 298.66666666666663, 298, 300, 300, 299, 299, 299, 298, 298.6, 299.20000000000005, 299.80000000000007, 300.4000000000001, 301, 283, 243, 236, 243, 244.5, 246, 250, 262.4, 274.79999999999995, 287.19999999999993, 299.5999999999999, 311.9999999999999, 324.39999999999986, 336.79999999999984, 349.1999999999998, 361.5999999999998, 374, 373.84615384615387, 373.69230769230774, 373.5384615384616, 373.3846153846155, 373.23076923076934, 373.0769230769232, 372.9230769230771, 372.76923076923094, 372.6153846153848, 372.4615384615387, 372.30769230769255, 372.1538461538464, 372, 366.8, 361.6, 356.40000000000003, 351.20000000000005, 346, 356.0, 366, 358.0, 350, 358.0, 366, 372, 367, 369.3333333333333, 371.66666666666663, 374, 362.0, 350, 354.75, 359.5, 364.25, 369, 368.75, 368.5, 368.25, 368.0, 367.75, 367.5, 367.25, 367.0, 366.75, 366.5, 366.25, 366, 365.375, 364.75, 364.125, 363.5, 362.875, 362.25, 361.625, 361, 362.0, 363, 361.9166666666667, 360.83333333333337, 359.75000000000006, 358.66666666666674, 357.5833333333334, 356.5000000000001, 355.4166666666668, 354.3333333333335, 353.25000000000017, 352.16666666666686, 351.08333333333354, 350, 354.4, 358.79999999999995, 363.19999999999993, 367.5999999999999, 372, 374.0, 376, 371.75, 367.5, 363.25, 359, 383, 361, 369.3333333333333, 377.66666666666663, 386, 378.0, 370, 369.1818181818182, 368.3636363636364, 367.54545454545456, 366.72727272727275, 365.90909090909093, 365.0909090909091, 364.2727272727273, 363.4545454545455, 362.6363636363637, 361.81818181818187, 361, 345.6666666666667, 330.33333333333337, 315, 312, 316, 311, 311, 312, 310, 313, 309, 310, 313, 311, 311, 312, 297, 282, 291, 285.0, 279.0, 273, 264, 257, 264, 323, 318, 318, 323, 324, 323, 325, 321, 319.6666666666667, 318.33333333333337, 317, 310.5, 304, 315, 310, 313, 311, 307.0, 303, 305, 311, 311, 313, 316, 317, 318, 316, 316, 315, 315, 314, 313, 312, 312, 311, 312, 311.0, 310.0, 309, 315, 314, 314, 313, 313.0, 313, 312, 311, 311, 311, 310, 311, 310, 309, 309, 314, 314, 312.0, 310, 315, 313, 314, 314, 313, 311.0, 309, 309, 310, 308, 308, 306, 306.0, 306, 311, 311, 288, 309, 309.5, 310, 309, 315.75, 322.5, 329.25, 336, 311, 308, 306.5, 305, 304, 310, 310, 310, 309, 307, 306, 304, 287, 280, 260.0, 240, 238, 223, 222, 228, 240, 283, 309.0, 335, 326, 317, 313, 310, 308, 306.75, 305.5, 304.25, 303, 311, 312, 310, 303, 305, 300, 295, 292.5, 290, 293, 300.0, 307, 304, 305, 305, 301.0, 297, 296, 298, 303, 309, 304, 306, 303.5, 301, 299, 295, 293, 295, 306, 302.3333333333333, 298.66666666666663, 295, 291, 296, 286, 298, 302, 300, 297.0, 294, 292, 292, 290.0, 288, 297, 296, 298, 302, 282.0, 262.0, 242, 239.0, 236.0, 233.0, 230, 228, 226.0, 224, 211.5, 199, 190.0, 181, 180.0, 179.0, 178, 176, 201.33333333333334, 226.66666666666669, 252.00000000000003, 277.33333333333337, 302.6666666666667, 328, 338, 335.6666666666667, 333.33333333333337, 331, 322.0, 313, 306, 303, 305, 303, 309, 309, 317, 316.0, 315, 313, 308, 305.5, 303, 299, 298, 299, 299, 304, 310, 312, 310, 311, 307.5, 304, 302, 299.5, 297, 298, 301.0, 304.0, 307, 308, 307, 305.6666666666667, 304.33333333333337, 303, 298, 294, 294, 308, 307, 305, 302, 300.0, 298.0, 296, 295.5, 295, 297.6666666666667, 300.33333333333337, 303, 302, 296.25, 290.5, 284.75, 279, 279.5, 280, 296, 293, 290, 284.0, 278, 293.85714285714283, 309.71428571428567, 325.5714285714285, 341.42857142857133, 357.28571428571416, 373.142857142857, 389, 380, 378.6666666666667, 377.33333333333337, 376, 376, 378, 379, 381, 378, 380, 384, 381, 382, 380, 380, 382, 385, 380, 367, 375.0, 383.0, 391, 385, 386, 379, 378, 379.0, 380, 387, 388, 381, 384, 385.0, 386, 385, 380, 379, 375, 375.3333333333333, 375.66666666666663, 376, 378, 382, 377, 377.5, 378, 377, 377, 374, 371, 377, 367, 378, 371.0, 364.0, 357, 375, 380, 376, 368, 382, 372.5, 363, 369.5, 376, 383.5, 391, 395, 396, 397, 396, 386.0, 376, 374, 410, 406, 400, 404, 404, 409.5, 415, 417, 414, 412, 410, 408, 401, 405, 404, 400, 399, 397, 394, 394, 391, 389, 387, 392, 397, 397, 398, 395.0, 392, 393, 391, 392, 392, 391, 391, 390, 389, 388, 387, 386, 386, 383, 387, 391, 398, 396, 395.0, 394, 393, 391, 392, 392, 391, 390, 384, 388, 388, 389, 387, 386, 386, 387, 386, 385, 385, 384, 384, 388, 390, 390, 388, 387.5, 387, 387, 386, 385, 385, 385, 385, 384, 383, 383, 383, 382, 382, 387, 386, 387, 388, 388.0, 388, 386, 385, 385, 383, 383, 380, 381, 383, 381, 379, 379, 377, 381, 389, 388, 388, 385, 385, 391, 391, 387, 385, 385, 384, 383, 381, 379, 378, 376, 374, 377, 382, 386, 385, 383, 381, 381, 383, 381, 379, 377, 376, 373, 372, 378.5, 385, 384.0, 383, 382, 380, 379, 378, 378, 376, 375, 373, 373, 377, 381, 381, 380.5, 380, 380, 380, 378, 379, 379, 379, 378, 378, 378, 375.0, 372]
        input_list_dates = []
        smoothed_list = self.readDetection.smooth_list(input_list)
        for i in range(0,len(smoothed_list)):
            input_list_dates.append(i)
        self.assertEqual(len(input_list[0:len(smoothed_list)]),len(smoothed_list))

        #self.readDetection.show_plot(input_list_dates,input_list[0:len(smoothed_list)],smoothed_list)

    def test_smooth_list_4(self):
        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        readDetection_2.set_window(3)
        print '------------'
        for i in range(0,5):
            print i
        print '------------'
        input_list = [353, 327.0, 301, 323.0, 345.0, 367, 376, 375, 365, 365, 366, 366, 369, 370.125, 371.25, 372.375, 373.5, 374.625, 375.75, 376.875, 378, 377, 373, 376, 373, 369.0, 365, 362.0, 359, 356, 363.0, 370.0, 377, 374, 372, 367.0, 362, 362, 357, 353, 352, 358.6666666666667, 365.33333333333337, 372, 368, 364, 359, 356, 354, 352, 346, 351.5, 357.0, 362.5, 368, 359, 355, 348, 348, 348, 377, 373, 367.0, 361, 358, 354, 349, 354.0, 359.0, 364, 361, 358, 351, 349, 347, 358.0, 369, 365, 360, 363, 368, 361, 360, 357, 361, 363, 361.0, 359, 355, 358, 365, 362.0, 359, 358, 355, 356.75, 358.5, 360.25, 362, 358, 355, 366, 366, 368, 363, 358, 356, 368, 371, 366, 358, 358, 363.0, 368, 364, 356, 355, 361.0, 367, 363.0, 359, 357, 362, 362]
        filtered_list = self.readDetection.filter_list(input_list)
        smoothed_list = self.readDetection.smooth_list(filtered_list)
        input_list_dates = []
        for i in range(0,len(smoothed_list)):
            input_list_dates.append(i)
        self.assertEqual(len(input_list[0:len(smoothed_list)]),len(smoothed_list))

        self.readDetection.show_plot(input_list_dates,input_list[0:len(smoothed_list)],smoothed_list,"test_smooth_list_4")

    def test_notify(self):
        readDetection_2 = Read_detection_tracking.ReadDetection('../../')
        input_list = [-1, 377, -1, 365, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 397, 405, 405, 399, 395, 391, 389, -1, 377, 375, 370, 371, -1, 388, 385, 382, 380, 379, 380, 387, 388, 386, 386, 384, 383, 382, 380, 377, 378, 375, 368, 370, 384, 387, 385, 384, 382, -1, 379, 377, 377, 371, 371, 373, 383, 388, 385, 382, 381, 379, 377, 376, 376, -1, 370, 372, 384, 387, 384, 380, 373, 372, 373, 371, 369, 369, 383, 382, 383, 385, 383, 378, 377, 374, 370, 367, 366, 383, 383, -1, 371, 374, 372, 372, 366, 370, 377, 383, 381, 379, 379, 377, 375, 373, 370, 366, 367, 365, 385, 383, 381, 379, 374, 374, 370, 367, 362, 363, -1, -1, 381, 379, 376, 375, 371, 369, 366, 367, 367, 367, 371, 376, 382, 386, 389, 385, 385, 384, 381, 380, 377, 376, 373, 370, 369, 369, 377, 382, 383, 383, 379, 376, 375, 373, 370, 368, 369, 370, 383, 385, 383, 378, 377, 374, 370, 368, 358, 364, 371, 384, 382, 379, 376, 372, 373, 370, 368, 366, 363, 359, 365, 376, 381, 381, 381, 377, 375, 374, 371, 371, 369, 368, 360, 365, 369, 382, 386, 382, 378, 378, 376, 374, -1, -1, 370, 371, 369, 368, 368, 363, 364, 364, 376, 381, 378, 379, 377, 376, 374, 373, 369, 370, 369, 368, 368, 365, 364, -1, 363, 372, 383, 381, 378, 376, 372, 373, 371, 371, 369, 365, 367, 363, 365, 366, 379, 378, 378, 375, 375, 372, 372, 371, 367, 364, 366, 366, 357, 375, 380, 378, 378, 375, 376, 374, 371, 369, 370, 372, 380, 384, 383, 379, 377, 378, 377, 374, 372, 371, 369, 368, 366, 364, 372, 381, 380, 377, 376, 374, 371, 369, 369, 367, 362, 368, 377, 378, 377, 376, 373, 371, 369, 369, 365, 366, 355, 368, 381, 381, 379, 377, 376, -1, 373, 371, 370, 365, 367, 374, 381, 378, -1, 373, 372, 370, 369, 367, 366, 361, 364, 371, 381, 381, 378, 377, 375, -1, 372, 370, 367, 365, 363, 364, 369, 381, 381, 379, 375, 373, 371, 370, 369, 367, 365, 363, -1, 379, 381, 378, 376, 374, 373, 371, 371, 369, 368, 367, 365, 363, 365, 377, 383, 383, 383, 380, 378, 375, 376, 375, 372, 371, 371, 368, 366, 360, 366, 380, 385, 383, 382, 379, 377, 376, 373, 371, 369, 369, 367, 364, 373, 383, 381, 377, 377, 375, 374, 373, 372, 369, 371, 370, 368, 367, 368, 360, 364, 376, 382, 380, 377, 374, 373, 370, 370, 370, 371, 369, 362, 364, 362, 358, 360, 374, 383, 380, 377, 374, 372, 369, 366, 368, 366, 359, -1, 363, 366, 374, 383, 378, 378, 376, 375, 373, 369, 367, -1, 367, 374, 383, 385, 382, 379, 375, 373, 372, 373, 370, 368, 366, 364, 361, -1, 383, 382, 381, 379, 377, 378, 373, 371, 370, 371, 368, 367, 366, 362, 357, 361, 364, 378, 383, 380, 378, 377, 376, 372, 370, 369, 368, 363, 365, 364, 370, 382, 382, 380, -1, 376, 373, 370, 368, 366, 360, 361, 368, 374, 381, 381, 377, 374, 371, 370, 368, 366, 363, 368, 370, 371, 369, 370, 373, 372]
        input_list_dates = []
        for i in range(0,len(input_list)):
            input_list_dates.append(str((i)))
        dataset = readDetection_2.analyse_list_for_reading_patterns(input_list,input_list_dates,"reading notify")
        print 'dataset notify'
        print dataset
        for i in range(0,len(input_list)):
            eye = [input_list[i],0]
            readDetection_2.notify(eye,input_list_dates[i])
        readDetection_2.notify_stopping_application()



if __name__ == '__main__':
    unittest.main()
