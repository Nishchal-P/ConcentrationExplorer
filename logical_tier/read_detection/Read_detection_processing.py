import datetime, time
from data_tier import DAReading_SQLite
def get_average_reading_specific_period(start_datetime_activity_detail,end_datetime_activity_detail):
    daReacing = DAReading_SQLite.DAReading('')
    gemiddelde_reading = 0.0


    reading = daReacing.get_data_specific_period(start_datetime_activity_detail,end_datetime_activity_detail)

    for item in reading :
        try:
            datetime_from_reading = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_from_reading = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")

        try:
            datetime_to_reading = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S.%f")
        except:
            datetime_to_reading = datetime.datetime.strptime(item[2],"%Y-%m-%d %H:%M:%S")

        if (datetime_from_reading < end_datetime_activity_detail) and (datetime_to_reading > start_datetime_activity_detail):
            if datetime_from_reading < start_datetime_activity_detail:
                datetime_from_reading = start_datetime_activity_detail
            if datetime_to_reading > end_datetime_activity_detail:
                datetime_to_reading = end_datetime_activity_detail

            difference = datetime_to_reading - datetime_from_reading


        total_time = end_datetime_activity_detail - start_datetime_activity_detail
        if total_time.seconds > 0:
            gemiddelde_reading = float((float(difference.seconds) / float(total_time.seconds)))
    return gemiddelde_reading
