import datetime

from matplotlib.dates import date2num
import numpy as np

from data_tier import DAMindwave_SQLite
from data_tier import DAUserGone_SQLite
from logical_tier.userfeedback import Userfeedback_processing
from logical_tier import List_operations
import Mindwave_enumeration
from exception import Exception


window_median = 5
treshold_poorSignalMindwave = 0
def get_list_interval_mindwave_data(list_mindwave_data, start_index,start_date, end_date):
    result = []

    for i in range(start_index,len(list_mindwave_data)):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[i][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[i][1], "%Y-%m-%d %H:%M:%S")

        if start_date <= datetime_from_mindwave:
            if end_date >= datetime_from_mindwave:
                result.append(list_mindwave_data[i])
            else:
                return result,i
    return result,(len(list_mindwave_data)-1)

"""
@param list_mindwave_data | array of different lists with data from mindwave (for example [attention_list, meditation_list]
@param list_dates | one list with the dates of each corresponding sample in each list in list_mindwave_data
@param start_index | usefull to spare computation time if you know upfront the lowerbound
@param start_date | the lowerbound of the list
@param end_date | the upperbound of the list

@precondition for each list in list_mindwave_data: len(list) == len(list_dates)

@return average sample of each list within the period start_date and end_date
@return end_index: the index of the last element in list_dates
"""
def get_average_sample_interval(list_mindwave_data,start_index,start_date,end_date):
    sublist,end_index = get_list_interval_mindwave_data(list_mindwave_data,start_index,start_date,end_date)
    total = 0.0
    attention_acc = 0.0
    meditation_acc = 0.0
    for index_sublist in range(0,len(sublist)):
        attention_acc += sublist[index_sublist][3]
        meditation_acc += sublist[index_sublist][4]
        total += 1.0
    if total > 0:
        attention_avg = attention_acc / total
        meditation_avg = meditation_acc / total
    else:
        raise Exception.ListEmpty("no mindwave data for this interval")
    datetime_start_mindwave = sublist[0][1]
    datetime_end_mindwave = sublist[len(sublist) - 1][1]
    return attention_avg,meditation_avg,end_index,datetime_start_mindwave,datetime_end_mindwave

