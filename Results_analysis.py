import datetime

from matplotlib import pyplot as plt

from data_tier import DASession_SQLite
from data_tier import DARescueTime_SQLite
from for_data_analysis import Manual_log

from logical_tier.mindwave import Mindwave_data_processing
from presentation_tier.visualisation import Visualisation_generator
from presentation_tier import Output
from for_data_analysis import Manual_log_processing
from for_data_analysis import Calculate_statistics

class ResultAnalysis():
    window_median = 5
    window_RescueTime = 150
    window_other = 30
    treshold_poorSignalMindwave = 0
    treshold_time_sec = 120
    options_reason = [['Notes','I was taking notes',1], ['Document','I was searching/reading a document',1], ['Break','I took a break',0], ['Distracted','I was distracted',0],  ['Screen','I was looking to the screen',1],['Other','Other',0]]
    dasession = DASession_SQLite.DASession('')
    daRescueTime = DARescueTime_SQLite.RescueTime('')
    manualLogProcessing = Manual_log_processing.ManualLog_data_processing('')
    calculateStatistics = Calculate_statistics.CalculateStatistics('')

    x_label = "Date and time of each measured sample"
    y_label = "Concentration and meditation percentage"

    def __init__(self):
        """
        testpersoon_A
        """
        self.get_barchart_manual_log_testpersoon_A_userstates()
        self.get_barchart_manual_log_testpersoon_A_userstates_avg()
        self.get_barchart_manual_log_testpersoon_A()
        self.get_barchart_manual_log_testpersoon_A_only_programs_websites_avg()
        self.calculateStatistics.get_statistics_session_testpersoon_A()
        """
        testpersoon_B
        """
        self.get_barchart_manual_log_testpersoon_B()
        self.get_barchart_manual_log_testpersoon_B_avg()
        self.get_barchart_manual_log_testpersoon_B_only_programs_websites()
        self.get_barchart_manual_log_testpersoon_B_only_programs_websites_avg()
        self.calculateStatistics.get_statistics_session_testpersoon_B()

        """
        testpersoon_C

        self.get_barchart_manual_log_testpersoon_C()
        self.get_barchart_manual_log_testpersoon_C_activities_only()
        self.get_barchart_manual_log_testpersoon_C_userstates()
        self.get_barchart_manual_log_testpersoon_C_session_2()
        self.calculateStatistics.get_statistics_session_testpersoon_C()
        """

        """
        testpersoon_D
        self.get_barchart_manual_log_testpersoon_D()
        self.get_barchart_manual_log_testpersoon_D_programs_and_extra_info()
        self.get_barchart_manual_log_testpersoon_D_userstates()
        self.calculateStatistics.get_statistics_session_testpersoon_D()
        """


        """
        merged
        self.calculateStatistics.get_merged_results()
        """

        plt.show()

    def show_results(self,session_id):
        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        Output.show_results(datetime_from,datetime_to,self.options_reason,self.treshold_time_sec)

    def get_barchart_manual_log_testpersoon_A(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_testpersoon_A()
        datetime_from = manual_log_testpersoon_A[0][0]
        datetime_to = manual_log_testpersoon_A[len(manual_log_testpersoon_A) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,self.window_other)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_A",mindwave_data,manual_log_testpersoon_A)

    def get_barchart_manual_log_testpersoon_A_only_programs_websites(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_testpersoon_A_enkel_programmas_websites()
        datetime_from = manual_log_testpersoon_A[0][0]
        datetime_to = manual_log_testpersoon_A[len(manual_log_testpersoon_A) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_A activities only",mindwave_data,manual_log_testpersoon_A)

    def get_barchart_manual_log_testpersoon_A_only_programs_websites_avg(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_testpersoon_A_enkel_programmas_websites()
        datetime_from = manual_log_testpersoon_A[0][0]
        datetime_to = manual_log_testpersoon_A[len(manual_log_testpersoon_A) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data_avg_per_manualLog_interval(manual_log_testpersoon_A)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_A activities only avg",mindwave_data,manual_log_testpersoon_A)

    def get_barchart_manual_log_testpersoon_A_userstates(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_userstates_testpersoon_A()
        datetime_from = manual_log_testpersoon_A[0][0]
        datetime_to = manual_log_testpersoon_A[len(manual_log_testpersoon_A) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_A userstates",mindwave_data,manual_log_testpersoon_A)

    def get_barchart_manual_log_testpersoon_A_userstates_avg(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_userstates_testpersoon_A()
        datetime_from = manual_log_testpersoon_A[0][0]
        datetime_to = manual_log_testpersoon_A[len(manual_log_testpersoon_A) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data_avg_per_manualLog_interval(manual_log_testpersoon_A)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_A userstates avg",mindwave_data,manual_log_testpersoon_A)

    def get_barchart_manual_log_testpersoon_C(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_C = Manual_log.get_manual_logfile_testpersoon_C_session_1()
        #manual_log_testpersoon_C = manual_log.get_manual_logfile_per_column(manual_log_testpersoon_C,3)
        datetime_from = manual_log_testpersoon_C[0][0]
        datetime_to = manual_log_testpersoon_C[len(manual_log_testpersoon_C) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_C",mindwave_data,manual_log_testpersoon_C)


    def get_barchart_manual_log_testpersoon_D(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_D = Manual_log.get_manual_log_testpersoon_D()
        #manual_log_testpersoon_D = manual_log.get_manual_logfile_per_column(manual_log_testpersoon_D,3)
        datetime_from = manual_log_testpersoon_D[0][0]
        datetime_to = manual_log_testpersoon_D[len(manual_log_testpersoon_D) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_D",mindwave_data,manual_log_testpersoon_D)

    def get_barchart_manual_log_testpersoon_D_programs_and_extra_info(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_D = Manual_log.get_manual_log_testpersoon_D_programms_and_extra_info()
        #manual_log_testpersoon_D = manual_log.get_manual_logfile_per_column(manual_log_testpersoon_D,3)
        datetime_from = manual_log_testpersoon_D[0][0]
        datetime_to = manual_log_testpersoon_D[len(manual_log_testpersoon_D) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log programs with extra info visualised testpersoon_D",mindwave_data,manual_log_testpersoon_D)

    def get_barchart_manual_log_testpersoon_D_userstates(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_D = Manual_log.get_manual_log_testpersoon_D_userstates()
        #manual_log_testpersoon_D = manual_log.get_manual_logfile_per_column(manual_log_testpersoon_D,3)
        datetime_from = manual_log_testpersoon_D[0][0]
        datetime_to = manual_log_testpersoon_D[len(manual_log_testpersoon_D) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log programs with extra info visualised testpersoon_D",mindwave_data,manual_log_testpersoon_D)

    def get_barchart_manual_log_testpersoon_C_activities_only(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_C = Manual_log.get_manual_logfile_testpersoon_C_session_1_activities_only()
        #manual_log_testpersoon_C = manual_log.get_manual_logfile_per_column(manual_log_testpersoon_C,3)
        datetime_from = manual_log_testpersoon_C[0][0]
        datetime_to = manual_log_testpersoon_C[len(manual_log_testpersoon_C) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_C activities only",mindwave_data,manual_log_testpersoon_C)

    def get_barchart_manual_log_testpersoon_C_userstates(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_C = Manual_log.get_manual_logfile_testpersoon_C_session_1_userstates()
        #manual_log_testpersoon_C = manual_log.get_manual_logfile_per_column(manual_log_testpersoon_C,3)
        datetime_from = manual_log_testpersoon_C[0][0]
        datetime_to = manual_log_testpersoon_C[len(manual_log_testpersoon_C) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_C userstates",mindwave_data,manual_log_testpersoon_C)

    def get_barchart_manual_log_testpersoon_C_session_2(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_C = Manual_log.get_manual_logfile_testpersoon_C_session_2()
        datetime_from = manual_log_testpersoon_C[0][0]
        datetime_to = manual_log_testpersoon_C[len(manual_log_testpersoon_C) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_C session 2",mindwave_data,manual_log_testpersoon_C)

    def get_barchart_manual_log_testpersoon_B(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_bugs_verwijderd()
        datetime_from = manual_log_testpersoon_B[0][0]
        datetime_to = manual_log_testpersoon_B[len(manual_log_testpersoon_B) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_B",mindwave_data,manual_log_testpersoon_B)

    def get_barchart_manual_log_testpersoon_B_avg(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_bugs_verwijderd()
        datetime_from = manual_log_testpersoon_B[0][0]
        datetime_to = manual_log_testpersoon_B[len(manual_log_testpersoon_B) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data_avg_per_manualLog_interval(manual_log_testpersoon_B)
        #mindwave_data = visualisationGenerator.get_mindwave_data_raw(datetime_from, datetime_to)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_B avg",mindwave_data,manual_log_testpersoon_B)

    def get_barchart_manual_log_testpersoon_B_only_programs_websites_avg(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_enkel_programmas_websites()
        datetime_from = manual_log_testpersoon_B[0][0]
        datetime_to = manual_log_testpersoon_B[len(manual_log_testpersoon_B) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data_avg_per_manualLog_interval(manual_log_testpersoon_B)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised testpersoon_B programs/websites only avg",mindwave_data,manual_log_testpersoon_B)


    def get_barchart_manual_log_testpersoon_B_only_programs_websites(self):
        visualisationGenerator = Visualisation_generator.Visualisations('')

        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_enkel_programmas_websites()
        datetime_from = manual_log_testpersoon_B[0][0]
        datetime_to = manual_log_testpersoon_B[len(manual_log_testpersoon_B) - 1][1]

        mindwave_data = visualisationGenerator.get_mindwave_data(datetime_from, datetime_to,visualisationGenerator.window_other)
        visualisationGenerator.generate_bar_chart_activities_manual_log("manual log visualised programs/websites only testpersoon_B",mindwave_data,manual_log_testpersoon_B)


    def get_list_log_testpersoon_B(self):
        session_id = 41
        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        activities, result_list = Manual_log.get_manual_logfile_Testpersoon_B()
        print activities
        for item in activities:
            selected_activity = item
            attention_data, x, y_attention, y_meditation,y_selectedActivity = self.get_mindwave_manual_logged_activities_data(datetime_from,datetime_to,result_list,selected_activity)
            title = "session_ID: " + str(session_id) + "mindwave data manual logged for activity: " + str(selected_activity)
            self.plot_data(attention_data, x, y_attention, y_meditation,y_selectedActivity,None,None,title)
            #plt.figure(figsize=(8, 6))
            figure = plt.gcf() # get current figure
            figure.set_size_inches(40, 30)
            plt.savefig(str('test_images/' + selected_activity + ".png"))


    def mindwave_data(self,session_id):

        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation = Mindwave_data_processing.get_mindwave_data(datetime_from, datetime_to,self.window_other)

        title = "session_ID: " + str(session_id) + "mindwave data"

        self.plot_data(attention_data, x, y_attention, y_meditation,None,None,None,title, self.x_label, self.y_label)


        #for item in list_mindwave_data:
        #    attention_data.append(item[3])
        #    meditation_data.append(item[4])
    def mindwave_data_raw(self,session_id):

        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation = Mindwave_data_processing.get_mindwave_data_raw(datetime_from, datetime_to)

        title = "session_ID: " + str(session_id) + "mindwave data raw"
        self.plot_data(attention_data, x, y_attention, y_meditation,None,None,None,title, self.x_label, self.y_label)



    def mindwave_userfeedback_data_per_activity(self,session_id,activity):

        datetime_from, datetime_to = self.get_dates_session(session_id)

        activity_details = self.daRescueTime.gat_sum_time_secnds_specific_activity_with_treshold(datetime_from, datetime_to, activity)
        attention_data, x, y_attention, y_meditation,y_activityDuration = Mindwave_data_processing.get_mindwave_activity_data(datetime_from, datetime_to,activity_details,self.window_other)

        dates_activity = self.convert_activityDetailsList_to_datesList(activity_details)

        self.modify_per_dates(attention_data, y_attention,
                                 y_meditation,y_activityDuration,dates_activity)
        title = "session_ID: " + str(session_id) + "mindwave data for activity: " + str(activity)
        self.plot_data(attention_data, x, y_attention, y_meditation,y_activityDuration,None,None,title, self.x_label, self.y_label)


        #for item in list_mindwave_data:
        #    attention_data.append(item[3])
        #    meditation_data.append(item[4])

    def mindwave_userfeedback_data(self,session_id):

        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation,y_userfeedback = Mindwave_data_processing.get_mindwave_userfeedback_data(datetime_from, datetime_to,self.window_RescueTime)

        title = "mindwave data per user estimated concentration"
        self.plot_data(attention_data, x, y_attention, y_meditation,y_userfeedback,None,None,title, self.x_label, self.y_label)
        print str("function 'mindwave_userfeedback_data' for session_Id: " + str(session_id) + " completed")

        #for item in list_mindwave_data:
        #    attention_data.append(item[3])
        #    meditation_data.append(item[4])

    def mindwave_data_per_userGone(self,session_id):
        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation,y_userGoneNotStudying,y_userGoneStudying = Mindwave_data_processing.get_mindwave_userGone_data(datetime_from,datetime_to,self.window_other)

        title =  "session_ID: " + str(session_id) + "mindwave data for userGone"
        self.plot_data(attention_data, x, y_attention, y_meditation,None,y_userGoneNotStudying,y_userGoneStudying,title, self.x_label, self.y_label)

    def mindwave_data_per_worksession(self,session_id):
        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation,y_userGoneNotStudying,y_userGoneStudying = Mindwave_data_processing.get_mindwave_worksession_data(datetime_from,datetime_to,self.window_other)

        title =  "session_ID: " + str(session_id) + "mindwave data for worksession"
        self.plot_data(attention_data, x, y_attention, y_meditation,None,y_userGoneNotStudying,y_userGoneStudying,title, self.x_label, self.y_label)

    def mindwave_data_important_unimportant_activity(self,session_id):
        datetime_from, datetime_to = self.dasession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation,y_userGoneNotStudying,y_userGoneStudying = Mindwave_data_processing.get_mindwave_dataa_important_unimportant_activity(datetime_from,datetime_to,self.window_RescueTime)

        title = "mindwave data important / unimportant activities"
        self.plot_data(attention_data, x, y_attention, y_meditation,None,y_userGoneNotStudying,y_userGoneStudying,title, self.x_label, self.y_label)



    def convert_activityDetailsList_to_datesList(self, activity_details):
        dates_activity = []
        for activity_detail in activity_details:
            start_datetime = datetime.datetime.strptime(activity_detail[0], "%Y-%m-%d %H:%M:%S")
            end_datetime = start_datetime + datetime.timedelta(minutes=5)
            dates_activity.append([start_datetime, end_datetime])
        return dates_activity

    def convert_userGoneList_to_datesList(self, userGone):
        dates_userGone = []
        for activity_detail in userGone:
            try:
                start_datetime = datetime.datetime.strptime(activity_detail[1], "%Y-%m-%d %H:%M:%S.%f")
            except:
                start_datetime = datetime.datetime.strptime(activity_detail[1], "%Y-%m-%d %H:%M:%S")

            try:
                end_datetime = datetime.datetime.strptime(activity_detail[1], "%Y-%m-%d %H:%M:%S.%f")
            except:
                end_datetime = datetime.datetime.strptime(activity_detail[1], "%Y-%m-%d %H:%M:%S")

            dates_userGone.append([start_datetime, end_datetime])
        return dates_userGone

    def modify_per_dates(self, attention_data,  y_attention, y_meditation,y_activityDuration,dates_list):
        for i in range(0, len(attention_data)):
            hasImportantActivity = False
            for item_dates_activity in dates_list:
                if attention_data[i][0] >= item_dates_activity[0] and attention_data[i][0] <= item_dates_activity[1]:
                    hasImportantActivity = True
            if hasImportantActivity is False:
                #y_attention[i] = 0
                #y_meditation[i] = 0
                y_activityDuration[i] = 0

    def plot_data(self, attention_data, x, y_attention, y_meditation,y_userfeedback,y_userGoneNotStudying,y_userGoneStudying,title,x_axis_label, y_axis_label):
        fig = plt.figure(title)
        graph = fig.add_subplot(111)
        # Plot the data as a red line with round markers
        graph.plot(x, y_attention, 'r-o')
        graph.plot(x, y_meditation, 'y-o')
        if y_userfeedback != None:
            graph.plot(x, y_userfeedback, 'b-o')
        if y_userGoneNotStudying is not None:
            graph.plot(x, y_userGoneNotStudying, 'r-o')
        if y_userGoneStudying is not None:
            graph.plot(x, y_userGoneStudying, 'g-o')

        # Set the xtick locations to correspond to just the dates you entered.
        x_label_index_array,attention_data_reduced = self.calculate_x_x_ticks(x,5,attention_data)
        graph.set_xticks(x_label_index_array)
        # Set the xtick labels to correspond to just the dates you entered.
        graph.set_xticklabels(
            [date.strftime("%Y-%m-%d %H:%M:%S") for (date, value) in attention_data_reduced]
        )
        graph.set_xlabel(x_axis_label)
        graph.set_ylabel(y_axis_label)
        plt.ylim((0,1))

    def calculate_x_x_ticks(self,x,amount_of_desired_labels,attention_data):
        max = len(x)
        interval = round(int(float(max) / float(amount_of_desired_labels)))
        result = []
        result_attention = []
        for i in range(0,amount_of_desired_labels):
            index = int(i * interval)
            result.append(x[index])
            result_attention.append(attention_data[index])


        return result,result_attention
ResultAnalysis()
