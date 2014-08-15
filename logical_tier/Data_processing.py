from exception import Exception

from data_tier import DARescueTime_SQLite

from logical_tier.user_gone import User_gone_processing
from data_tier import DAUserGone_SQLite
from data_tier import DAMindwave_SQLite
from data_tier import DAErrorReport_SQLite
from data_tier import DASession_SQLite
from data_tier import DAReading_SQLite
from logical_tier.read_detection import Read_detection_processing
from logical_tier.mindwave import Mindwave_data_processing
from logical_tier.userfeedback import Userfeedback_processing
import datetime

#@param datetime_from
#@param datetime_to
#@pre datetime_from < datetime_to
#@return result [activity, time_sec, avg_attention,avg_meditation]
def calculate_average_mindwave(start_datetime_activity_detail, end_datetime_activity_detail,list_mindwave):
    attention_gemiddelde = 0.0
    meditation_gemiddelde = 0.0
    total_attention = 0
    total_meditation = 0
    # item = [id, datetime_from, datetime_to, attention, meditation, ...]
    duration_activity_detail = end_datetime_activity_detail - start_datetime_activity_detail
    total_time_mindwave_in_activity_detail = 0.0
    if len(list_mindwave) == 0:
        message = "Ontbrekende meetgegevens"
        raise Exception.ListEmpty(message)

    for item in list_mindwave:
        try:
            datetime_from_mindwave = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_to_mindwave = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S")

        if datetime_from_mindwave < end_datetime_activity_detail:
            if datetime_from_mindwave < start_datetime_activity_detail:
                datetime_from_mindwave = start_datetime_activity_detail
            if datetime_to_mindwave > end_datetime_activity_detail:
                datetime_to_mindwave = end_datetime_activity_detail

            difference = datetime_to_mindwave - datetime_from_mindwave
            total_time_mindwave_in_activity_detail += difference.seconds
    for item in list_mindwave:
        try:
            datetime_from_mindwave = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_mindwave = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
        try:
            datetime_to_mindwave = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_to_mindwave = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S")

        if datetime_from_mindwave < end_datetime_activity_detail:
            if datetime_from_mindwave < start_datetime_activity_detail:
                datetime_from_mindwave = start_datetime_activity_detail
            if datetime_to_mindwave > end_datetime_activity_detail:
                datetime_to_mindwave = end_datetime_activity_detail

            difference = datetime_to_mindwave - datetime_from_mindwave

            attention_gemiddelde += float(item[3] * (float(difference.seconds) / float(total_time_mindwave_in_activity_detail)))
            meditation_gemiddelde += float(item[4] * (float(difference.seconds) / float(total_time_mindwave_in_activity_detail)))
    return attention_gemiddelde,meditation_gemiddelde


