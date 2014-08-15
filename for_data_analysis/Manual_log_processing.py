from exception import Exception
from data_tier import DARescueTime_program_keys_SQLite
from data_tier import DARescueTime_SQLite
from logical_tier.mindwave import Mindwave_data_processing
from for_data_analysis import Manual_log
from for_data_analysis import Calculate_statistics_enumeration

class ManualLog_data_processing():
    treshold_activity_duration = 5
    def __init__(self,link_to_form_main):
        self.daRescueTime_program_keys = DARescueTime_program_keys_SQLite.RescueTime_program_key(link_to_form_main)
        self.darescuetime = DARescueTime_SQLite.RescueTime(link_to_form_main)
        self.link_to_form_main = link_to_form_main

    def get_list_concentration_differences_manual_log(self,manual_log_list,mindwave_data_list):

        result_x = []
        result_y = []
        window_avg = 5

        index_m = 0
        for i in range(0,len(manual_log_list)):
            datetime_from_ml = manual_log_list[i][0]
            while index_m < len(mindwave_data_list):
                datetime_from_mindwave = mindwave_data_list[index_m][0]
                datetime_to_mindwave = mindwave_data_list[index_m][1]
                if datetime_from_mindwave <= datetime_from_ml and datetime_to_mindwave >= datetime_from_ml:
                    avg_before_att,avg_before_med,avg_after_att,avg_after_med = self.get_average_samples(mindwave_data_list,index_m,window_avg)
                    result_y.append(avg_after_att - avg_before_att)
                    result_x.append(i)
                    index_m += 1
                    break
                index_m += 1
        print 'diff'
        print "result_x:"
        print result_x
        print "result_y:"
        print result_y
        return result_x, result_y

    def get_list_concentration_differences_manual_log_specific_switch(self,manual_log_list,mindwave_data_list,activity_from, activity_to):
        result_x = []
        result_y = []
        window_avg = 10

        index_m = 0
        for i in range(0,len(manual_log_list)):
            if i == 2:
                pass
            datetime_from_ml = manual_log_list[i][0]
            while index_m < len(mindwave_data_list):
                datetime_from_mindwave = mindwave_data_list[index_m][0]
                datetime_to_mindwave = mindwave_data_list[index_m][1]
                if datetime_from_mindwave <= datetime_from_ml and datetime_to_mindwave >= datetime_from_ml:
                    if i > 0:
                        if manual_log_list[i-1][2] == activity_from and manual_log_list[i][2] == activity_to:
                            avg_before_att,avg_before_med,avg_after_att,avg_after_med = self.get_average_samples(mindwave_data_list,index_m,window_avg)
                            result_y.append(avg_after_att - avg_before_att)
                            result_x.append(i)
                            index_m += 1
                    break
                index_m += 1
        return result_x, result_y

    def get_average_samples(self,mindwave_data,index_mindwave, window_avg):
        avg_before_att = 0.0
        avg_before_med = 0.0

        avg_after_att = 0.0
        avg_after_med = 0.0
        if (index_mindwave - window_avg) >= 0 and (index_mindwave + window_avg) < len(mindwave_data):

            total = 0.0
            for i_mw in range (index_mindwave - window_avg+1,index_mindwave+1):
                avg_before_att += mindwave_data[i_mw][2]
                avg_before_med += mindwave_data[i_mw][3]
                total += 1.0
            avg_before_att = float(avg_before_att / total)
            avg_before_med = float(avg_before_med / total)

            total = 0.0
            for i_mw in range (index_mindwave,index_mindwave + window_avg):
                avg_after_att += mindwave_data[i_mw][2]
                avg_after_med += mindwave_data[i_mw][3]
                total += 1.0
            avg_after_att = float(avg_after_att / total)
            avg_after_med = float(avg_after_med / total)

        return avg_before_att,avg_before_med,avg_after_att,avg_after_med


    def get_list_impact_concentration_manual_logs(self,manual_log_list,mindwave_data):
        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_enkel_programmas_websites()
        datetime_from = manual_log_testpersoon_B[0][0]
        datetime_to = manual_log_testpersoon_B[len(manual_log_testpersoon_B) - 1][1]

        mindwave_data_list = Mindwave_data_processing.get_mindwave_data_filtered_smoothed(datetime_from,datetime_to,10)

        result_x, result_y =  self.get_list_concentration_differences_manual_log(manual_log_testpersoon_B,mindwave_data_list)


        return result_x, result_y

    def get_list_concentration_time_spent_activity(self,manual_log_list,mindwave_data,activity,type_statistics):
        result_x = []
        result_y = []
        for item in manual_log_list:
            difference = (item[1] - item[0]).seconds
            if item[2] == activity and difference >= self.treshold_activity_duration:
                try:
                    sublist = Mindwave_data_processing.get_sublist(mindwave_data,item[0],item[1])
                    if type_statistics == Calculate_statistics_enumeration.AVG:
                        attention, meditation = Mindwave_data_processing.calculate_avg_attention_meditation(sublist)
                    elif type_statistics == Calculate_statistics_enumeration.STD:
                        attention, meditation = Mindwave_data_processing.calculate_std_attention_meditation(sublist)

                    result_x.append(difference)
                    result_y.append(attention)
                except Exception,e:
                    print str(e)
        return result_x, result_y

    def get_list_amount_used_programs_concentration_per_interval(self,mindwave_data,manual_log, list_dates_interval,type_statistic):
        result_x = []
        result_y = []
        for i in range(0,len(list_dates_interval)):
            datetime_from = list_dates_interval[i][0]
            datetime_to = list_dates_interval[i][1]
            sublist = Mindwave_data_processing.get_sublist(mindwave_data,datetime_from,datetime_to)
            try:
                if type_statistic==Calculate_statistics_enumeration.AVG:
                    attention, meditation = Mindwave_data_processing.calculate_avg_attention_meditation(sublist)
                elif type_statistic==Calculate_statistics_enumeration.STD:
                    attention, meditation = Mindwave_data_processing.calculate_std_attention_meditation(sublist)
                else:
                    raise Exception.UnknownID("The type_statistics ID is unknown")
                amount = self.count_activities(manual_log,datetime_from,datetime_to)

                result_x.append(amount)
                result_y.append(attention)
            except Exception, e:
                str(e)

        return result_x, result_y



    def count_activities(self,manual_log, datetime_from, datetime_to):
        total = 0.0
        for item in manual_log:
            if (item[0] >= datetime_from and item[0] <= datetime_to) or (item[1] >= datetime_from and item[1] <= datetime_to):
                total += 1.0

        return total

    def get_statistics_attention_userstates(self,activities,manual_log_list, mindwave_data_list,statistic_type):
        result_x = []
        result_y = []
        for activity in activities:
            try:
                sublist_mindwave_activity = []
                for item in manual_log_list:
                    if item[2] == activity:
                        sublist_mindwave_activity += Mindwave_data_processing.get_sublist(mindwave_data_list,item[0],item[1])
                if statistic_type == Calculate_statistics_enumeration.AVG:
                    attention, meditation = Mindwave_data_processing.calculate_avg_attention_meditation(sublist_mindwave_activity)
                elif statistic_type == Calculate_statistics_enumeration.STD:
                    attention, meditation = Mindwave_data_processing.calculate_std_attention_meditation(sublist_mindwave_activity)
                else:
                    raise Exception.UnknownID("The type_statistics ID is unknown")
                result_y.append(attention)
                result_x.append(activity)
            except Exception, e:
                str(e)
        print "userstates"
        print "result_x:"
        print result_x
        print "result_y"
        print result_y
        return result_x, result_y