def convert_mindwave_data_to_RescueTime_intervals(list_mindwave_data,list_dates_RescueTime):
    attention_data = []
    meditation_data = []
    x_axis = []
    start_index = 0

    for i_res in range(0,len(list_dates_RescueTime)):
        datetime_interval_from = datetime.datetime.strptime(list_dates_RescueTime[i_res][0], "%Y-%m-%d %H:%M:%S")
        datetime_interval_to =  datetime_interval_from + datetime.timedelta(seconds=300)
        try:
            attention_avg,meditation_avg,end_index,datetime_start_mindwave,datetime_end_mindwave = get_average_sample_interval(list_mindwave_data,start_index,datetime_interval_from,datetime_interval_to)

            try:
                datetime_start_mindwave_converted = datetime.datetime.strptime(datetime_start_mindwave, "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_start_mindwave_converted = datetime.datetime.strptime(datetime_start_mindwave, "%Y-%m-%d %H:%M:%S")

            try:
                datetime_end_mindwave_converted = datetime.datetime.strptime(datetime_end_mindwave, "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_end_mindwave_converted = datetime.datetime.strptime(datetime_end_mindwave, "%Y-%m-%d %H:%M:%S")

            x_axis.append([datetime_start_mindwave_converted,datetime_end_mindwave_converted])
            attention_data.append(attention_avg)
            meditation_data.append(meditation_avg)

            start_index = end_index
        except Exception.ListEmpty, e:
            pass
    return x_axis,attention_data,meditation_data

def convert_mindwave_data_to_manualLog_intervals(list_mindwave_data,list_manualLog):
    attention_data = []
    meditation_data = []
    x_axis = []
    start_index = 0

    for i_res in range(0,len(list_manualLog)):
        datetime_interval_from = list_manualLog[i_res][0]
        datetime_interval_to = list_manualLog[i_res][1]
        try:
            attention_avg,meditation_avg,end_index,datetime_start_mindwave,datetime_end_mindwave = get_average_sample_interval(list_mindwave_data,start_index,datetime_interval_from,datetime_interval_to)
            try:
                datetime_start_mindwave_converted = datetime.datetime.strptime(datetime_start_mindwave, "%Y-%m-%d %H:%M:%S")
            except:
                datetime_start_mindwave_converted = datetime.datetime.strptime(datetime_start_mindwave, "%Y-%m-%d %H:%M:%S.%f")

            try:
                datetime_end_mindwave_converted = datetime.datetime.strptime(datetime_end_mindwave, "%Y-%m-%d %H:%M:%S")
            except:
                datetime_end_mindwave_converted = datetime.datetime.strptime(datetime_end_mindwave, "%Y-%m-%d %H:%M:%S.%f")

            x_axis.append([datetime_start_mindwave_converted,datetime_end_mindwave_converted])
            attention_data.append(attention_avg)
            meditation_data.append(meditation_avg)

            start_index = end_index
        except Exception.ListEmpty, e:
            pass
    return x_axis,attention_data,meditation_data

def get_mindwave_data_filtered_smoothed( datetime_from, datetime_to,window_moving_average):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    mindwave_data_result = []
    list_dates = []
    attention_data = []
    meditation_data = []
    x = []
    index = 0
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")
        list_dates.append([datetime_from_mindwave,datetime_to_mindwave])

        if list_mindwave_data[index][5] == treshold_poorSignalMindwave:
            attention_data.append(list_mindwave_data[index][3])
            meditation_data.append(list_mindwave_data[index][4])
        else:
            attention_data.append(-1)
            meditation_data.append(-1)

        index += 1

    attention_data = List_operations.filter_list(attention_data)
    meditation_data = List_operations.filter_list(meditation_data)

    attention_data = List_operations.moving_median(attention_data,window_median)
    meditation_data = List_operations.moving_median(meditation_data,window_median)

    attention_data = List_operations.movingaverage(attention_data, window_moving_average)
    meditation_data = List_operations.movingaverage(meditation_data, window_moving_average)

    for i in range(0,len(attention_data)):
        mindwave_data_result.append([list_dates[i][0],list_dates[i][1],attention_data[i],meditation_data[i]])

    return mindwave_data_result

def get_mindwave_data_filtered_smoothed_middle_moving_median( datetime_from, datetime_to,window_moving_average):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    mindwave_data_result = []
    list_dates = []
    attention_data = []
    meditation_data = []
    x = []
    index = 0
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")
        list_dates.append([datetime_from_mindwave,datetime_to_mindwave])

        if list_mindwave_data[index][5] == treshold_poorSignalMindwave:
            attention_data.append(list_mindwave_data[index][3])
            meditation_data.append(list_mindwave_data[index][4])
        else:
            attention_data.append(-1)
            meditation_data.append(-1)

        index += 1

    attention_data = List_operations.filter_list(attention_data)
    meditation_data = List_operations.filter_list(meditation_data)

    attention_data = List_operations.moving_median_middle(attention_data,window_median)
    meditation_data = List_operations.moving_median_middle(meditation_data,window_median)

    attention_data = List_operations.movingaverage(attention_data, window_moving_average)
    meditation_data = List_operations.movingaverage(meditation_data, window_moving_average)

    for i in range(0,len(attention_data)):
        mindwave_data_result.append([list_dates[i][0],list_dates[i][1],attention_data[i],meditation_data[i]])

    return mindwave_data_result


def get_attention_meditation_buckets(datetime_from, datetime_to, mindwave_data_list):
    # [strongly lowered, reduced, neutral, slightly elevated, elevated]

    attention_bucket = []
    meditation_bucket = []
    total = 0.0
    amount_buckets = 5

    for i in range(0,amount_buckets):
        attention_bucket.append(0.0)
        meditation_bucket.append(0.0)

    for i in range (0,len(mindwave_data_list)):

        if mindwave_data_list[i][0] >= datetime_from and mindwave_data_list[i][1] < datetime_to:
            id_attention = classify_percentage(mindwave_data_list[i][2])
            id_meditation = classify_percentage(mindwave_data_list[i][3])

            attention_bucket[id_attention] += 1.0
            meditation_bucket[id_meditation] += 1.0
            total += 1.0

    for i in range(0,amount_buckets):
        attention_bucket[i] = float(attention_bucket[i] / total)
        meditation_bucket[i] = float(meditation_bucket[i] / total)
    return attention_bucket, meditation_bucket




def classify_percentage(percentage):
    if percentage >= 0 and percentage < 0.20:
        return Mindwave_enumeration.STRONGLY_LOWERED
    if percentage >= 0.20 and percentage < 0.40:
        return Mindwave_enumeration.REDUCED
    if percentage >= 0.40 and percentage < 0.60:
        return Mindwave_enumeration.NEUTRAL
    if percentage >= 0.60 and percentage < 0.80:
        return Mindwave_enumeration.SLIGHTLY_ELEVATED
    #if percentage >= 0.80 and percentage <= 1.0:
    if percentage >= 0.80:
        return Mindwave_enumeration.ELEVATED
#    raise exception.UnknownID("The mindwave classification ID is unknown")


def merge_buckets(attention_bucket_array, meditation_bucket_array):
    attention_bucket_result = []
    meditation_bucket_result = []
    total = 0.0

    #initialise buckets
    amount_buckets = 5
    for i in range(0,amount_buckets):
        attention_bucket_result.append(0.0)
        meditation_bucket_result.append(0.0)

    for i in range(0,len(attention_bucket_array)):
        for a in range(0,amount_buckets):
            attention_bucket_result[a] += attention_bucket_array[i][a]
            meditation_bucket_result[a] += meditation_bucket_array[i][a]
        total += 1.0

    for a in range(0,amount_buckets):
        attention_bucket_result[a] = float(attention_bucket_result[a] / total)
        meditation_bucket_result[a] = float(meditation_bucket_result[a] / total)

    return attention_bucket_result, meditation_bucket_result

def get_sublist(mindwave_data,datetime_from, datetime_to):
    index_from = -1
    index_to = -1
    for i in range(0,len(mindwave_data)):
        if mindwave_data[i][0] >= datetime_from and index_from == -1:
            index_from = i
        else:
            if mindwave_data[i][1] <= datetime_to and index_from != -1:
                index_to = i

    if datetime_from == -1 or datetime_to == -1:
        raise Exception.ListEmpty("datetime_from or datetime_to is outside the range of the mindwave data")
    return mindwave_data[index_from : index_to+1]

def calculate_avg_attention_meditation(mindwave_data):
    attention_avg = 0.0
    meditation_avg = 0.0
    total = 0.0
    for item in mindwave_data:
        attention_avg += item[2]
        meditation_avg += item[3]
        total += 1.0
    if total > 0:
        attention_avg = float(round(attention_avg / total,2))
        meditation_avg = float(round(meditation_avg / total,2))

    return  attention_avg, meditation_avg

def calculate_std_attention_meditation(mindwave_data):
    attention_list = []
    meditation_list = []

    if len(mindwave_data) == 0:
        #raise ZeroDivisionError("mindwave_data has no items")
        return 0.0,0.0
    for item in mindwave_data:
        attention_list.append(item[2])
        meditation_list.append(item[3])
    attention_std = np.std(attention_list)
    meditation_std = np.std(meditation_list)

    return attention_std, meditation_std

"""
def get_mindwave_dataa_important_unimportant_activity(daRescueTime,treshold_time_sec, datetime_from, datetime_to,window):
    dates = daRescueTime.get_dates(datetime_from,datetime_to)
    important_activities = []
    unimportant_activities = []
    for item in dates:
        datetime_rescueTime_from = datetime.datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S")
        datetime_rescueTime_to = datetime_rescueTime_from + datetime.timedelta(minutes=5)
        activities = daRescueTime.get_data_specific_period(datetime_rescueTime_from,datetime_rescueTime_to)
        sum_time_spent = 0
        for activity in activities:
            if activity[6] == 0:
                sum_time_spent += activity[2]
        if sum_time_spent >= treshold_time_sec:
            unimportant_activities.append([datetime_rescueTime_from,datetime_rescueTime_to])
        else:
            important_activities.append([datetime_rescueTime_from,datetime_rescueTime_to])


    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []
    userNotStudying = []
    userStudying = []
    x = []
    index = 0
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except :
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")


        if list_mindwave_data[index][5] == self.treshold_poorSignalMindwave:
            attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
            meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
        else:
            attention_data.append((datetime_from_mindwave,-1))
            meditation_data.append((datetime_from_mindwave,-1))

        canAddNotStudyingEntry = False
        canAddStudyingEntry = False
        for i in range(0,len(unimportant_activities)):
            datetime_from_unimportant = unimportant_activities[i][0]
            datetime_to_unimportant = unimportant_activities[i][1]

            if datetime_from_mindwave >= datetime_from_unimportant and datetime_to_mindwave <= datetime_to_unimportant:
                canAddNotStudyingEntry = True

        for i in range(0,len(important_activities)):
            datetime_from_important = important_activities[i][0]
            datetime_to_important = important_activities[i][1]

            if datetime_from_mindwave >= datetime_from_important and datetime_to_mindwave <= datetime_to_important:
                canAddStudyingEntry = True

        if canAddNotStudyingEntry is True:
            userNotStudying.append((datetime_from_mindwave,1))
        else:
            userNotStudying.append((datetime_from_mindwave,0))

        if canAddStudyingEntry is True:
            userStudying.append((datetime_from_mindwave,0.9))
        else:
            userStudying.append((datetime_from_mindwave,0))

        index += 1
    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]


    print "--------------------------------"
    print "original"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    y_attention = list_operations.filter_list(y_attention)
    y_meditation = list_operations.filter_list(y_meditation)

    print "after filter_list"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = list_operations.moving_median(y_attention,window_median)
    y_meditation = list_operations.moving_median(y_meditation,window_median)

    print "after moving_median"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = list_operations.movingaverage(y_attention, window)
    y_meditation = list_operations.movingaverage(y_meditation, window)

    print "after movingaverage"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    print "---------------------------"

    y_userGoneNotStudying = list_operations.filter_list([value for (date, value) in userNotStudying])
    y_userGoneStudying = list_operations.filter_list([value for (date, value) in userStudying])

    return attention_data, x, y_attention, y_meditation,y_userGoneNotStudying,y_userGoneStudying
"""
def get_mindwave_data_raw( datetime_from, datetime_to):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []

    x = []
    index = 0
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")

        attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
        meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))

        index += 1
    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]


    return attention_data, x, y_attention, y_meditation