def getListUnimportantActivities(datetime_from,datetime_to,link_to_main):
    daRescueTime = DARescueTime_SQLite.RescueTime(link_to_main)
    unimportant_activities_list = daRescueTime.get_data_unimportant_activities_specific_period_group_by_activity(datetime_from,datetime_to)
    result = []
    previous_datetime_to = None

    for activity in unimportant_activities_list:
        activity_details = daRescueTime.get_data_unimportant_activities_specific_period_activity(datetime_from,datetime_to,activity[1])

        gemiddelde_attention_mindwave = 0.0
        totaal_attention_mindwave = 0

        gemiddelde_meditation_mindwave = 0.0
        totaal_meditation_mindwave = 0

        gemiddelde_reading = 0.0
        totaal_reading = 0.0


        for activity_detail in activity_details:
            start_datetime = datetime.datetime.strptime(activity_detail[1],"%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + datetime.timedelta(minutes=5)

           # Mindwave, gemiddelde berekenen
            list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(start_datetime,end_datetime)
            try:
                gemiddelde_attention_mindwave_temp,gemiddelde_meditation_mindwave_temp = calculate_average_mindwave(start_datetime,end_datetime,list_mindwave_data)
            except Exception.ListEmpty, e:
                DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"data_processing,calculate_average_mindwave(" + str(start_datetime) + ", " + str(end_datetime), e.msg)
                gemiddelde_attention_mindwave = -1
                gemiddelde_meditation_mindwave = -1
                break
            gemiddelde_attention_mindwave += gemiddelde_attention_mindwave_temp
            gemiddelde_meditation_mindwave += gemiddelde_meditation_mindwave_temp

            totaal_attention_mindwave += 1
            totaal_meditation_mindwave += 1

             # reading
            reading_temp = Read_detection_processing.get_average_reading_specific_period(start_datetime,end_datetime)
            if reading_temp > 0:
                gemiddelde_reading += reading_temp
                totaal_reading += 1

            # moet refereren naar item in lijst activity_details, niet naar end_datetime
            previous_datetime_to = datetime.datetime.strptime(activity_detail[1],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=5)


        if totaal_attention_mindwave > 0 and totaal_meditation_mindwave > 0 :
            if gemiddelde_attention_mindwave != -1 and gemiddelde_meditation_mindwave != -1:
                gemiddelde_attention_mindwave = float(gemiddelde_attention_mindwave / totaal_attention_mindwave)
                gemiddelde_meditation_mindwave = float(gemiddelde_meditation_mindwave / totaal_meditation_mindwave)
            if totaal_reading > 0:
                gemiddelde_reading = float(gemiddelde_reading / totaal_reading)
            result.append([activity[1],activity[0],gemiddelde_attention_mindwave,gemiddelde_meditation_mindwave,gemiddelde_reading])

    return  result

