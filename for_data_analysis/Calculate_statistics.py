from exception import Exception

import Manual_log_processing
import Manual_log
from logical_tier.mindwave import Mindwave_data_processing
from logical_tier.rescueTime import RescueTime_data_processing
from data_tier import DARescueTime_SQLite
from data_tier import DASession_SQLite
from for_data_analysis import Calculate_statistics_enumeration
class CalculateStatistics():
    link_to_main = ''
    folder = 'for_data_analysis/'
    manualLogDataProcessing = None
    rescuetimeDataProcessing = None
    dasession = None
    darescuetime = None
    window_mindwave = 10
    def __init__(self,link_to_main):
        self.manualLogDataProcessing = Manual_log_processing.ManualLog_data_processing(self.link_to_main)
        self.rescuetimeDataProcessing = RescueTime_data_processing.RescueTime_data_processing(self.link_to_main)
        self.dasession = DASession_SQLite.DASession(self.link_to_main)
        self.darescuetime = DARescueTime_SQLite.RescueTime(self.link_to_main)
        self.link_to_main = link_to_main

    def get_statistics_session_testpersoon_B(self):
        session_id = 41
        datetime_from_session, datetime_to_session = self.dasession.get_dates_session(session_id)
        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_enkel_programmas_websites()
        datetime_from = manual_log_testpersoon_B[0][0]
        datetime_to = manual_log_testpersoon_B[len(manual_log_testpersoon_B) - 1][1]
        mindwave_data_list = Mindwave_data_processing.get_mindwave_data_filtered_smoothed_middle_moving_median(datetime_from,datetime_to,self.window_mindwave)

        list_dates = self.rescuetimeDataProcessing.get_dates_list(datetime_from_session, datetime_to_session)

        result_x_diff, result_y_diff =  self.manualLogDataProcessing.get_list_concentration_differences_manual_log(manual_log_testpersoon_B,mindwave_data_list)

        result_x_amount_avg, result_y_amount_avg = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_B,list_dates,Calculate_statistics_enumeration.AVG)
        result_x_amount_std, result_y_amount_std = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_B,list_dates,Calculate_statistics_enumeration.STD)

        result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.AVG)
        result_x_std_rescuetime_amount, result_y_std_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.STD)



        activities_important = ["Wikipedia","Latex"]

        result_x_avg, result_y_avg = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.AVG)
        result_x_std, result_y_std = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg = ResultTuple(result_x_avg, result_y_avg)
        resultTuple_std = ResultTuple(result_x_std, result_y_std)
        for i in range(1,len(activities_important)):
            result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.AVG)
            result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.STD)
            resultTuple_avg.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
            resultTuple_std.merge(ResultTuple(result_x_std_temp,result_y_std_temp))

        activity_from = "Latex"
        activity_to = "Wikipedia"
        result_x_diff_specific_switch, result_y_diff_specific_switch = self.manualLogDataProcessing.get_list_concentration_differences_manual_log_specific_switch(manual_log_testpersoon_B,mindwave_data_list,activity_from,activity_to)
        resultTuple_diff_specific_switch = ResultTuple(result_x_diff_specific_switch,result_y_diff_specific_switch)



        # ////////////////////////////
        # /// with all activities ////
        # ////////////////////////////
        result_x_avg_all_act, result_y_avg_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities[0],Calculate_statistics_enumeration.AVG)
        result_x_std_all_act, result_y_std_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg_all_act = ResultTuple(result_x_avg_all_act, result_y_avg_all_act)
        resultTuple_std_all_act = ResultTuple(result_x_std_all_act, result_y_std_all_act)
        for i in range(1,len(activities)):
            try:
                result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities[i],Calculate_statistics_enumeration.AVG)
                result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_B,mindwave_data_list,activities[i],Calculate_statistics_enumeration.STD)
                resultTuple_avg_all_act.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
                resultTuple_std_all_act.merge(ResultTuple(result_x_std_temp,result_y_std_temp))
            except:
                pass


        # ////////////////////////////


        resultTuple_diff = ResultTuple(result_x_diff, result_y_diff)

        resultTuple_amount_avg = ResultTuple(result_x_amount_avg, result_y_amount_avg)
        resultTuple_amount_std = ResultTuple(result_x_amount_std, result_y_amount_std)

        resultTuple_avg_rescuetime_amount = ResultTuple(result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount)
        resultTuple_std_rescuetime_amount = ResultTuple(result_x_std_rescuetime_amount, result_y_std_rescuetime_amount)

        filename = self.folder + "data_analysis_results/testpersoon_B/"
        # //////////////////////
        # /// all activities ///
        # //////////////////////
        self.generate_csv("Time_spent_seconds","Concentration avg",resultTuple_avg_all_act,filename + "comparison time_spent_sec against average concentration all activities")
        self.generate_csv("Time_spent_seconds","Concentration std",resultTuple_std_all_act,filename + "comparison time_spent_sec against std concentration all activities")
        # //////////////////////
        self.generate_csv("Time_spent_seconds","Concentration avg",resultTuple_avg,filename + "comparison time_spent_sec against average concentration")
        self.generate_csv("Time_spent_seconds","Concentration std",resultTuple_std,filename + "comparison time_spent_sec against std concentration")

        self.generate_csv("Switch ID","Concentration avg",resultTuple_diff,filename + "comparison concentration difference when switch between activities")

        self.generate_csv("Switch ID","Concentration avg",resultTuple_diff_specific_switch,filename + "comparison concentration difference specific switch between activities")

        self.generate_csv("Amount","Concentration avg",resultTuple_amount_avg,filename + "comparison amount used programs with avg concentration")
        self.generate_csv("Amount","Concentration std",resultTuple_amount_std,filename + "comparison amount used programs with std concentration")

        self.generate_csv("Amount","Concentration avg",resultTuple_avg_rescuetime_amount,filename + "comparision RescueTime amount concentration avg")
        self.generate_csv("Amount","Concentration std",resultTuple_std_rescuetime_amount,filename + "comparision RescueTime amount concentration std")


        resultObject = ResultObject()
        resultObject.set_result_timeSpent_activity_avg(resultTuple_avg)
        resultObject.set_result_timeSpent_activity_std(resultTuple_std)

        resultObject.set_concentration_diff_activity_switch_avg(resultTuple_diff)

        resultObject.set_concentration_diff_specific_activity_switch_avg(resultTuple_diff_specific_switch)

        resultObject.set_result_amount_used_programs_avg(resultTuple_amount_avg)
        resultObject.set_result_amount_used_programs_std(resultTuple_amount_std)

        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_avg(resultTuple_avg_rescuetime_amount)
        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_std(resultTuple_std_rescuetime_amount)

        return resultObject

    def get_statistics_session_testpersoon_A(self):
        session_id = 42
        datetime_from_session, datetime_to_session = self.dasession.get_dates_session(session_id)
        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_testpersoon_A_enkel_programmas_websites()
        userstates,manual_log_testpersoon_A_userstates = Manual_log.get_manual_logfile_userstates_testpersoon_A()
        datetime_from = manual_log_testpersoon_A[0][0]
        datetime_to = manual_log_testpersoon_A[len(manual_log_testpersoon_A) - 1][1]
        mindwave_data_list = Mindwave_data_processing.get_mindwave_data_filtered_smoothed_middle_moving_median(datetime_from,datetime_to,self.window_mindwave)

        list_dates = self.rescuetimeDataProcessing.get_dates_list(datetime_from_session, datetime_to_session)

        activities_important = ["Google docs"]

        result_x_avg, result_y_avg = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.AVG)
        result_x_std, result_y_std = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg = ResultTuple(result_x_avg, result_y_avg)
        resultTuple_std = ResultTuple(result_x_std, result_y_std)
        for i in range(1,len(activities_important)):
            result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.AVG)
            result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.STD)
            resultTuple_avg.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
            resultTuple_std.merge(ResultTuple(result_x_std_temp,result_y_std_temp))

        activity_from = "Google docs"
        activity_to = "Surfing internet"
        result_x_diff_specific_switch, result_y_diff_specific_switch = self.manualLogDataProcessing.get_list_concentration_differences_manual_log_specific_switch(manual_log_testpersoon_A,mindwave_data_list,activity_from,activity_to)
        resultTuple_diff_specific_switch = ResultTuple(result_x_diff_specific_switch,result_y_diff_specific_switch)



        # ////////////////////////////
        # /// with all activities ////
        # ////////////////////////////
        result_x_avg_all_act, result_y_avg_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities[0],Calculate_statistics_enumeration.AVG)
        result_x_std_all_act, result_y_std_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg_all_act = ResultTuple(result_x_avg_all_act, result_y_avg_all_act)
        resultTuple_std_all_act = ResultTuple(result_x_std_all_act, result_y_std_all_act)
        for i in range(1,len(activities)):
            try:
                result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities[i],Calculate_statistics_enumeration.AVG)
                result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_A,mindwave_data_list,activities[i],Calculate_statistics_enumeration.STD)
                resultTuple_avg_all_act.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
                resultTuple_std_all_act.merge(ResultTuple(result_x_std_temp,result_y_std_temp))
            except:
                pass


        # ////////////////////////////




        result_x_diff, result_y_diff =  self.manualLogDataProcessing.get_list_concentration_differences_manual_log(manual_log_testpersoon_A,mindwave_data_list)

        result_x_amount_avg, result_y_amount_avg = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_A,list_dates,Calculate_statistics_enumeration.AVG)