def get_mindwave_data( datetime_from, datetime_to,window):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []

    x = []
    index = 0
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")

        attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
        meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))

        index += 1
    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]

    print "--------------------------------"
    print "original"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    y_attention = List_operations.filter_list(y_attention)
    y_meditation = List_operations.filter_list(y_meditation)

    print "after filter_list"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.moving_median(y_attention,window_median)
    y_meditation = List_operations.moving_median(y_meditation,window_median)

    print "after moving_median"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.movingaverage(y_attention, window)
    y_meditation = List_operations.movingaverage(y_meditation, window)

    print "after movingaverage"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    print "---------------------------"

    return attention_data, x, y_attention, y_meditation

def get_mindwave_userfeedback_data( datetime_from, datetime_to,window):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []
    userfeedback_data = []
    x = []
    index = 0
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except :
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")

        if list_mindwave_data[index][5] == treshold_poorSignalMindwave:
            attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
            meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
        else:
            attention_data.append((datetime_from_mindwave,-1))
            meditation_data.append((datetime_from_mindwave,-1))

        try:
            avg_userfeedback = Userfeedback_processing.get_average_userfeedback_specific_period(datetime_from_mindwave,datetime_to_mindwave)
        except Exception.ListEmpty:
            avg_userfeedback = -1
        userfeedback_data.append((datetime_from_mindwave,avg_userfeedback))
        #meditation_data.append((list_mindwave_data[index][1], list_mindwave_data[index][4]))
        index += 1

    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]

    print "--------------------------------"
    print "original"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    y_attention = List_operations.filter_list(y_attention)
    y_meditation = List_operations.filter_list(y_meditation)

    print "after filter_list"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.moving_median(y_attention,window_median)
    y_meditation = List_operations.moving_median(y_meditation,window_median)

    print "after moving_median"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.movingaverage(y_attention, window)
    y_meditation = List_operations.movingaverage(y_meditation, window)

    print "after movingaverage"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    print "---------------------------"

    y_userfeedback = List_operations.filter_list([value for (date, value) in userfeedback_data])

    return attention_data, x, y_attention, y_meditation,y_userfeedback