def getListUnimportantActivities_V2_buckets(datetime_from,datetime_to,link_to_main):
    daRescueTime = DARescueTime_SQLite.RescueTime(link_to_main)
    unimportant_activities_list = daRescueTime.get_data_unimportant_activities_specific_period_group_by_activity(datetime_from,datetime_to)
    result = []
    previous_datetime_to = None

    for activity in unimportant_activities_list:
        activity_details = daRescueTime.get_data_unimportant_activities_specific_period_activity(datetime_from,datetime_to,activity[1])

        attention_bucket_total = []
        meditation_bucket_total = []

        gemiddelde_reading = 0.0
        totaal_reading = 0.0


        for activity_detail in activity_details:
            start_datetime = datetime.datetime.strptime(activity_detail[1],"%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + datetime.timedelta(minutes=5)

           # Mindwave, gemiddelde berekenen
            list_mindwave_data = Mindwave_data_processing.get_mindwave_data_filtered_smoothed(datetime_from,datetime_to,10)

            # Mindwave, gemiddelde berekenen
            attention_bucket, meditation_bucket = Mindwave_data_processing.get_attention_meditation_buckets(start_datetime,end_datetime,list_mindwave_data)
            attention_bucket_total.append(attention_bucket)
            meditation_bucket_total.append(meditation_bucket)


             # reading
            reading_temp = Read_detection_processing.get_average_reading_specific_period(start_datetime,end_datetime)
            if reading_temp > 0:
                gemiddelde_reading += reading_temp
                totaal_reading += 1

            # moet refereren naar item in lijst activity_details, niet naar end_datetime
            previous_datetime_to = datetime.datetime.strptime(activity_detail[1],"%Y-%m-%d %H:%M:%S") + datetime.timedelta(minutes=5)


        if len(attention_bucket_total) > 0:
            attention_bucket_avg, meditation_bucket_avg = Mindwave_data_processing.merge_buckets(attention_bucket_total, meditation_bucket_total)

            if totaal_reading > 0:
                gemiddelde_reading = float(gemiddelde_reading / totaal_reading)
            result.append([activity[1],activity[0],attention_bucket_avg, meditation_bucket_avg,gemiddelde_reading])

    return  result

def getListImportantActivities_V2_buckets(datetime_from, datetime_to,options_reason,link_to_main):
    daRescueTime = DARescueTime_SQLite.RescueTime(link_to_main)
    #result_rescueTime = DARescueTime_SQLite.get_data_important_activities_specific_period(datetime_from,datetime_to)
    important_activities_list = daRescueTime.get_data_important_activities_specific_period_group_by_activity(datetime_from,datetime_to)

# hier komt het resultaat in per activity. Dus gemiddelde concentratie met tijd activiteit geopend
    result = []
    # Itereren over elke belangrijke activitieit
    for activity in important_activities_list :
        #[DateTime, Time_sec,ActivityDetail, Category, isImportant, ActivityGeneral, Subject_ID]
        activity_details = daRescueTime.get_data_important_activities_specific_period_activity(datetime_from,datetime_to,activity[1])
        # Dan per belangrijke activitieit, in die 5 minuten tijdspanne gaan kijken hoeveel de gebruiker naar het scherm keek
        mindwave_data_list = Mindwave_data_processing.get_mindwave_data_filtered_smoothed(datetime_from,datetime_to,10)

        attention_bucket_total = []
        meditation_bucket_total = []

        gemiddelde_concentratie_userfeedback = 0.0
        totaal_userfeedback = 0

        gemiddelde_eyes_detected = 0.0
        totaal_eyes_detected = 0

        gemiddelde_attention_mindwave = 0.0
        totaal_attention_mindwave = 0

        gemiddelde_meditation_mindwave = 0.0
        totaal_meditation_mindwave = 0

        gemiddelde_reading = 0.0
        totaal_reading = 0.0


        # Bijhouden dat, per keer de gebruiker niet naar het scherm keek, wat was die dan wel aan het doen?
        reason_array = []
        for reason in options_reason:
            reason_array.append([reason[0],0.0])

        for activity_detail in activity_details:
            start_datetime = datetime.datetime.strptime(activity_detail[1],"%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + datetime.timedelta(minutes=5)

            # gemiddelde berekenen van de userfeedback gegevens voor de periodes van activity_detail
            try:
                concentratie = Userfeedback_processing.get_average_userfeedback_specific_period(start_datetime,end_datetime)
                gemiddelde_concentratie_userfeedback += concentratie
                totaal_userfeedback += 1
            except Exception.ListEmpty, e:
                source = "data_processing, function: get_average_userfeedback_specific_period(" + str(start_datetime) + "," + str(end_datetime) + ")"
                DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),source,e.msg)

            gemiddelde_eyes_detected += float(User_gone_processing.get_eyes_detected_specific_period(start_datetime,end_datetime))
            totaal_eyes_detected += 1

            # Mindwave, gemiddelde berekenen
            attention_bucket, meditation_bucket = Mindwave_data_processing.get_attention_meditation_buckets(start_datetime,end_datetime,mindwave_data_list)
            attention_bucket_total.append(attention_bucket)
            meditation_bucket_total.append(meditation_bucket)


            # reason_array opvullen:
            teller_reason = 0

            while(teller_reason < len(options_reason)):
                reason_array[teller_reason][1] += User_gone_processing.get_average_reason(start_datetime,end_datetime,options_reason[teller_reason][0])
                teller_reason += 1

            # reading
            reading_temp = Read_detection_processing.get_average_reading_specific_period(start_datetime,end_datetime)
            if reading_temp > 0:
                gemiddelde_reading += reading_temp
                totaal_reading += 1

        teller_reason = 0
        while (teller_reason < len(reason_array)):
            reason_array[teller_reason][1] = reason_array[teller_reason][1] / float(len(activity_details))
            teller_reason += 1

        if totaal_userfeedback > 0 :
            gemiddelde_concentratie_userfeedback = float((gemiddelde_concentratie_userfeedback / totaal_userfeedback))
        else:
            gemiddelde_concentratie_userfeedback = -1

        if totaal_eyes_detected > 0:
            gemiddelde_eyes_detected = float((gemiddelde_eyes_detected / totaal_eyes_detected))
        else:
            gemiddelde_eyes_detected = 0

        if len(attention_bucket_total) > 0:
            attention_bucket_avg, meditation_bucket_avg = Mindwave_data_processing.merge_buckets(attention_bucket_total, meditation_bucket_total)

        if totaal_reading > 0:
            gemiddelde_reading = float(gemiddelde_reading / totaal_reading)
        else:
            gemiddelde_reading = 0

        result.append([activity[1],activity[0],gemiddelde_concentratie_userfeedback,gemiddelde_eyes_detected,reason_array,attention_bucket_avg, meditation_bucket_avg,gemiddelde_reading,activity[2]])

    return result

