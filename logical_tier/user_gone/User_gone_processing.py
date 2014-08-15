from data_tier import DAUserGone_SQLite

import datetime, time
from data_tier import DAEyesDetected_SQLite

def get_eyes_detected_specific_period(datetime_from,datetime_to):
    activities = DAEyesDetected_SQLite.get_data_specific_period(datetime_from,datetime_to)

    time_eyes_detected = 0.0
    total_time = 0.0

    for activity in activities:
        total_time += activity[3]
        if activity[2] == 1:
            time_eyes_detected += activity[3]
    result = 0.0
    if (total_time > 0):
        result = time_eyes_detected / total_time

    return result

# Voor een bepaalde periode, hoeveel % ervan was de gebruiker bv afgeleid?
def get_average_reason(datetime_from,datetime_to,reason) :
    list_UserGone = DAUserGone_SQLite.get_data_specific_period_specific_reason(datetime_from,datetime_to,reason)
    result = 0.0

    date_diff_input = datetime_to - datetime_from

    for item in list_UserGone:
        datetime_from_database = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
        datetime_to_database = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S.%f")

        if datetime_from_database < datetime_from:
            datetime_from_database = datetime_from

        if datetime_to_database > datetime_to:
            datetime_to_database = datetime_to

        date_diff_fromDatabase = (datetime_to_database - datetime_from_database)
        result += (float(date_diff_fromDatabase.seconds) / float(date_diff_input.seconds))
    return round(result,2)

def get_list_userGone(date_from,date_to,options_reason):
    list = DAUserGone_SQLite.get_data_specific_period(date_from,date_to)
    list_result = []
    list_temp = []


    for reason in options_reason:
        # [reason,  totaal, gemiddeld, minimaal, maximaal]
        list_result.append([reason[0],0,0.0,0,0])

        #[reason,aantal voorkomens]
        list_temp.append([reason,0])
    for item in list :
        teller = 0
        try:
            dateFrom_item = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
        except:
            dateFrom_item = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")

        try:
            dateTo_item = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S.%f")
        except:
            dateTo_item = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S")

        difference = dateTo_item - dateFrom_item
        while (teller < len(options_reason)):

            if(options_reason[teller][0] == item[3]):
                list_result[teller][1] += difference.seconds
                list_temp[teller][1] += 1
                # check minimal
                if(list_result[teller][3]==0):
                    list_result[teller][3] = difference.seconds

                if(list_result[teller][3] > difference.seconds):
                    list_result[teller][3] = difference.seconds

                #check maximal
                if(list_result[teller][4] < difference.seconds):
                    list_result[teller][4] = difference.seconds
                break
            teller += 1

    teller = 0
    while(teller < len(list_result)):
        if( list_temp[teller][1] != 0):
            list_result[teller][2] = list_result[teller][1] / list_temp[teller][1]
        teller += 1

    return list_result