def get_mindwave_activity_data( datetime_from, datetime_to,activity_details,window):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []
    activityDuration_data = []
    x = []
    index = 0

    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except :
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")

        if list_mindwave_data[index][5] == treshold_poorSignalMindwave:
            attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
            meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
        else:
            attention_data.append((datetime_from_mindwave,-1))
            meditation_data.append((datetime_from_mindwave,-1))

        added = False
        for activityDetail in activity_details:
            start_datetime_RescueTime = datetime.datetime.strptime(activityDetail[0], "%Y-%m-%d %H:%M:%S")
            end_datetime_rescueTime = start_datetime_RescueTime + datetime.timedelta(minutes=5)

            if datetime_from_mindwave >=start_datetime_RescueTime and datetime_to_mindwave <= end_datetime_rescueTime and added is False:
                activityDuration_data.append((datetime_from_mindwave,float((activityDetail[1]) / 300.0)))
                added = True
        if added is False:
            activityDuration_data.append((datetime_from_mindwave,-1))




        index += 1

    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]

    print "--------------------------------"
    print "original"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    y_attention = List_operations.filter_list(y_attention)
    y_meditation = List_operations.filter_list(y_meditation)

    print "after filter_list"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.moving_median(y_attention,window_median)
    y_meditation = List_operations.moving_median(y_meditation,window_median)

    print "after moving_median"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.movingaverage(y_attention, window)
    y_meditation = List_operations.movingaverage(y_meditation, window)

    print "after movingaverage"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    print "---------------------------"

    y_activityDuration = List_operations.filter_list([value for (date, value) in activityDuration_data])

    return attention_data, x, y_attention, y_meditation,y_activityDuration


