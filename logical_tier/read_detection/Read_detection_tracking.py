import math

from matplotlib import pyplot as plt

from data_tier import DAReading_SQLite
from logical_tier import List_operations
class ReadDetection():
    x_coordinates_iris_array = []
    datetime_array = []


    treshold_length_array_x_coordinates_iris = 18000
    #treshold_length_array_x_coordinates_iris = 10

    median_window = 3
    treshold_read_samples_line = 3
    treshold_ratio_pos_neg_read_samples = 1.2

    threshold_readLines_positive = 2
    threshold_readLines_negative = 2
    threshold_from_neg_to_pos = 2

    threshold_window_selection = -1
    threshold_second_derivative = 1.0

    # nodig om na te gaan wat het verschil is in ooglocatie als de lezer 1 regel gelezen heeft.
    # Deze treshold geeft de minimale afstand aan. Dit is nodig om te voorkomen dat als de gebruiker gewoon staart naar 1 punt, dit niet gedetecteerd wordt.
    threshold_derivative = 5.0
    threshold_amound_derivative_avg = 30

    # tresholds for window selection
    threshold_window_selection_total_pos = 2.0
    threshold_window_selection_relative_marge_difference_amount_pos = 0.5
    threshold_scale_factor_teller_pos_for_window = 1.2
    threshold_window_accept_pos = 1.0

    #read detection 2
    threshold_check_reading = 100
    threshold_switch_to_read = (threshold_check_reading * (treshold_ratio_pos_neg_read_samples - 1)) * (-1)

    dareading = None
    def __init__(self,link_to_main):
        self.dareading = DAReading_SQLite.DAReading(link_to_main)

    def set_window(self,window):
        self.threshold_window_selection = window

    def set_tresholds(self, treshold_from_neg_to_pos, treshold_length_array_x_coordinates_iris,
                      treshold_ratio_pos_neg_read_samples, treshold_readLines_negative, treshold_readLines_positive,
                      treshold_read_samples_line, treshold_second_derivative, treshold_window_selection,
                      treshold_window_selection_relative_marge_difference_amount_pos,
                      treshold_window_selection_total_pos):

        self.treshold_length_array_x_coordinates_iris = treshold_length_array_x_coordinates_iris
        self.treshold_read_samples_line = treshold_read_samples_line
        self.treshold_ratio_pos_neg_read_samples = treshold_ratio_pos_neg_read_samples
        self.threshold_readLines_positive = treshold_readLines_positive
        self.threshold_readLines_negative = treshold_readLines_negative
        self.threshold_from_neg_to_pos = treshold_from_neg_to_pos
        self.threshold_window_selection = treshold_window_selection
        self.threshold_second_derivative = treshold_second_derivative
        self.threshold_window_selection_total_pos = treshold_window_selection_total_pos
        self.threshold_window_selection_relative_marge_difference_amount_pos = treshold_window_selection_relative_marge_difference_amount_pos


    def notify(self,eye,datetime_detection):
        if eye is not None:
            self.x_coordinates_iris_array.append(eye[0])
        else:
             self.x_coordinates_iris_array.append(-1)
        self.datetime_array.append(datetime_detection)
        if len(self.x_coordinates_iris_array) >= self.treshold_length_array_x_coordinates_iris:
            self.flush_data()

    def flush_data(self):
        self.analyse_list_for_reading_patterns_2(self.x_coordinates_iris_array,self.datetime_array,'')
        self.x_coordinates_iris_array = []
        self.datetime_array = []

    def eye_switched(self):
        self.flush_data()

    def notify_stopping_application(self):
        self.flush_data()

    # @param raw list x coordinates iris
    def analyse_list_for_reading_patterns(self,x_coordinates_iris,datetime_array,title):
        filtered_list = self.filter_list(x_coordinates_iris)
        #filtered_list = list_operations.moving_median(filtered_list,self.median_window)

        if self.threshold_window_selection == -1:
            smoothened_list = self.smooth_list(filtered_list)
        else:
            smoothened_list = List_operations.movingaverage(filtered_list,self.threshold_window_selection)

        dataset = self.analyse_list_for_reading_patterns_smooth_list(smoothened_list,datetime_array)

        try:
            self.show_plot(datetime_array,filtered_list,smoothened_list,title)
        except Exception, e:
            print str(e)

        for item in dataset:
            self.dareading.insert_row_reading(item[0],item[1],item[2],item[3])
        return dataset


        # @param raw list x coordinates iris
    def analyse_list_for_reading_patterns_2(self,x_coordinates_iris,datetime_array,title):
        filtered_list = self.filter_list(x_coordinates_iris)
        #filtered_list = list_operations.moving_median(filtered_list,self.median_window)

        if self.threshold_window_selection == -1:
            smoothened_list = self.smooth_list(filtered_list)
        else:
            smoothened_list = List_operations.movingaverage(filtered_list,self.threshold_window_selection)

        dataset = self.analyse_list_for_reading_patterns_smooth_list_2(smoothened_list,datetime_array)
        """
        try:
            self.show_plot(datetime_array,filtered_list,smoothened_list,title)
        except Exception, e:
            print str(e)
        """
        for item in dataset:
            self.dareading.insert_row_reading(item[0],item[1],item[2],item[3])
        return dataset

    def analyse_list_for_reading_patterns_smooth_list_2(self,x_coordinates_iris_smooth,datetime_array):
        dataset = []
        derivative_list = self.calculate_derivative(x_coordinates_iris_smooth)
        read_detector = 0
        reading = False
        mode_switched = False
        datetime_from = None
        datetime_to = None
        list_acc = 0
        for i in range(0,len(derivative_list)):
            if derivative_list[i] > 0:
                read_detector += 1
            else:
                read_detector -= 1

            list_acc += 1
            if list_acc >= self.threshold_check_reading:
                if reading == False and read_detector <= self.threshold_switch_to_read:
                    reading = True
                    mode_switched = True
                else:
                    if reading == True and read_detector > self.threshold_switch_to_read:
                        reading = False
                        mode_switched = True
                        datetime_to = datetime_array[i]

                if mode_switched is True:
                    if reading is True:
                        datetime_from = datetime_array[i]
                    else:
                        dataset.append([datetime_from,datetime_to,True,''])
                    mode_switched = False
                list_acc = 0
                read_detector = 0

        if reading is True:
            datetime_to = datetime_array[len(datetime_array) - 1]
            dataset.append([datetime_from,datetime_to,True,''])

        return dataset


    def analyse_list_for_reading_patterns_smooth_list(self,x_coordinates_iris_smooth,datetime_array):
        dataset = []
        derivative_list = self.calculate_derivative(x_coordinates_iris_smooth)
        second_derivative_list = self.calculate_derivative(derivative_list)
        index = 0
        teller_pos = 0.0
        teller_neg = 0.0
        #teller_from_neg_to_pos = 0.0
        teller_ratio_not_in_bounds = 0.0
        teller_ratio_in_bounds = 0.0

        teller_second_derivative = 0.0
        teller_total_second_derivative = 0.0

        teller_derivative = 0.0
        teller_total_derivative = 0.0

        reading = False
        datetime_from = None
        datetime_to = None
        while index < len(derivative_list) and index < len(datetime_array):

            # derivative > 0, eyes moving from left to right
            if datetime_from == None:
                datetime_from = datetime_array[index]
            if index == 150:
                True

            if derivative_list[index] > 0:
                teller_pos += 1.0
                """
                if teller_from_neg_to_pos == 1:
                    teller_pos += 2
                else:
                    if teller_from_neg_to_pos > 1:
                        teller_pos += 1.0
                teller_from_neg_to_pos += 1
                """
            else:
                # derivative
                teller_derivative += derivative_list[index]

                #second derivative
                teller_second_derivative += second_derivative_list[index]
                teller_total_second_derivative += 1.0
                teller_from_neg_to_pos = 0
                if index > 0:
                    if derivative_list[index - 1] > 0 and teller_pos > 0 and teller_neg > 0:
                        avg_second_derivative = teller_second_derivative / teller_total_second_derivative

                        ratio_temp = teller_neg / teller_pos
                        if(ratio_temp) >= self.treshold_ratio_pos_neg_read_samples \
                            and abs(avg_second_derivative) <= self.threshold_second_derivative \
                            and (-1) * teller_derivative >= self.threshold_derivative:

                            teller_ratio_not_in_bounds = 0.0
                            teller_ratio_in_bounds += 1.0
                            if teller_ratio_in_bounds >= self.threshold_readLines_positive:
                                datetime_to = None

                        else:
                            teller_ratio_not_in_bounds += 1.0
                            teller_ratio_in_bounds = 0.0
                            if reading == False:
                                datetime_from = None
                            if datetime_to is None:
                                datetime_to = datetime_array[index]


                        teller_pos = 0.0
                        teller_neg = 0.0

                        teller_derivative = 0.0

                        teller_second_derivative = 0.0
                        teller_total_second_derivative = 0.0

                teller_neg += 1.0

            if (reading == False):
                if teller_ratio_in_bounds >= self.threshold_readLines_positive:
                    reading = True
                    #teller_derivative = 0.0
                    #teller_total_derivative = 0.0
            else:
                if (teller_ratio_not_in_bounds > self.threshold_readLines_negative):
                    reading = False
                    dataset.append([datetime_from,datetime_to,True,''])
                    datetime_from = None
                    datetime_to = None
            index += 1

        # If after the while loop, "reading" was True, then add this to the dataset as well
        if reading == True:
            datetime_to = datetime_array[len(datetime_array) - 1]
            dataset.append([datetime_from,datetime_to,True,''])

        return dataset


    def calculate_derivative(self,array_y):
        result = []
        result.append(0)
        index = 0
        while index < len(array_y)-1:
            previous_value = array_y[index]
            index += 1
            result.append(array_y[index] - previous_value)
        return result

    # @input array
    # @effect array filtered
    # @return array
    # This function will elliminate "-1" (noise) values. This will be done by averaging these values.
    def filter_list(self,array):
        index = 0
        result = []
        while index < len(array):
            if array[index] != -1:
                result.append(array[index])
                index += 1
            else:
                index_temp = index
                if index > 0:
                    previous_value = array[index - 1]
                    next_value = -1
                    while index_temp < len(array) and next_value == -1:
                        if array[index_temp] == -1:
                            index_temp += 1
                        else:
                            next_value = array[index_temp]
                    if next_value != -1:
                        difference_index = float(index_temp - (index - 1))
                        difference_value = float(next_value - previous_value)
                        incrementer = float(difference_value / difference_index)

                        while index < index_temp:
                            result.append(float(result[len(result)-1]) + incrementer)
                            index += 1
                    else:
                        result.append(next_value)
                        index += 1
                else:
                    result.append(array[index])
                    index += 1
        return result


    def smooth_list(self,list):
        derivative_list = self.calculate_derivative(list)
        list_copy = []
        for item in list:
            list_copy.append(item)
        index = 0
        teller_pos = 0
        teller_pos_acc = 0.0
        teller_pos_total = 0.0
        current_window = 0.0
        start_index = 0
        result = []
        while index < len(list):

            if derivative_list[index] > 0:
                teller_pos += 1
            else:
                if teller_pos > 0:
                    if teller_pos < self.threshold_window_accept_pos:
                        teller_pos = 0
                    else:
                        teller_pos_acc += teller_pos
                        teller_pos_total += 1
                        teller_pos = 0
                        # Eerst gemiddelde van teller_pos nemen over enkele momenten dat de functie stijgt, weer daalt en weer stijgt.
                        # Dan gebaseerd daarop nieuw window berekenen door die avg_pos te vermenigvuldigen met percentage
                        # Dan kijken of het new_window binnen de marges van verschil liggen tov oud window
                        # Zo niet, lijst meegeven aan movingaverage tot deze index met oud window, dan oud window op new window zetten en alles resetten.
                        if teller_pos_total > self.threshold_window_selection_total_pos:
                            avg_pos = teller_pos_acc / teller_pos_total
                            new_window = math.ceil(float(avg_pos * self.threshold_scale_factor_teller_pos_for_window))

                            if new_window > 0:
                                if current_window == 0: # and new_window != 0
                                    current_window = new_window
                                if (float(abs(current_window - new_window))/float(current_window)) > self.threshold_window_selection_relative_marge_difference_amount_pos: #(new_window > 0) and
                                    if start_index - current_window >= 0:
                                        start_index_with_current_window_marge = int(start_index - current_window)
                                    else:
                                        start_index_with_current_window_marge = start_index
                                    temp_smoothed_list = List_operations.movingaverage(list[start_index_with_current_window_marge:index],int(current_window))

                                    # het resultaat van movingaverage gaat op het einde steeds dalend zijn omdat, als er minder items over zijn dan de size van de window, gaat het movingaverage foutief berekent worden. Om dit tegen te gaan worden den laatste elementen van subarray eraf geknipt
                                    for index_restore in range(0,index):
                                        list[index_restore] = list_copy[index_restore]
                                    if(index - current_window) > 0:
                                        end_index = int(index - current_window)
                                    else:
                                        end_index = index
                                    if(len(temp_smoothed_list) - current_window ) > 0:
                                        end_index_smooth = int(len(temp_smoothed_list)  - current_window)
                                    else:
                                        end_index_smooth = len(temp_smoothed_list)

                                    if start_index >= (1 * current_window) and current_window < end_index_smooth:
                                        start_index_smooth_temp = int(current_window)
                                    else:
                                        start_index_smooth_temp = 0

                                    for index_temp_list in range(start_index_smooth_temp,end_index_smooth):
                                        result.append(temp_smoothed_list[index_temp_list])
                                        if (len(result) >= 337):
                                            True
                                    current_window = new_window
                                    start_index = len(result)

                            teller_pos = 0
                            teller_pos_total = 0.0
                            teller_pos_acc = 0.0
            index += 1

        if start_index < len(list) and current_window > 0:
            temp_smoothed_list = List_operations.movingaverage(list[int(start_index - current_window):len(list)],current_window)
            for index in range(int(current_window),len(temp_smoothed_list)):
                result.append(temp_smoothed_list[index])
        return result


    def show_plot(self,x,eye_x,eye_x_smooth,title):
        # plot

        fig_left_eye = plt.figure(title)
        subplot = 111
        graph = fig_left_eye.add_subplot(subplot)
        graph.plot(x,eye_x,'r-o')
        graph.plot(x,eye_x_smooth,'g-o')

        plt.show()
        #filename = type + '.png'
        #plt.savefig(filename)

      #  graph.savefig("test-graph")

