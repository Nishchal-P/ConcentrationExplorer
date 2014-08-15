import datetime
from exception import Exception

from data_tier import DAUserFeedback_SQLite
def get_average_userfeedback_specific_period(start_datetime_activity_detail,end_datetime_activity_detail):
    gemiddelde_concentratie = 0.0
    totaal = 0.0
    userfeedback = DAUserFeedback_SQLite.get_data_specific_period(start_datetime_activity_detail,end_datetime_activity_detail)
      # gemiddelde berekenen van de userfeedback gegevens voor de periodes van activity_detail
    total_user_feedback_time = 0.0
    for item in userfeedback :
        try:
            datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")

        datetime_to_userfeedback =  datetime_from_userfeedback + datetime.timedelta(seconds=item[4])

        if (datetime_from_userfeedback < end_datetime_activity_detail) and (datetime_to_userfeedback > start_datetime_activity_detail):
            if datetime_from_userfeedback < start_datetime_activity_detail:
                datetime_from_userfeedback = start_datetime_activity_detail
            if datetime_to_userfeedback > end_datetime_activity_detail:
                datetime_to_userfeedback = end_datetime_activity_detail

            difference = datetime_to_userfeedback - datetime_from_userfeedback
            total_user_feedback_time += difference.seconds

    if total_user_feedback_time <= 0:
        raise Exception.ListEmpty('Geen user_feedback gegevens gevonden')
    for item in userfeedback :
        try:
            datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_userfeedback = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
        datetime_to_userfeedback =  datetime_from_userfeedback + datetime.timedelta(seconds=item[4])

        if datetime_from_userfeedback < end_datetime_activity_detail:
            if datetime_from_userfeedback < start_datetime_activity_detail:
                datetime_from_userfeedback = start_datetime_activity_detail
            if datetime_to_userfeedback > end_datetime_activity_detail:
                datetime_to_userfeedback = end_datetime_activity_detail

            difference = datetime_to_userfeedback - datetime_from_userfeedback


            gemiddelde_concentratie += float(item[2] * (float(difference.seconds) / float(total_user_feedback_time)))


    return gemiddelde_concentratie