def get_mindwave_userGone_data(datetime_from, datetime_to,window):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []
    userGoneNotStudying = []
    userGoneStudying = []
    x = []
    index = 0
    listUserGone = DAUserGone_SQLite.get_data_specific_period(datetime_from,datetime_to)
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except :
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")


        if list_mindwave_data[index][5] == treshold_poorSignalMindwave:
            attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
            meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
        else:
            attention_data.append((datetime_from_mindwave,-1))
            meditation_data.append((datetime_from_mindwave,-1))

        canAddUserGoneNotStudyingEntry = False
        canAddUserGoneStudyingEntry = False
        for item in listUserGone:
            try:
                datetime_from_userGone = datetime.datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_from_userGone = datetime.datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S")

            try:
                datetime_to_userGone = datetime.datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_to_userGone = datetime.datetime.strptime(item[2], "%Y-%m-%d %H:%M:%S")

            if datetime_from_mindwave >= datetime_from_userGone and datetime_to_mindwave <= datetime_to_userGone and item[5] == 0:
                canAddUserGoneNotStudyingEntry = True

            if datetime_from_mindwave >= datetime_from_userGone and datetime_to_mindwave <= datetime_to_userGone and item[5] == 1:
                canAddUserGoneStudyingEntry = True
        if canAddUserGoneNotStudyingEntry is True:
            userGoneNotStudying.append((datetime_from_mindwave,1))
        else:
            userGoneNotStudying.append((datetime_from_mindwave,0))

        if canAddUserGoneStudyingEntry is True:
            userGoneStudying.append((datetime_from_mindwave,1))
        else:
            userGoneStudying.append((datetime_from_mindwave,0))

        index += 1
    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]


    print "--------------------------------"
    print "original"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    y_attention = List_operations.filter_list(y_attention)
    y_meditation = List_operations.filter_list(y_meditation)

    print "after filter_list"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.moving_median(y_attention,window_median)
    y_meditation = List_operations.moving_median(y_meditation,window_median)

    print "after moving_median"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.movingaverage(y_attention, window)
    y_meditation = List_operations.movingaverage(y_meditation, window)

    print "after movingaverage"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    print "---------------------------"

    y_userGoneNotStudying = List_operations.filter_list([value for (date, value) in userGoneNotStudying])
    y_userGoneStudying = List_operations.filter_list([value for (date, value) in userGoneStudying])

    return attention_data, x, y_attention, y_meditation,y_userGoneNotStudying,y_userGoneStudying