def getListImportantActivities(datetime_from, datetime_to,options_reason,link_to_main):
    daRescueTime = DARescueTime_SQLite.RescueTime(link_to_main)
    #result_rescueTime = DARescueTime_SQLite.get_data_important_activities_specific_period(datetime_from,datetime_to)
    important_activities_list = daRescueTime.get_data_important_activities_specific_period_group_by_activity(datetime_from,datetime_to)

# hier komt het resultaat in per activity. Dus gemiddelde concentratie met tijd activiteit geopend
    result = []
    # Itereren over elke belangrijke activitieit
    for activity in important_activities_list :
        #[DateTime, Time_sec,ActivityDetail, Category, isImportant, ActivityGeneral, Subject_ID]
        activity_details = daRescueTime.get_data_important_activities_specific_period_activity(datetime_from,datetime_to,activity[1])
        # Dan per belangrijke activitieit, in die 5 minuten tijdspanne gaan kijken hoeveel de gebruiker naar het scherm keek


        gemiddelde_concentratie_userfeedback = 0.0
        totaal_userfeedback = 0

        gemiddelde_eyes_detected = 0.0
        totaal_eyes_detected = 0

        gemiddelde_attention_mindwave = 0.0
        totaal_attention_mindwave = 0

        gemiddelde_meditation_mindwave = 0.0
        totaal_meditation_mindwave = 0

        gemiddelde_reading = 0.0
        totaal_reading = 0.0


        # Bijhouden dat, per keer de gebruiker niet naar het scherm keek, wat was die dan wel aan het doen?
        reason_array = []
        for reason in options_reason:
            reason_array.append([reason[0],0.0])

        for activity_detail in activity_details:
            start_datetime = datetime.datetime.strptime(activity_detail[1],"%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + datetime.timedelta(minutes=5)

            # gemiddelde berekenen van de userfeedback gegevens voor de periodes van activity_detail
            try:
                concentratie = Userfeedback_processing.get_average_userfeedback_specific_period(start_datetime,end_datetime)
                gemiddelde_concentratie_userfeedback += concentratie
                totaal_userfeedback += 1
            except Exception.ListEmpty, e:
                source = "data_processing, function: get_average_userfeedback_specific_period(" + str(start_datetime) + "," + str(end_datetime) + ")"
                DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),source,e.msg)

            gemiddelde_eyes_detected += float(User_gone_processing.get_eyes_detected_specific_period(start_datetime,end_datetime))
            totaal_eyes_detected += 1

            # Mindwave, gemiddelde berekenen
            list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(start_datetime,end_datetime)
            if (gemiddelde_attention_mindwave != -1) and (gemiddelde_meditation_mindwave != -1):
                try:
                    gemiddelde_attention_mindwave_temp,gemiddelde_meditation_mindwave_temp = calculate_average_mindwave(start_datetime,end_datetime,list_mindwave_data)
                    gemiddelde_attention_mindwave += gemiddelde_attention_mindwave_temp
                    gemiddelde_meditation_mindwave += gemiddelde_meditation_mindwave_temp
                    totaal_attention_mindwave += 1
                    totaal_meditation_mindwave += 1
                except Exception.ListEmpty, e:
                    DAErrorReport_SQLite.insert_row_action(datetime.datetime.today(),"data_processing,calculate_average_mindwave(" + str(start_datetime) + ", " + str(end_datetime), e.msg)
                    gemiddelde_attention_mindwave = -1
                    gemiddelde_meditation_mindwave = -1


            # reason_array opvullen:
            teller_reason = 0

            while(teller_reason < len(options_reason)):
                reason_array[teller_reason][1] += User_gone_processing.get_average_reason(start_datetime,end_datetime,options_reason[teller_reason][0])
                teller_reason += 1

            # reading
            reading_temp = Read_detection_processing.get_average_reading_specific_period(start_datetime,end_datetime)
            if reading_temp > 0:
                gemiddelde_reading += reading_temp
                totaal_reading += 1

        teller_reason = 0
        while (teller_reason < len(reason_array)):
            reason_array[teller_reason][1] = reason_array[teller_reason][1] / float(len(activity_details))
            teller_reason += 1

        if totaal_userfeedback > 0 :
            gemiddelde_concentratie_userfeedback = float((gemiddelde_concentratie_userfeedback / totaal_userfeedback))
        else:
            gemiddelde_concentratie_userfeedback = -1

        if totaal_eyes_detected > 0:
            gemiddelde_eyes_detected = float((gemiddelde_eyes_detected / totaal_eyes_detected))
        else:
            gemiddelde_eyes_detected = 0

        if gemiddelde_attention_mindwave != -1 and gemiddelde_meditation_mindwave != -1:
            gemiddelde_attention_mindwave = float(gemiddelde_attention_mindwave / totaal_attention_mindwave)
            gemiddelde_meditation_mindwave = float(gemiddelde_meditation_mindwave / totaal_meditation_mindwave)

        if totaal_reading > 0:
            gemiddelde_reading = float(gemiddelde_reading / totaal_reading)
        else:
            gemiddelde_reading = 0

        result.append([activity[1],activity[0],gemiddelde_concentratie_userfeedback,gemiddelde_eyes_detected,reason_array,gemiddelde_attention_mindwave,gemiddelde_meditation_mindwave,gemiddelde_reading,activity[2]])

    return result