#        result_x_amount_std, result_y_amount_std = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_A,list_dates,calculate_statistics_enumeration.STD)

        result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.AVG)
        result_x_std_rescuetime_amount, result_y_std_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.STD)

        result_x_avg_userstate, result_y_avg_userstate = self.manualLogDataProcessing.get_statistics_attention_userstates(userstates,manual_log_testpersoon_A_userstates,mindwave_data_list,Calculate_statistics_enumeration.AVG)
        result_x_std_userstate, result_y_std_userstate = self.manualLogDataProcessing.get_statistics_attention_userstates(userstates,manual_log_testpersoon_A_userstates,mindwave_data_list,Calculate_statistics_enumeration.STD)


        resultTuple_diff = ResultTuple(result_x_diff, result_y_diff)

        resultTuple_amount_avg = ResultTuple(result_x_amount_avg, result_y_amount_avg)
  #      resultTuple_amount_std = ResultTuple(result_x_amount_std, result_y_amount_std)

        resultTuple_avg_rescuetime_amount = ResultTuple(result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount)
        resultTuple_std_rescuetime_amount = ResultTuple(result_x_std_rescuetime_amount, result_y_std_rescuetime_amount)

        resultTuple_avg_userstate = ResultTuple(result_x_avg_userstate,result_y_avg_userstate)
        resultTuple_std_userstate = ResultTuple(result_x_std_userstate,result_y_std_userstate)

        filename = self.folder + "data_analysis_results/testpersoon_A/"
        # //////////////////////
        # /// all activities ///
        # //////////////////////
        self.generate_csv("Time_spent_seconds","Concentration avg",resultTuple_avg_all_act,filename + "comparison time_spent_sec against average concentration all activities")
        self.generate_csv("Time_spent_seconds","Concentration std",resultTuple_std_all_act,filename + "comparison time_spent_sec against std concentration all activities")
        # //////////////////////
        self.generate_csv("Time_spent_sec","Concentration avg",resultTuple_avg,filename + "comparison time_spent_sec against average concentration")
        self.generate_csv("Time_spent_sec","Concentration std",resultTuple_std,filename + "comparison time_spent_sec against std concentration")

        self.generate_csv("Switch ID","Concentration avg",resultTuple_diff,filename + "comparison concentration difference when switch between activities")

        self.generate_csv("Switch ID","Concentration avg",resultTuple_diff_specific_switch,filename + "comparison concentration difference specific switch between activities")

        self.generate_csv("Amount","Concentration avg",resultTuple_amount_avg,filename + "comparison amount used programs with avg concentration")