"""
def get_mindwave_worksession_data(self, datetime_from, datetime_to,window):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []
    userGoneNotStudying = []
    userGoneStudying = []
    x = []
    index = 0
    worksessions_list = data_processing.get_list_work_sessions(datetime_from,datetime_to,self.options_reason,30)
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except :
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")


        if list_mindwave_data[index][5] == self.treshold_poorSignalMindwave:
            attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
            meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
        else:
            attention_data.append((datetime_from_mindwave,-1))
            meditation_data.append((datetime_from_mindwave,-1))

        canAddNotStudyingEntry = False
        canAddStudyingEntry = False
        for i in range(0,len(worksessions_list)):
            datetime_from_worksession = worksessions_list[i][0]
            datetime_to_worksession = worksessions_list[i][1]


            if datetime_from_mindwave >= datetime_from_worksession and datetime_to_mindwave <= datetime_to_worksession and worksessions_list[i][3] is False:
                canAddNotStudyingEntry = True

            if datetime_from_mindwave >= datetime_from_worksession and datetime_to_mindwave <= datetime_to_worksession and worksessions_list[i][3] is True:
                canAddStudyingEntry = True

        if canAddNotStudyingEntry is True:
            userGoneNotStudying.append((datetime_from_mindwave,1))
        else:
            userGoneNotStudying.append((datetime_from_mindwave,0))

        if canAddStudyingEntry is True:
            userGoneStudying.append((datetime_from_mindwave,1))
        else:
            userGoneStudying.append((datetime_from_mindwave,0))

        index += 1
    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]

    print "--------------------------------"
    print "original"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    y_attention = list_operations.filter_list(y_attention)
    y_meditation = list_operations.filter_list(y_meditation)

    print "after filter_list"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = list_operations.moving_median(y_attention,window_median)
    y_meditation = list_operations.moving_median(y_meditation,window_median)

    print "after moving_median"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = list_operations.movingaverage(y_attention, window)
    y_meditation = list_operations.movingaverage(y_meditation, window)

    print "after movingaverage"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    print "---------------------------"

    y_userGoneNotStudying = list_operations.filter_list([value for (date, value) in userGoneNotStudying])
    y_userGoneStudying = list_operations.filter_list([value for (date, value) in userGoneStudying])

    return attention_data, x, y_attention, y_meditation,y_userGoneNotStudying,y_userGoneStudying
"""
def get_mindwave_manual_logged_activities_data(self, datetime_from, datetime_to,list_manual_logs,selected_activity,window):
    list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
    attention_data = []
    meditation_data = []
    selectedActivity = []
    userGoneStudying = []
    x = []
    index = 0
    listUserGone = DAUserGone_SQLite.get_data_specific_period(datetime_from,datetime_to)
    while index < len(list_mindwave_data):
        try:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
        except :
            datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")


        if list_mindwave_data[index][5] == self.treshold_poorSignalMindwave:
            attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
            meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
        else:
            attention_data.append((datetime_from_mindwave,-1))
            meditation_data.append((datetime_from_mindwave,-1))

        canAddMatchedActivity = False

        for item in list_manual_logs:
            datetime_from_log = item[0]
            datetime_to_log = item[1]

            if datetime_from_mindwave >= datetime_from_log and datetime_to_mindwave <= datetime_to_log and item[2] == selected_activity:
                canAddMatchedActivity = True

        if canAddMatchedActivity is True:
            selectedActivity.append((datetime_from_mindwave,1))
        else:
            selectedActivity.append((datetime_from_mindwave,0))

        index += 1
    x = [date2num(date) for (date, value) in attention_data]
    y_attention = [value for (date, value) in attention_data]
    y_meditation = [value for (date, value) in meditation_data]


    print "--------------------------------"
    print "original"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    y_attention = List_operations.filter_list(y_attention)
    y_meditation = List_operations.filter_list(y_meditation)

    print "after filter_list"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.moving_median(y_attention,window_median)
    y_meditation = List_operations.moving_median(y_meditation,window_median)

    print "after moving_median"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))

    y_attention = List_operations.movingaverage(y_attention, window)
    y_meditation = List_operations.movingaverage(y_meditation, window)

    print "after movingaverage"
    print str("length y_attention: " + str(len(y_attention)))
    print str("length y_meditation: " + str(len(y_meditation)))
    print "---------------------------"
    y_selectedActivity = List_operations.filter_list([value for (date, value) in selectedActivity])

    return attention_data, x, y_attention, y_meditation,y_selectedActivity

def get_average_attention_meditation_specific_period(datetime_from, datetime_to):
    attention_meditation_list = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)

    gemiddelde_attention = 0.0
    gemiddelde_meditation = 0.0

    total = 0.0
    for item in attention_meditation_list:
        gemiddelde_attention += item[3]
        gemiddelde_meditation += item[4]
        total += 1.0

    if total != 0.0:
        gemiddelde_attention = gemiddelde_attention / total
        gemiddelde_meditation = gemiddelde_meditation / total
    return gemiddelde_attention, gemiddelde_meditation
