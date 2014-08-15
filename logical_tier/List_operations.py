import math
import numpy
def movingaverage(interval, window_size):
    window = numpy.ones(int(window_size))/float(window_size)
    #print str('window_size : ' + str(window_size))
    if interval == []:
        return []
    return numpy.convolve(interval, window, 'same')

# @input array
# @effect array filtered
# @return array
# This function will elliminate "-1" (noise) values. This will be done by averaging these values.
def filter_list(array):
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


def moving_median(array,window):
    result = []
    for i in range(0,len(array)):
        temp_array = []
        for j in range (i - window+1,i+1):
            if j >= 0:
                temp_array.append(array[j])
        temp_array.sort()
        if len(temp_array) ==0:
            median = array[i]
        if len(temp_array) == 1:
            median = temp_array[0]
        else:
            if len(temp_array) % 2.0 == 0:
                lowerbound = int(len(temp_array) / 2.0) - 1
                upperbound = int(len(temp_array) / 2.0)
                median = float(temp_array[lowerbound] + temp_array[upperbound]) / 2.0
            else:
                median = temp_array[int(len(temp_array) / 2.0)]

        result.append(median)
    return result

def moving_median_middle(array,window):
    result = []
    for i in range(0,len(array)):
        temp_array = []
        lowerbound_window = int(math.floor(float(window) / 2.0))
        upperbound_window = int(math.ceil(float(window) / 2.0))
        for j in range (i - lowerbound_window,i+upperbound_window):
            if j >= 0 and j < len(array):
                temp_array.append(array[j])
        temp_array.sort()
        if len(temp_array) == 0:
            median = array[i]
        if len(temp_array) == 1:
            median = temp_array[0]
        else:
            if len(temp_array) % 2.0 == 0:
                lowerbound = int(len(temp_array) / 2.0) - 1
                upperbound = int(len(temp_array) / 2.0)
                median = float(temp_array[lowerbound] + temp_array[upperbound]) / 2.0
            else:
                median = temp_array[int(len(temp_array) / 2.0)]

        result.append(median)
    return result

def calculate_average(list):
    return numpy.mean(list)

def calculate_std(list):
    return numpy.std(list)

def get_1D_list_from_2D_doubles_removed(list,index_column):
    result = []
    for item in list:
        if item[index_column] not in result:
            result.append(item[index_column])
    return result

def delete_entry(list,index):
    result = []
    for i in range(0,len(list)):
        if i != index:
            result.append(list[i])

    return result