#        self.generate_csv("Amount","Concentration std",resultTuple_amount_std,filename + "comparison amount used programs with std concentration")

        self.generate_csv("Amount","Concentration avg",resultTuple_avg_rescuetime_amount,filename + "comparision RescueTime amount concentration avg")
        self.generate_csv("Amount","Concentration std",resultTuple_std_rescuetime_amount,filename + "comparision RescueTime amount concentration std")



        self.generate_csv("Userstate","Concentration avg",resultTuple_avg_userstate,filename + "comparision userstates concentration avg")
        self.generate_csv("Amount","Concentration std",resultTuple_std_userstate,filename + "comparision userstates concentration std")


        resultObject = ResultObject()
        resultObject.set_result_timeSpent_activity_avg(resultTuple_avg)
        resultObject.set_result_timeSpent_activity_std(resultTuple_std)

        resultObject.set_concentration_diff_activity_switch_avg(resultTuple_diff)

        resultObject.set_concentration_diff_specific_activity_switch_avg(resultTuple_diff_specific_switch)

        resultObject.set_result_amount_used_programs_avg(resultTuple_amount_avg)
  #      resultObject.set_result_amount_used_programs_std(resultTuple_amount_std)

        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_avg(resultTuple_avg_rescuetime_amount)
        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_std(resultTuple_std_rescuetime_amount)

        return resultObject

    def get_statistics_session_testpersoon_C(self):
        session_id = 8
        datetime_from_session, datetime_to_session = self.dasession.get_dates_session(session_id)
        activities,manual_log_testpersoon_C = Manual_log.get_manual_logfile_testpersoon_C_session_1_activities_only()
        userstates,manual_log_testpersoon_C_userstates = Manual_log.get_manual_logfile_testpersoon_C_session_1_userstates()
        datetime_from = manual_log_testpersoon_C[0][0]
        datetime_to = manual_log_testpersoon_C[len(manual_log_testpersoon_C) - 1][1]
        mindwave_data_list = Mindwave_data_processing.get_mindwave_data_filtered_smoothed_middle_moving_median(datetime_from,datetime_to,self.window_mindwave)

        list_dates = self.rescuetimeDataProcessing.get_dates_list(datetime_from_session, datetime_to_session)

        activities_important = ["Wikipedia","Latex","Adobe Reader","Webmail", "Google Docs"]

        result_x_avg, result_y_avg = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.AVG)
        result_x_std, result_y_std = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg = ResultTuple(result_x_avg, result_y_avg)
        resultTuple_std = ResultTuple(result_x_std, result_y_std)
        for i in range(1,len(activities_important)):
            result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.AVG)
            result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.STD)
            resultTuple_avg.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
            resultTuple_std.merge(ResultTuple(result_x_std_temp,result_y_std_temp))

        # ////////////////////////////
        # /// with all activities ////
        # ////////////////////////////
        result_x_avg_all_act, result_y_avg_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities[0],Calculate_statistics_enumeration.AVG)
        result_x_std_all_act, result_y_std_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg_all_act = ResultTuple(result_x_avg_all_act, result_y_avg_all_act)
        resultTuple_std_all_act = ResultTuple(result_x_std_all_act, result_y_std_all_act)
        for i in range(1,len(activities)):
            try:
                result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities[i],Calculate_statistics_enumeration.AVG)
                result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_C,mindwave_data_list,activities[i],Calculate_statistics_enumeration.STD)
                resultTuple_avg_all_act.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
                resultTuple_std_all_act.merge(ResultTuple(result_x_std_temp,result_y_std_temp))
            except:
                pass


        # ////////////////////////////


        result_x_diff, result_y_diff =  self.manualLogDataProcessing.get_list_concentration_differences_manual_log(manual_log_testpersoon_C,mindwave_data_list)

        result_x_amount_avg, result_y_amount_avg = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_C,list_dates,Calculate_statistics_enumeration.AVG)
        result_x_amount_std, result_y_amount_std = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_C,list_dates,Calculate_statistics_enumeration.STD)

        result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.AVG)
        result_x_std_rescuetime_amount, result_y_std_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.STD)

        result_x_avg_userstate, result_y_avg_userstate = self.manualLogDataProcessing.get_statistics_attention_userstates(userstates,manual_log_testpersoon_C_userstates,mindwave_data_list,Calculate_statistics_enumeration.AVG)
        result_x_std_userstate, result_y_std_userstate = self.manualLogDataProcessing.get_statistics_attention_userstates(userstates,manual_log_testpersoon_C_userstates,mindwave_data_list,Calculate_statistics_enumeration.STD)

        resultTuple_diff = ResultTuple(result_x_diff, result_y_diff)

        resultTuple_amount_avg = ResultTuple(result_x_amount_avg, result_y_amount_avg)
        resultTuple_amount_std = ResultTuple(result_x_amount_std, result_y_amount_std)

        resultTuple_avg_rescuetime_amount = ResultTuple(result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount)
        resultTuple_std_rescuetime_amount = ResultTuple(result_x_std_rescuetime_amount, result_y_std_rescuetime_amount)

        resultTuple_avg_userstate = ResultTuple(result_x_avg_userstate,result_y_avg_userstate)
        resultTuple_std_userstate = ResultTuple(result_x_std_userstate,result_y_std_userstate)

        filename = self.folder + "data_analysis_results/testpersoon_C/"

        # //////////////////////
        # /// all activities ///
        # //////////////////////
        self.generate_csv("Time_spent_seconds","Concentration avg",resultTuple_avg_all_act,filename + "comparison time_spent_sec against average concentration all activities")
        self.generate_csv("Time_spent_seconds","Concentration std",resultTuple_std_all_act,filename + "comparison time_spent_sec against std concentration all activities")
        # //////////////////////

        self.generate_csv("Time_spent_seconds","Concentration avg",resultTuple_avg,filename + "comparison time_spent_sec against average concentration")
        self.generate_csv("Time_spent_seconds","Concentration std",resultTuple_std,filename + "comparison time_spent_sec against std concentration")

        self.generate_csv("Unknown","Concentration std",resultTuple_diff,filename + "comparison concentration difference when switch between activities")

        self.generate_csv("Amount","Concentration avg",resultTuple_amount_avg,filename + "comparison amount used programs with avg concentration")
        self.generate_csv("Amount","Concentration std",resultTuple_amount_std,filename + "comparison amount used programs with std concentration")

        self.generate_csv("Amount","Concentration avg",resultTuple_avg_rescuetime_amount,filename + "comparision RescueTime amount concentration avg")
        self.generate_csv("Amount","Concentration std",resultTuple_std_rescuetime_amount,filename + "comparision RescueTime amount concentration std")



        self.generate_csv("Userstate","Concentration avg",resultTuple_avg_userstate,filename + "comparision userstates concentration avg")
        self.generate_csv("Amount","Concentration std",resultTuple_std_userstate,filename + "comparision userstates concentration std")


        resultObject = ResultObject()
        resultObject.set_result_timeSpent_activity_avg(resultTuple_avg)
        resultObject.set_result_timeSpent_activity_std(resultTuple_std)

        resultObject.set_concentration_diff_activity_switch_avg(resultTuple_diff)

        resultObject.set_result_amount_used_programs_avg(resultTuple_amount_avg)
        resultObject.set_result_amount_used_programs_std(resultTuple_amount_std)

        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_avg(resultTuple_avg_rescuetime_amount)
        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_std(resultTuple_std_rescuetime_amount)

        return resultObject


    def get_statistics_session_testpersoon_D(self):
        session_id = 11
        datetime_from_session, datetime_to_session = self.dasession.get_dates_session(session_id)

        activities,manual_log_testpersoon_D = Manual_log.get_manual_log_testpersoon_D_programms_and_extra_info()
        activities_userstate,manual_log_testpersoon_D_userstate = Manual_log.get_manual_log_testpersoon_D_userstates()

        datetime_from = manual_log_testpersoon_D[0][0]
        datetime_to = manual_log_testpersoon_D[len(manual_log_testpersoon_D) - 1][1]
        mindwave_data_list = Mindwave_data_processing.get_mindwave_data_filtered_smoothed_middle_moving_median(datetime_from,datetime_to,self.window_mindwave)

        list_dates = self.rescuetimeDataProcessing.get_dates_list(datetime_from_session, datetime_to_session)

        activities_important = ["pdf + toledovragen","powerpoint","wikipedia","toledovragen", "pdf"]

        # With important activities
        result_x_avg, result_y_avg = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.AVG)
        result_x_std, result_y_std = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities_important[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg = ResultTuple(result_x_avg, result_y_avg)
        resultTuple_std = ResultTuple(result_x_std, result_y_std)
        for i in range(1,len(activities_important)):
            result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.AVG)
            result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities_important[i],Calculate_statistics_enumeration.STD)
            resultTuple_avg.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
            resultTuple_std.merge(ResultTuple(result_x_std_temp,result_y_std_temp))

        result_x_diff, result_y_diff =  self.manualLogDataProcessing.get_list_concentration_differences_manual_log(manual_log_testpersoon_D,mindwave_data_list)

        # ////////////////////////////
        # /// with all activities ////
        # ////////////////////////////
        result_x_avg_all_act, result_y_avg_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities[0],Calculate_statistics_enumeration.AVG)
        result_x_std_all_act, result_y_std_all_act = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities[0],Calculate_statistics_enumeration.STD)

        resultTuple_avg_all_act = ResultTuple(result_x_avg_all_act, result_y_avg_all_act)
        resultTuple_std_all_act = ResultTuple(result_x_std_all_act, result_y_std_all_act)
        for i in range(1,len(activities)):
            try:
                result_x_avg_temp, result_y_avg_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities[i],Calculate_statistics_enumeration.AVG)
                result_x_std_temp, result_y_std_temp = self.manualLogDataProcessing.get_list_concentration_time_spent_activity(manual_log_testpersoon_D,mindwave_data_list,activities[i],Calculate_statistics_enumeration.STD)
                resultTuple_avg_all_act.merge(ResultTuple(result_x_avg_temp,result_y_avg_temp))
                resultTuple_std_all_act.merge(ResultTuple(result_x_std_temp,result_y_std_temp))
            except:
                pass


        # ////////////////////////////
        result_x_amount_avg, result_y_amount_avg = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_D,list_dates,Calculate_statistics_enumeration.AVG)
        result_x_amount_std, result_y_amount_std = self.manualLogDataProcessing.get_list_amount_used_programs_concentration_per_interval(mindwave_data_list,manual_log_testpersoon_D,list_dates,Calculate_statistics_enumeration.STD)

        result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.AVG)
        result_x_std_rescuetime_amount, result_y_std_rescuetime_amount = self.get_list_amount_activities_RescueTime_interval_with_mindwave(session_id,Calculate_statistics_enumeration.STD)

        result_x_avg_userstate, result_y_avg_userstate = self.manualLogDataProcessing.get_statistics_attention_userstates(activities_userstate,manual_log_testpersoon_D_userstate,mindwave_data_list,Calculate_statistics_enumeration.AVG)
        result_x_std_userstate, result_y_std_userstate = self.manualLogDataProcessing.get_statistics_attention_userstates(activities_userstate,manual_log_testpersoon_D_userstate,mindwave_data_list,Calculate_statistics_enumeration.STD)

        resultTuple_diff = ResultTuple(result_x_diff, result_y_diff)

        resultTuple_amount_avg = ResultTuple(result_x_amount_avg, result_y_amount_avg)
        resultTuple_amount_std = ResultTuple(result_x_amount_std, result_y_amount_std)

        resultTuple_avg_rescuetime_amount = ResultTuple(result_x_avg_rescuetime_amount, result_y_avg_rescuetime_amount)
        resultTuple_std_rescuetime_amount = ResultTuple(result_x_std_rescuetime_amount, result_y_std_rescuetime_amount)

        resultTuple_avg_userstate = ResultTuple(result_x_avg_userstate,result_y_avg_userstate)
        resultTuple_std_userstate = ResultTuple(result_x_std_userstate,result_y_std_userstate)

        filename = self.folder + "data_analysis_results/testpersoon_D/"
        self.generate_csv("Time_spent_seconds","Concentration avg",resultTuple_avg,filename + "comparison time_spent_sec against average concentration")
        self.generate_csv("Time_spent_seconds","Concentration std",resultTuple_std,filename + "comparison time_spent_sec against std concentration")

        # //////////////////////
        # /// all activities ///
        # //////////////////////
        self.generate_csv("Time_spent_seconds","Concentration avg",resultTuple_avg_all_act,filename + "comparison time_spent_sec against average concentration all activities")
        self.generate_csv("Time_spent_seconds","Concentration std",resultTuple_std_all_act,filename + "comparison time_spent_sec against std concentration all activities")
        # //////////////////////


        self.generate_csv("Unknown","Concentration std",resultTuple_diff,filename + "comparison concentration difference when switch between activities")

        self.generate_csv("Amount","Concentration avg",resultTuple_amount_avg,filename + "comparison amount used programs with avg concentration")
        self.generate_csv("Amount","Concentration std",resultTuple_amount_std,filename + "comparison amount used programs with std concentration")

        self.generate_csv("Amount","Concentration avg",resultTuple_avg_rescuetime_amount,filename + "comparision RescueTime amount concentration avg")
        self.generate_csv("Amount","Concentration std",resultTuple_std_rescuetime_amount,filename + "comparision RescueTime amount concentration std")



        self.generate_csv("Userstate","Concentration avg",resultTuple_avg_userstate,filename + "comparision userstates concentration avg")
        self.generate_csv("Amount","Concentration std",resultTuple_std_userstate,filename + "comparision userstates concentration std")


        resultObject = ResultObject()
        resultObject.set_result_timeSpent_activity_avg(resultTuple_avg)
        resultObject.set_result_timeSpent_activity_std(resultTuple_std)

        resultObject.set_concentration_diff_activity_switch_avg(resultTuple_diff)

        resultObject.set_result_amount_used_programs_avg(resultTuple_amount_avg)
        resultObject.set_result_amount_used_programs_std(resultTuple_amount_std)

        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_avg(resultTuple_avg_rescuetime_amount)
        resultObject.set_amount_activities_RescueTime_interval_with_mindwave_std(resultTuple_std_rescuetime_amount)

        return resultObject

    def get_merged_results(self):
        resultObject_testpersoon_B = self.get_statistics_session_testpersoon_B()
        resultObject_testpersoon_A = self.get_statistics_session_testpersoon_A()
        resultObject_testpersoon_C = self.get_statistics_session_testpersoon_C()

        resultObject_testpersoon_B.merge(resultObject_testpersoon_A)

        filename = "data_analysis_results/merged/"
        self.generate_csv("Time_spent_sec","Concentration avg",resultObject_testpersoon_B.result_timeSpent_activity_avg,filename + "comparison time_spent_sec against average concentration")
        self.generate_csv("Time_spent_sec","Concentration std",resultObject_testpersoon_B.result_timeSpent_activity_std, filename + "comparison time_spent_sec against std concentration")

        self.generate_csv("Switch ID","Concentration avg",resultObject_testpersoon_B.result_concentration_diff_activity_switch_avg,filename + "comparison concentration difference when switch between activities")

        self.generate_csv("Switch ID","Concentration avg",resultObject_testpersoon_B.result_concentration_diff_specific_switch_avg,filename + "comparison concentration difference specific switch between activities")

        self.generate_csv("Amount","Concentration avg",resultObject_testpersoon_B.result_amount_used_programs_avg,filename + "comparison amount used programs with avg concentration")
        self.generate_csv("Amount","Concentration std",resultObject_testpersoon_B.result_amount_used_programs_std,filename + "comparison amount used programs with std concentration")

        self.generate_csv("Amount","Concentration avg",resultObject_testpersoon_B.amount_activities_RescueTime_interval_with_mindwave_avg,filename + "comparision RescueTime amount concentration avg")
        self.generate_csv("Amount","Concentration std",resultObject_testpersoon_B.amount_activities_RescueTime_interval_with_mindwave_avg,filename + "comparision RescueTime amount concentration std")

        return resultObject_testpersoon_B



    def get_list_amount_activities_RescueTime_interval_with_mindwave(self,session_id,statistic_type):
        result_x = []
        result_y = []

        datetime_from_session, datetime_to_session = self.dasession.get_dates_session(session_id)
        list_dates = self.rescuetimeDataProcessing.get_dates_list(datetime_from_session, datetime_to_session)
        mindwave_data_list = Mindwave_data_processing.get_mindwave_data_filtered_smoothed(datetime_from_session,datetime_to_session,10)

        for interval in list_dates:
            rescueTime_data = self.darescuetime.get_data_specific_period(interval[0], interval[1])
            result_x.append(len(rescueTime_data))
            sublist = Mindwave_data_processing.get_sublist(mindwave_data_list,datetime_from_session,datetime_to_session)
            if statistic_type == Calculate_statistics_enumeration.AVG:
                attention, meditation = Mindwave_data_processing.calculate_avg_attention_meditation(sublist)
            elif statistic_type == Calculate_statistics_enumeration.STD:
                attention, meditation = Mindwave_data_processing.calculate_std_attention_meditation(sublist)
            else:
                raise Exception.UnknownID("The statistic_type is unknown")
            result_y.append(attention)
        print "rescuetime amount"
        print "result_x"
        print result_x
        print "result_y"
        print result_y
        return result_x, result_y


    def generate_csv(self,label_x,label_y,resultTuple, filename):
        result = ""
        result += label_x + "," + label_y + "\n"
        for i in range(0,len(resultTuple.result_x)):
            result += str(resultTuple.result_x[i]) + "," + str(resultTuple.result_y[i]) + "\n"

        result_page = open(filename + ".csv","wb")
        result_page.write(result)
        result_page.close()
        print str(filename + ".csv generated successfully")

