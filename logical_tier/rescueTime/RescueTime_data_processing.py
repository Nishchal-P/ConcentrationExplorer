import datetime

from data_tier import DARescueTime_program_keys_SQLite
from data_tier import DARescueTime_SQLite
from logical_tier.mindwave import Mindwave_data_processing

class RescueTime_data_processing():
    def __init__(self,link_to_form_main):
        self.daRescueTime_program_keys = DARescueTime_program_keys_SQLite.RescueTime_program_key(link_to_form_main)
        self.darescuetime = DARescueTime_SQLite.RescueTime(link_to_form_main)
        self.link_to_form_main = link_to_form_main

    def get_dates_list(self,datetime_from, datetime_to):
        dates_rescuetime = self.darescuetime.get_dates(datetime_from, datetime_to)
        result = []
        for item in dates_rescuetime:
            start_datetime = datetime.datetime.strptime(item[0],"%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + datetime.timedelta(minutes=5)
            result.append([start_datetime, end_datetime])

        return result