def remove_screen_attribute(options_reason):
    result = []
    for item in options_reason:
        if item[0] != 'Screen':
            result.append(item)
    return result

def get_list_work_sessions(datetime_from, datetime_to, options_reason,treshold_rescuetime,link_to_main):
    daRescueTime = DARescueTime_SQLite.RescueTime(link_to_main)
    dasession = DASession_SQLite.DASession(link_to_main)

    # list_result = [datetime_from, datetime_to, reason,isStudying,Time_sec]
    list_result = []
    list_rescueTime = daRescueTime.get_data_specific_period(datetime_from,datetime_to)
    list_dates_rescueTime = daRescueTime.get_dates(datetime_from,datetime_to)
    if len(list_dates_rescueTime) == 0:
        raise Exception.ListEmpty("no data saved from RescueTime for this session. Probably the logged session was too short")

    date_from_rescuetime = datetime.datetime.strptime(list_dates_rescueTime[0][0],"%Y-%m-%d %H:%M:%S")
   # if(list_rescueTime[0][6]==1):
    #    list_result.append([date_from_rescuetime,None,'', True,0])
    #else:
     #   list_result.append([date_from_rescuetime,None,'', False,0])
    list_result.append([date_from_rescuetime,None,'', None,0])


    teller_datetime = 0
    while (teller_datetime < (len(list_dates_rescueTime))):
        date_from_rescuetime = datetime.datetime.strptime(list_dates_rescueTime[teller_datetime][0],"%Y-%m-%d %H:%M:%S")
        if(teller_datetime < (len(list_dates_rescueTime)-1)):
            date_to_rescuetime = datetime.datetime.strptime(list_dates_rescueTime[teller_datetime + 1][0],"%Y-%m-%d %H:%M:%S")
        else:
            date_to_rescuetime = date_from_rescuetime + datetime.timedelta(minutes=5)
        if(list_result[(len(list_result)-1)][0] < date_to_rescuetime):
            list_rescueTime_per_period = daRescueTime.get_data_specific_period(date_from_rescuetime,date_to_rescuetime)
            distracted = False
            seconds_activity_important = 0
            seconds_activity_unimportant = 0
            for item_per_period in list_rescueTime_per_period :
                if(item_per_period[6] == 0):
                    seconds_activity_unimportant += item_per_period[2]
                else:
                    seconds_activity_important += item_per_period[2]
            if seconds_activity_unimportant >= treshold_rescuetime:
                distracted = True

            if distracted == True:
                if list_result[len(list_result)-1][3] == None:
                    list_result[len(list_result)-1][3] = False
                else:
                    if list_result[(len(list_result)-1)][3] == True:
                        # controle dat de laatste datetime_from toegevoegd ad list_result lijst, wel degelijk voor date_from_rescuetime ligt
                        if(list_result[(len(list_result)-1)][0] < date_from_rescuetime):
                            list_result[(len(list_result) - 1)][1] = date_from_rescuetime
                            difference  =  list_result[(len(list_result) - 1)][1] -  list_result[(len(list_result) - 1)][0]
                            list_result[(len(list_result) - 1)][4] = difference.seconds
                            list_result.append([date_from_rescuetime,None,'not important user activity',False,0])
            else :
                if list_result[len(list_result)-1][3] == None:
                    list_result[len(list_result)-1][3] = True
                else:
                    if list_result[(len(list_result)-1)][3] == False:
                        # controle dat de laatste datetime_from toegevoegd ad list_result lijst, wel degelijk voor date_from_rescuetime ligt
                        if(list_result[(len(list_result)-1)][0] < date_from_rescuetime):
                            list_result[(len(list_result) - 1)][1] = date_from_rescuetime
                            difference  =  list_result[(len(list_result) - 1)][1] -  list_result[(len(list_result) - 1)][0]
                            list_result[(len(list_result) - 1)][4] += difference.seconds
                            list_result.append([date_from_rescuetime,None,'studying',True,0])


            list_userGone = DAUserGone_SQLite.get_data_specific_period(date_from_rescuetime,date_to_rescuetime)
            teller_usergone = 0
            datetime_to_userGone = None
            list_userGone_not_empty_or_last_item_is_not_screen = False
            while teller_usergone < len(list_userGone):

                if list_userGone[teller_usergone][3] == "screen":
                    list_userGone_not_empty_or_last_item_is_screen = False
                else:
                    list_userGone_not_empty_or_last_item_is_not_screen = True
                    try:
                        datetime_from_userGone =  datetime.datetime.strptime(list_userGone[teller_usergone][1],"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        datetime_from_userGone =  datetime.datetime.strptime(list_userGone[teller_usergone][1],"%Y-%m-%d %H:%M:%S")

                    try:
                        datetime_to_userGone =  datetime.datetime.strptime(list_userGone[teller_usergone][2],"%Y-%m-%d %H:%M:%S.%f")
                    except:
                        datetime_to_userGone =  datetime.datetime.strptime(list_userGone[teller_usergone][2],"%Y-%m-%d %H:%M:%S")

                    if (date_to_rescuetime >= datetime_from_userGone) and (date_from_rescuetime <= datetime_to_userGone):

                        if(list_result[len(list_result)-1][0] < datetime_from_userGone) and (list_result[len(list_result)-1][0] != datetime_to_userGone):
                            if(list_userGone[teller_usergone][5]==0):
                                list_result[(len(list_result) - 1)][1] = datetime_from_userGone
                                difference  =  list_result[(len(list_result) - 1)][1] -  list_result[(len(list_result) - 1)][0]
                                list_result[(len(list_result) - 1)][4] = difference.seconds
                                list_result.append([datetime_from_userGone,datetime_to_userGone,list_userGone[teller_usergone][3],False,(datetime_to_userGone - datetime_from_userGone).seconds])
                                list_result.append([datetime_to_userGone,None,'',None,-1])
                            else:
                                list_result[(len(list_result) - 1)][1] = datetime_from_userGone
                                difference  =  list_result[(len(list_result) - 1)][1] -  list_result[(len(list_result) - 1)][0]
                                list_result[(len(list_result) - 1)][4] = difference.seconds

                                list_result.append([datetime_from_userGone,datetime_to_userGone,list_userGone[teller_usergone][3],True,(datetime_to_userGone - datetime_from_userGone).seconds])
                                list_result.append([datetime_to_userGone,None,'',None,-1])

                teller_usergone += 1
            if list_userGone_not_empty_or_last_item_is_not_screen:
                if len(dasession.get_period_specific_date(datetime_to_userGone)) == 0:
                    list_result[len(list_result) - 1][1] = date_to_rescuetime
                    list_result[len(list_result) - 1][2] = 'no tracking info'
                    list_result[len(list_result) - 1][3] = False

                    difference  =  list_result[(len(list_result) - 1)][1] -  list_result[(len(list_result) - 1)][0]
                    list_result[(len(list_result) - 1)][4] = difference.seconds

                    list_result.append([date_to_rescuetime,None,'',None,-1])

        teller_datetime += 1
    if datetime_to_userGone != None :
        if date_to_rescuetime < datetime_to_userGone:
            list_result[len(list_result)-1][1] = datetime_to_userGone
            difference = datetime_to_userGone - list_result[len(list_result)-1][0]
        else:
            list_result[len(list_result)-1][1] = date_to_rescuetime
            difference = date_to_rescuetime - list_result[len(list_result)-1][0]
    else:
        list_result[len(list_result)-1][1] = date_to_rescuetime
        difference = date_to_rescuetime - list_result[len(list_result)-1][0]

    list_result[len(list_result)-1][4] = difference.seconds


       # print str('date_from_rescuetime: ' + str(date_from_rescuetime) + '\t' + 'date_to_rescuetime:' + str(date_to_rescuetime))
    return list_result

def get_list_workSession_amount_details(list_worksessions, options_reason):
    # list_worksessions: [datetime_from, datetime_to, reason,isStudying, Time_sec]
    list_worksessions_copy = list_worksessions
    # [isStudying, reason, total, amount, avg, min, max]
    list_result = []

    list_result.append([True,'studying',0,0,0.0,-1,-1])
    list_result.append([True,'not important user activity',0,0,0.0,-1,-1])
    for item in options_reason:
        if(item[2] == 0):
            list_result.append([False,item[0],0,0,0.0,-1,-1])

    # list_worksessions filteren, 2 opeenvolgende True sessions samen nemen
    teller = 0

    list_filtered_worksessions = []
    while(teller < len(list_worksessions_copy)):
        if(teller == 0 ):
            list_filtered_worksessions.append([list_worksessions_copy[teller][0],list_worksessions_copy[teller][1],list_worksessions_copy[teller][2],list_worksessions_copy[teller][3],list_worksessions_copy[teller][4]])
        else :
            if(list_worksessions_copy[teller][3] == True) and (list_worksessions_copy[teller - 1][3] == True):
                index_previousRow = (len(list_filtered_worksessions)-1)
                list_filtered_worksessions[index_previousRow][1] = list_worksessions_copy[teller][1]
                list_filtered_worksessions[index_previousRow][2] += ', ' + list_worksessions_copy[teller][2]
                difference =  list_filtered_worksessions[index_previousRow][1] -  list_filtered_worksessions[index_previousRow][0]
                list_filtered_worksessions[index_previousRow][4] = difference.seconds
            else :
                 list_filtered_worksessions.append([list_worksessions_copy[teller][0],list_worksessions_copy[teller][1],list_worksessions_copy[teller][2],list_worksessions_copy[teller][3],list_worksessions_copy[teller][4]])

        teller += 1



    for session in list_filtered_worksessions:
        if(session[3] == True):
            # total
            list_result[0][2] += session[4]
            # Amount
            list_result[0][3] += 1
            # Min
            if(list_result[0][5] == -1) or (session[4] < list_result[0][5]):
                list_result[0][5] = session[4]
            # Max
            if(session[4] > list_result[0][6]):
                list_result[0][6] = session[4]

        else :
            for item in list_result :
                if(item[1] == session[2]):
                    # total
                    item[2] += session[4]
                    # Amount
                    item[3] += 1
                    # Min
                    if(item[5] == -1) or (session[4] < item[5]):
                        item[5] = session[4]
                    # Max
                    if(session[4] > item[6]):
                        item[6] = session[4]
                    break

    # calculate average
    for item in list_result :
        if(item[3] > 0) :
            item[4] = item[2] / item[3]

    return list_result