class ResultObject():
    result_timeSpent_activity_avg = None
    result_timeSpent_activity_std = None

    result_concentration_diff_activity_switch_avg = None

    result_concentration_diff_specific_switch_avg = None

    result_amount_used_programs_avg = None
    result_amount_used_programs_std = None

    amount_activities_RescueTime_interval_with_mindwave_avg = None
    amount_activities_RescueTime_interval_with_mindwave_std = None


    def set_result_timeSpent_activity_avg(self,result_timeSpent_activity_avg):
        self.result_timeSpent_activity_avg = result_timeSpent_activity_avg
    def set_result_timeSpent_activity_std(self,result_timeSpent_activity_std):
        self.result_timeSpent_activity_std = result_timeSpent_activity_std

    def set_concentration_diff_activity_switch_avg(self,result_concentration_diff_switch_avg):
        self.result_concentration_diff_activity_switch_avg = result_concentration_diff_switch_avg

    def set_concentration_diff_specific_activity_switch_avg(self,result_concentration_diff_specific_switch_avg):
        self.result_concentration_diff_specific_switch_avg = result_concentration_diff_specific_switch_avg

    def set_result_amount_used_programs_avg(self,result_amount_used_programs_avg):
        self.result_amount_used_programs_avg  = result_amount_used_programs_avg
    def set_result_amount_used_programs_std(self,result_amount_used_programs_std):
        self.result_amount_used_programs_std = result_amount_used_programs_std

    def set_amount_activities_RescueTime_interval_with_mindwave_avg(self,amount_activities_RescueTime_interval_with_mindwave_avg):
        self.amount_activities_RescueTime_interval_with_mindwave_avg = amount_activities_RescueTime_interval_with_mindwave_avg
    def set_amount_activities_RescueTime_interval_with_mindwave_std(self,amount_activities_RescueTime_interval_with_mindwave_std):
        self.amount_activities_RescueTime_interval_with_mindwave_std = amount_activities_RescueTime_interval_with_mindwave_std

    def merge(self,resultObjectB):
        if self.result_timeSpent_activity_avg is not None and resultObjectB.result_timeSpent_activity_avg is not None:
            self.result_timeSpent_activity_avg.result_x += resultObjectB.result_timeSpent_activity_avg.result_x
            self.result_timeSpent_activity_avg.result_y += resultObjectB.result_timeSpent_activity_avg.result_y

        if self.result_timeSpent_activity_std is not None and resultObjectB.result_timeSpent_activity_std is not None:
            self.result_timeSpent_activity_std.result_x += resultObjectB.result_timeSpent_activity_std.result_x
            self.result_timeSpent_activity_std.result_y += resultObjectB.result_timeSpent_activity_std.result_y

        if self.result_concentration_diff_activity_switch_avg is not None and resultObjectB.result_concentration_diff_activity_switch_avg is not None:
            self.result_concentration_diff_activity_switch_avg.result_x +=  resultObjectB.result_concentration_diff_activity_switch_avg.result_x
            self.result_concentration_diff_activity_switch_avg.result_y +=  resultObjectB.result_concentration_diff_activity_switch_avg.result_y

        if self.result_concentration_diff_specific_switch_avg is not None and resultObjectB.result_concentration_diff_specific_switch_avg is not None:
            self.result_concentration_diff_specific_switch_avg.result_x +=  resultObjectB.result_concentration_diff_specific_switch_avg.result_x
            self.result_concentration_diff_specific_switch_avg.result_y +=  resultObjectB.result_concentration_diff_specific_switch_avg.result_y


        if self.result_amount_used_programs_avg is not None and resultObjectB.result_amount_used_programs_avg is not None:
            self.result_amount_used_programs_avg.result_x += resultObjectB.result_amount_used_programs_avg.result_x
            self.result_amount_used_programs_avg.result_y += resultObjectB.result_amount_used_programs_avg.result_y
        if self.result_amount_used_programs_std is not None and resultObjectB.result_amount_used_programs_std is not None:
            self.result_amount_used_programs_std.result_x += resultObjectB.result_amount_used_programs_std.result_x
            self.result_amount_used_programs_std.result_y += resultObjectB.result_amount_used_programs_std.result_y

        if self.amount_activities_RescueTime_interval_with_mindwave_avg is not None and resultObjectB.amount_activities_RescueTime_interval_with_mindwave_avg is not None:
            self.amount_activities_RescueTime_interval_with_mindwave_avg.result_x += resultObjectB.amount_activities_RescueTime_interval_with_mindwave_avg.result_x
            self.amount_activities_RescueTime_interval_with_mindwave_avg.result_y += resultObjectB.amount_activities_RescueTime_interval_with_mindwave_avg.result_y
        if self.amount_activities_RescueTime_interval_with_mindwave_std is not None and resultObjectB.amount_activities_RescueTime_interval_with_mindwave_std is not None:
            self.amount_activities_RescueTime_interval_with_mindwave_std.result_x += resultObjectB.amount_activities_RescueTime_interval_with_mindwave_std.result_x
            self.amount_activities_RescueTime_interval_with_mindwave_std.result_y += resultObjectB.amount_activities_RescueTime_interval_with_mindwave_std.result_y

class ResultTuple():
    result_x = None
    result_y = None
    label = ""
    def __init__(self,result_x, result_y):
        self.result_x = result_x
        self.result_y = result_y

    def set_label(self,label):
        self.label = label

    def merge(self, resultTupleB):
        self.result_x += resultTupleB.result_x
        self.result_y += resultTupleB.result_y

