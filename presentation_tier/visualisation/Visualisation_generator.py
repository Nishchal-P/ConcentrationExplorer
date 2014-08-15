import datetime
from matplotlib.dates import date2num
from matplotlib import pyplot as plt
import numpy as np
import pylab

from data_tier import DAMindwave_SQLite
from data_tier import DASession_SQLite
from data_tier import DARescueTime_SQLite
from exception import Exception
from logical_tier import Data_processing
from logical_tier import List_operations
from logical_tier.userfeedback import Userfeedback_processing
import Convert_to_barchart_data
from logical_tier.mindwave import Mindwave_data_processing


__author__ = 'Peter'
class Visualisations():
    window_median = 5
    window_RescueTime = 150
    window_other = 10
    treshold_poorSignalMindwave = 0
    treshold_time_sec = 120
    link_to_main = ''
    daRescueTime = None
    daSession = None
    barchartdata_converter = None
    def __init__(self,link_to_main):
        self.link_to_main = link_to_main
        self.daRescueTime = DARescueTime_SQLite.RescueTime(self.link_to_main)
        self.daSession = DASession_SQLite.DASession(self.link_to_main)
        self.barchartdata_converter = Convert_to_barchart_data.ConvertToBarchartData(self.daRescueTime,self.daSession)


    def mindwave_data(self,session_id):

        datetime_from, datetime_to = self.daSession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation = self.get_mindwave_data(datetime_from, datetime_to)

        title = "session_ID: " + str(session_id) + " mindwave data"
        self.plot_data(attention_data, x, y_attention, y_meditation,None,None,None,title)


        #for item in list_mindwave_data:
        #    attention_data.append(item[3])
        #    meditation_data.append(item[4])
    def mindwave_data_raw(self,session_id):

        datetime_from, datetime_to = self.daSession.get_dates_session(session_id)
        attention_data, x, y_attention, y_meditation = self.get_mindwave_data_raw(datetime_from, datetime_to)

        title = "session_ID: " + str(session_id) + " mindwave data raw"
        self.plot_data(attention_data, x, y_attention, y_meditation,None,None,None,title)

    def get_mindwave_data(self, datetime_from, datetime_to,window_moving_average):
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

            if list_mindwave_data[index][5] == self.treshold_poorSignalMindwave:
                attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
                meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
            else:
                attention_data.append((datetime_from_mindwave,-1))
                meditation_data.append((datetime_from_mindwave,-1))

            index += 1
        x = [date2num(date) for (date, value) in attention_data]
        y_attention = [value for (date, value) in attention_data]
        y_meditation = [value for (date, value) in meditation_data]

        y_attention = List_operations.filter_list(y_attention)
        y_meditation = List_operations.filter_list(y_meditation)

        y_attention = List_operations.moving_median(y_attention,self.window_median)
        y_meditation = List_operations.moving_median(y_meditation,self.window_median)

        y_attention = List_operations.movingaverage(y_attention, window_moving_average)
        y_meditation = List_operations.movingaverage(y_meditation, window_moving_average)

        return attention_data, x, y_attention, y_meditation

    def get_mindwave_data_raw(self, datetime_from, datetime_to):
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

    def get_mindwave_data_smoothened(self,datetime_from, datetime_to):
        list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from, datetime_to)
        attention_data = []
        meditation_data = []

        for item in list_mindwave_data:
            attention_data.append(item[3])
            meditation_data.append(item[4])
        attention_data = List_operations.filter_list(attention_data)
        meditation_data = List_operations.filter_list(meditation_data)

        attention_data = List_operations.moving_median(attention_data,self.window_median)
        meditation_data = List_operations.moving_median(meditation_data,self.window_median)

        attention_data = List_operations.movingaverage(attention_data, self.window_other)
        meditation_data = List_operations.movingaverage(meditation_data, self.window_other)
        list_mindwave_data_modified = []
        for i in range(0,len(list_mindwave_data)):
            row = []
            row.append(list_mindwave_data[i][0])
            row.append(list_mindwave_data[i][1])
            row.append(list_mindwave_data[i][2])
            row.append(attention_data[i])
            row.append(meditation_data[i])
            row.append(list_mindwave_data[i][5])
            row.append(list_mindwave_data[i][6])

            list_mindwave_data_modified.append(row)

        return list_mindwave_data_modified

    def get_mindwave_data_avg_per_manualLog_interval(self, list_manual_log):
        datetime_from = list_manual_log[0][0]
        datetime_to = list_manual_log[len(list_manual_log) - 1][1]

        list_mindwave_data = self.get_mindwave_data_smoothened(datetime_from, datetime_to)
        x_axis, attention_data, meditation_data = Mindwave_data_processing.convert_mindwave_data_to_manualLog_intervals(
            list_mindwave_data, list_manual_log)
        x_axis_converted = []
        attention_data_converted = []
        meditation_data_converted = []

        mindwave_data_converted = []
        for index in range(0, len(list_mindwave_data)):
            try:
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1],
                                                                    "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")

            try:
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2],
                                                                    "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")
            for index_m_c in range(0, len(x_axis)):
                if datetime_from_mindwave >= x_axis[index_m_c][0] and datetime_from_mindwave < x_axis[index_m_c][1]:
                    x_axis_converted.append(datetime_from_mindwave)
                    attention_data_converted.append(attention_data[index_m_c])
                    meditation_data_converted.append(meditation_data[index_m_c])
                    mindwave_data_converted.append([datetime_from_mindwave,datetime_to_mindwave,attention_data[index_m_c],meditation_data[index_m_c]])

        return mindwave_data_converted, x_axis_converted, attention_data_converted, meditation_data_converted

    def get_mindwave_data_avg_per_RescueTime_interval(self, datetime_from, datetime_to):
        #datetime_from, datetime_to = self.daSession.get_dates_session(session_id)
        list_mindwave_data = self.get_mindwave_data_smoothened(datetime_from, datetime_to)
        list_dates_Rescuetime = self.daRescueTime.get_dates(datetime_from, datetime_to)
        x_axis, attention_data, meditation_data = Mindwave_data_processing.convert_mindwave_data_to_RescueTime_intervals(
            list_mindwave_data, list_dates_Rescuetime)
        x_axis_converted = []
        attention_data_converted = []
        meditation_data_converted = []

        mindwave_data_converted = []
        for index in range(0, len(list_mindwave_data)):
            try:
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1],
                                                                    "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")

            try:
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2],
                                                                    "%Y-%m-%d %H:%M:%S.%f")
            except:
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")
            for index_m_c in range(0, len(x_axis)):
                if datetime_from_mindwave >= x_axis[index_m_c][0] and datetime_from_mindwave < x_axis[index_m_c][1]:
                    x_axis_converted.append(datetime_from_mindwave)
                    attention_data_converted.append(attention_data[index_m_c])
                    meditation_data_converted.append(meditation_data[index_m_c])
                    mindwave_data_converted.append([datetime_from_mindwave,datetime_to_mindwave,attention_data[index_m_c],meditation_data[index_m_c]])

        mindwave_data_specific_period = [mindwave_data_converted, x_axis_converted, attention_data_converted, meditation_data_converted]
        return mindwave_data_specific_period

    def show_barchart_activities_mindwave_avg(self,datetime_from, datetime_to):
        mindwave_data_specific_period = self.get_mindwave_data_avg_per_RescueTime_interval(datetime_from, datetime_to)
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_activities(datetime_from, datetime_to)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Activities RescueTime mindwave avg',mindwave_data_specific_period)

    def show_barchart_activities_mindwave_attention_avg(self,datetime_from, datetime_to):
        mindwave_data_specific_period = self.get_mindwave_data_avg_per_RescueTime_interval(datetime_from, datetime_to)
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_activities(datetime_from, datetime_to)
        self.generate_bar_chart_activities_attention_only(prepared_array,list_activities_color,list_dates,'Activities RescueTime mindwave attention only avg',mindwave_data_specific_period)

    def show_barchart_important_activities_mindwave_avg(self,datetime_from, datetime_to):
        mindwave_data_specific_period = self.get_mindwave_data_avg_per_RescueTime_interval(datetime_from, datetime_to)
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_important_activities(datetime_from, datetime_to)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Important activities RescueTime avg mindwave',mindwave_data_specific_period)

    def show_barchart_important_unimportant_mindwave_avg(self,datetime_from, datetime_to):
        mindwave_data_specific_period = self.get_mindwave_data_avg_per_RescueTime_interval(datetime_from, datetime_to)
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_important_unimportant_activities(datetime_from, datetime_to)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Important and unimportant activities avg mindwave',mindwave_data_specific_period)

    def show_barchart_activities(self,datetime_from, datetime_to):
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_activities(datetime_from, datetime_to)
        mindwave_data = self.get_mindwave_data(datetime_from, datetime_to,self.window_RescueTime)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Activities RescueTime',mindwave_data)

    def show_barchart_important_activities(self,datetime_from, datetime_to):
        mindwave_data = self.get_mindwave_data(datetime_from, datetime_to,self.window_RescueTime)
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_important_activities(datetime_from, datetime_to)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Important activities RescueTime',mindwave_data)

    def show_barchart_important_unimportant_mindwave(self,datetime_from, datetime_to):
        mindwave_data = self.get_mindwave_data(datetime_from, datetime_to,self.window_RescueTime)
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_important_unimportant_activities(datetime_from, datetime_to)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Important and unimportant activities',mindwave_data)

    """
    Subjects
    """
    def show_barchart_subjects_mindwave_avg(self,datetime_from, datetime_to):
        mindwave_data_specific_period = self.get_mindwave_data_avg_per_RescueTime_interval(datetime_from, datetime_to)
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_subjects(datetime_from, datetime_to)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Subjects RescueTime avg',mindwave_data_specific_period)

    def show_barchart_subjects(self,datetime_from, datetime_to):
        prepared_array,list_activities_color,list_dates = self.barchartdata_converter.prepare_bar_chart_subjects(datetime_from, datetime_to)
        mindwave_data = self.get_mindwave_data(datetime_from, datetime_to,self.window_RescueTime)
        self.generate_bar_chart_activities(prepared_array,list_activities_color,list_dates,'Subjects RescueTime',mindwave_data)



    def convert_datetime_to_time_label(self, datetime_from):
        if datetime_from.hour < 10:
            from_hour = "0" + str(datetime_from.hour)
        else:
            from_hour = str(datetime_from.hour)

        if datetime_from.minute < 10:
            from_minute = "0" + str(datetime_from.minute)
        else:
            from_minute = str(datetime_from.minute)

        if datetime_from.second < 10:
            from_second = "0" + str(datetime_from.second)
        else:
            from_second = str(datetime_from.second)

        str_time_from = str(from_hour) + ":" + str(from_minute) + ":" + str(from_second)
        return str_time_from

    """
    @param prepared_array,list_activities_color,list_dates
    @effect generate barchart met gegevens rescueTime + mindwave
    """
    def generate_bar_chart_activities(self,prepared_array,list_activities_color,list_dates,title,mindwave_data):
        #mindwave plot data

        attention_data, x, y_attention, y_meditation = mindwave_data

        # x wordt geconverteerd omdat bar integers verwacht, dus om bar en plot te combineren kan er beter met integers gewerkt worden.
        # Tenslotte worden achteraf de labels van de bars er manueel opgezet.
        # x_converted komt overeen met het aantal seconden vanaf de eerste gemeten mindwave sample van die sessie
        x_converted = []
        start_Datetime_x_converted = attention_data[0][0]

        for i in range(0,len(attention_data)):
            value = attention_data[i][0] - start_Datetime_x_converted
            x_converted.append(int(value.seconds))
        """
        for i in range(0,len(x)):
            x_converted.append(i)
        """
        # barchart data RescueTime
        #prepared_array,list_activities_color,list_dates = self.prepare_bar_chart_activities(session_id)

        # voorbereiding graph
        fig = plt.figure(title)
        ax = fig.gca()
        N = len(prepared_array[0])
        ind =  np.zeros(N)
        ind[0] = 1
        width = np.zeros(N)
        index_ind = 0
        index_width = 0
        for date in list_dates:

            if index_ind >0:
                start_datetime = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
                difference = start_datetime - start_Datetime_x_converted
                ind[index_ind] = difference.seconds

                width[index_width] = ind[index_ind] - ind[index_ind - 1]
                index_width += 1
            index_ind += 1

        start_datetime = datetime.datetime.strptime(list_dates[len(list_dates) - 1][0], "%Y-%m-%d %H:%M:%S")
        end_datetime = start_datetime + datetime.timedelta(minutes=5)
        difference = end_datetime - start_datetime

        width[len(width) - 1] = difference.seconds

        # p_array opvullen
        p_array = []
        p_array.append(ax.bar(ind,prepared_array[0],width,color=list_activities_color[0][1]))
        bottom_array = prepared_array[0]
        for i in range(1,len(prepared_array)):
            p_array.append(ax.bar(ind,prepared_array[i],width,color=list_activities_color[i][1],bottom = bottom_array))
            bottom_array = self.sum_array(bottom_array,prepared_array[i])

        x_labels = []
        for item in list_dates:
            datetime_from = datetime.datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S")
            datetime_to =  datetime_from + datetime.timedelta(seconds=300)

            str_time_from = self.convert_datetime_to_time_label(datetime_from)
            str_time_to = self.convert_datetime_to_time_label(datetime_to)

            x_labels.append(str(str_time_from + " - " + str_time_to))


        ax.plot(x_converted,y_attention,'r-o')
        ax.plot(x_converted,y_meditation,'y-o')
        legend_labels = []
        for item in list_activities_color:
            legend_labels.append(item[0][0])

        legend = []
        for item in p_array:
            legend.append(item[0])
        plt.yticks(np.arange(0,1.1,0.1))
        plt.ylabel('percentage')
        plt.xlabel('RescueTime intervals')
        plt.title(title)
        lenInd = len(ind)
        if lenInd > 10:
            plt.xticks(ind+width/2., x_labels,rotation='vertical' )
        else:
            plt.xticks(ind+width/2., x_labels)
        #plt.xticks(ind+width/2., x_labels)
        plt.yticks(np.arange(0,1.1,0.1))

        figLegend = pylab.figure(str("Legend of: " + title))
        figLegend.legend( legend, legend_labels )
        figLegend.show()

        plt.legend( legend, legend_labels)
        figure = plt.gcf() # get current figure
        figure.set_size_inches(40, 15)
        plt.savefig(str('test_images/' + title + ".png"))


    """
    @param prepared_array,list_activities_color,list_dates
    @effect generate barchart met gegevens rescueTime + mindwave
    """
    def generate_bar_chart_activities_attention_only(self,prepared_array,list_activities_color,list_dates,title,mindwave_data):
        #mindwave plot data

        attention_data, x, y_attention, y_meditation = mindwave_data

        # x wordt geconverteerd omdat bar integers verwacht, dus om bar en plot te combineren kan er beter met integers gewerkt worden.
        # Tenslotte worden achteraf de labels van de bars er manueel opgezet.
        x_converted = []
        start_Datetime_x_converted = attention_data[0][0]

        for i in range(0,len(attention_data)):
            value = attention_data[i][0] - start_Datetime_x_converted
            x_converted.append(int(value.seconds))
        """
        for i in range(0,len(x)):
            x_converted.append(i)
        """
        # barchart data RescueTime
        #prepared_array,list_activities_color,list_dates = self.prepare_bar_chart_activities(session_id)

        # voorbereiding graph
        fig = plt.figure(title)
        ax = fig.gca()
        N = len(prepared_array[0])
        ind =  np.zeros(N)
        ind[0] = 1
        width = np.zeros(N)
        index_ind = 0
        index_width = 0
        for date in list_dates:

            if index_ind >0:
                start_datetime = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
                difference = start_datetime - start_Datetime_x_converted
                ind[index_ind] = difference.seconds

                width[index_width] = ind[index_ind] - ind[index_ind - 1]
                index_width += 1
            index_ind += 1

        start_datetime = datetime.datetime.strptime(list_dates[len(list_dates) - 1][0], "%Y-%m-%d %H:%M:%S")
        end_datetime = start_datetime + datetime.timedelta(minutes=5)
        difference = end_datetime - start_datetime

        width[len(width) - 1] = difference.seconds

        # calculate std
        attention_std = []
        #meditation_std = []
        for i in range(1,len(ind)):
            attention_std.append(List_operations.calculate_std(y_attention[int(ind[i - 1]) : int(ind[i])]))
         #   meditation_std.append(list_operations.calculate_std(y_meditation[ind[i - 1] : ind[i]]))
        attention_std.append(List_operations.calculate_std(y_attention[int(ind[N - 1]) : x_converted[int(len(x_converted) - 1)]]))


        # p_array opvullen
        p_array = []
        p_array.append(ax.bar(ind,prepared_array[0],width,color=list_activities_color[0][1]))
        bottom_array = prepared_array[0]
        for i in range(1,len(prepared_array)):
            if i == len(prepared_array) - 1:
                p_array.append(ax.bar(ind,prepared_array[i],width,color=list_activities_color[i][1],yerr=attention_std,bottom = bottom_array))
            else:
                p_array.append(ax.bar(ind,prepared_array[i],width,color=list_activities_color[i][1],bottom = bottom_array))
            bottom_array = self.sum_array(bottom_array,prepared_array[i])

        x_labels = []
        for item in list_dates:
            datetime_from = datetime.datetime.strptime(item[0], "%Y-%m-%d %H:%M:%S")
            datetime_to =  datetime_from + datetime.timedelta(seconds=300)

            str_time_from = str(datetime_from.hour) + ":" + str(datetime_from.minute) + ":" + str(datetime_from.second)
            str_time_to = str(datetime_to.hour) + ":" + str(datetime_to.minute) + ":" + str(datetime_to.second)

            x_labels.append(str(str_time_from + " - " + str_time_to))


        ax.plot(x_converted,y_attention,'r-o')
        #ax.plot(x_converted,y_meditation,'y-o')
        legend_labels = []
        for item in list_activities_color:
            legend_labels.append(item[0][0])

        legend = []
        for item in p_array:
            legend.append(item[0])

        plt.ylabel('percentage')
        plt.xlabel('RescueTime intervals')
        plt.title(title)
        lenInd = len(ind)
        if lenInd > 10:
            plt.xticks(ind+width/2., x_labels,rotation='vertical' )
        else:
            plt.xticks(ind+width/2., x_labels)

        plt.yticks(np.arange(0,1.1,0.1))
        figLegend = pylab.figure()
        figLegend.legend( legend, legend_labels )
        figLegend.show()
        figure = plt.gcf() # get current figure
        figure.set_size_inches(40, 15)
        plt.savefig(str('test_images/' + title + ".png"))

    """
    @param session_id,prepared_array,list_activities_color,list_dates
    @param manual_log | [datetime_from, datetime_to, description]
    @effect generate barchart met gegevens manual log + mindwave
    """
    def generate_bar_chart_activities_manual_log(self,title,mindwave_data,manual_log):
        #mindwave plot data

        attention_data, x, y_attention, y_meditation = mindwave_data
        list_activities_color = []
        unique_activities = List_operations.get_1D_list_from_2D_doubles_removed(manual_log,2)
        list_unique_activities_color = self.barchartdata_converter.get_list_activities_color(unique_activities)



        # x wordt geconverteerd omdat bar integers verwacht, dus om bar en plot te combineren kan er beter met integers gewerkt worden.
        # Tenslotte worden achteraf de labels van de bars er manueel opgezet.
        x_converted = []
        start_Datetime_x_converted = attention_data[0][0]

        for i in range(0,len(attention_data)):
            value = attention_data[i][0] - start_Datetime_x_converted
            x_converted.append(int(value.seconds))
        """
        for i in range(0,len(x)):
            x_converted.append(i)
        """

        # barchart data RescueTime
        #prepared_array,list_activities_color,list_dates = self.prepare_bar_chart_activities(session_id)

        # voorbereiding graph
        fig = plt.figure(title)
        ax = fig.gca()
        N = len(manual_log)
        ind =  np.zeros(N)

        index_ind = 0
        index_l = 0

        for index_m in range(0,len(attention_data)):
            try:
                datetime_from_attention_data = datetime.datetime(attention_data[index_m][0].year,attention_data[index_m][0].month,attention_data[index_m][0].day,attention_data[index_m][0].hour,attention_data[index_m][0].minute,attention_data[index_m][0].second)
            except Exception,e:
                datetime_from_attention_data =  attention_data[index_m][0]

            if datetime_from_attention_data >= manual_log[index_l][0] and datetime_from_attention_data < manual_log[index_l][1]:
                ind[index_ind] = x_converted[index_m]
                index_ind += 1
                index_l += 1
            else:
                if index_l < len(manual_log) - 1:
                    if datetime_from_attention_data >= manual_log[index_l + 1][0] and datetime_from_attention_data < manual_log[index_l + 1][1]:
                        #index_l += 1
                        manual_log = List_operations.delete_entry(manual_log,index_l)
                        N -= 1
                        ind = np.delete(ind,N - 1)
                        ind[index_ind] = x_converted[index_m]
                        index_ind += 1
                        index_l += 1

            if index_ind >= len(ind) or index_l >= len(manual_log):
                break


        for item in manual_log:
            for activity in list_unique_activities_color:
                if item[2] == activity[0]:
                    list_activities_color.append([item[2],activity[1]])
                    break

        #width = ind[1:len(ind)] + [x_converted[len(x_converted) - 1] - ind[len(ind) - 1]]       # the width of the bars: can also be len(x) sequence
        width = np.zeros(N)

        for i in range (0,len(ind) - 1):
            width[i] = ind[i + 1] - ind[i]
        width[N - 1] = (x_converted[len(x_converted) - 1] - ind[len(ind) - 1])

        # p_array opvullen
        p_array = []
        p_array_for_legend = []
        height_array = []
        for i in range(0,N):
            height_array.append(np.zeros(N))
            height_array[i][i] = 1

        list_activities_temp = []
        list_unique_activities_color = []
        for i in range(1,N):
            ax_bar = ax.bar(ind, height_array[i], width[i], color=list_activities_color[i][1])
            p_array.append(ax_bar)
            if list_activities_color[i][0] not in list_activities_temp:
                p_array_for_legend.append(ax_bar)
                list_activities_temp.append(list_activities_color[i][0])
                list_unique_activities_color.append(list_activities_color[i])


        x_labels = []
        for item in manual_log:
            datetime_from = item[0]
            datetime_to = item[1]

            str_time_from = str(datetime_from.hour) + ":" + str(datetime_from.minute) + ":" + str(datetime_from.second)
            str_time_to = str(datetime_to.hour) + ":" + str(datetime_to.minute) + ":" + str(datetime_to.second)

            x_labels.append(str(str_time_from + " - " + str_time_to))


        ax.plot(x_converted,y_attention,'r-o')
        ax.plot(x_converted,y_meditation,'y-o')
        legend_labels = []
        for item in list_unique_activities_color:
            legend_labels.append(item[0])

        legend = []
        for item in p_array_for_legend:
            legend.append(item[0])

        plt.ylabel('percentage')
        plt.title(title)
        lenInd = len(ind)
        if lenInd > 10:
            plt.xticks(ind+width/2., x_labels,rotation='vertical' )
        else:
            plt.xticks(ind+width/2., x_labels)

        plt.yticks(np.arange(0,1.1,0.1))
        plt.legend( legend, legend_labels )

        figure = plt.gcf() # get current figure
        figure.set_size_inches(80, 15)
        plt.savefig(str('test_images/' + "manual_log" + ".png"))



    def sum_array(self,array_1,array_2):
       if len(array_1) != len(array_2):
           raise Exception.message('both input arrays should be of the same size')
       result = []
       for i in range(0,len(array_1)):
           result.append(array_1[i] + array_2[i])
       return result


    def show_barchart_important_activity_details(self,date_time_from, date_time_to,options_reason):
        result_list = Data_processing.getListImportantActivities(date_time_from,date_time_to,options_reason)
        list_time = []
        list_eyes_detected =[]
        list_user_feedback = []
        list_attention_mindwave = []
        list_meditation_mindwave = []
        total_time = 0.0

        for item in result_list:
            total_time += item[1]

        x = []
        for item in result_list:
            # item = [activity, time_sec, avg_concentration_user, avg_eyes_detected, [userGone],avg_attention_mindwave, avg_meditation_mindwave]
            list_time.append(round((float(item[1]) / total_time * 100.0),0))
            list_user_feedback.append(round(item[2] * 100,0))
            list_eyes_detected.append(round(item[3] * 100,0))
            list_attention_mindwave.append(round(item[5] * 100,0))
            list_meditation_mindwave.append(round(item[6] * 100,0))
            x.append(item[0])

        N = len(result_list)

        ind = np.arange(N)  # the x locations for the groups
        width = 0.15       # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(ind, list_time, width, color='c')
        rects2 = ax.bar(ind + width, list_user_feedback, width, color='g')
        rects3 = ax.bar(ind + (2.0 * width), list_eyes_detected, width, color='b')
        rects4 = ax.bar(ind + (3.0 * width), list_attention_mindwave, width, color='r')
        rects5 = ax.bar(ind + (4.0 * width), list_meditation_mindwave, width, color='y')

        # add some
        ax.set_ylabel('percentage')
        ax.set_title('Attention + Meditation')
        ax.set_xticks(ind+width)
        ax.set_xticklabels( x )

        ax.legend( (rects1[0], rects2[0],rects3[0],rects4[0],rects5[0]), ('Relative time spent', 'Average user indicated concentration','Average eyes detected', 'Average attention mindwave','Average meditation mindwave') )
        self.autolabel(rects1,ax)
        self.autolabel(rects2,ax)
        self.autolabel(rects3,ax)
        self.autolabel(rects4,ax)
        self.autolabel(rects5,ax)


    def show_graph_attention_data_mindwave(self,datetime_from, datetime_to):
        list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from,datetime_to)
        attention_data = []
        meditation_data = []
        x = []
        index = 0
        while index < len(list_mindwave_data):

            try:
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
            except :
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")

            try:
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
            except :
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")

            if list_mindwave_data[index][5] <= self.treshold_poorSignalMindwave:
                attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
                meditation_data.append((datetime_from_mindwave,list_mindwave_data[index][4]))
            else:
                attention_data.append((datetime_from_mindwave,-1))
                meditation_data.append((datetime_from_mindwave,-1))
            #meditation_data.append((list_mindwave_data[index][1], list_mindwave_data[index][4]))
            index += 1

        x = [date2num(date) for (date, value) in attention_data]
        y_attention = [value for (date, value) in attention_data]
        y_meditation = [value for (date, value) in meditation_data]

        y_attention = List_operations.filter_list(y_attention)
        y_meditation = List_operations.filter_list(y_meditation)


        y_attention = List_operations.moving_median(y_attention,self.window_median)
        y_meditation = List_operations.moving_median(y_meditation,self.window_median)



        y_attention = List_operations.movingaverage(y_attention, self.window_other)
        y_meditation = List_operations.movingaverage(y_meditation, self.window_other)


        fig = plt.figure("Line chart data mindwave headset")

        graph = fig.add_subplot(111)

        # Plot the data as a red line with round markers
        graph.plot(x,y_attention,'r-o')
        graph.plot(x,y_meditation,'y-o')

        # Set the xtick locations to correspond to just the dates you entered.
        graph.set_xticks(x)

        # Set the xtick labels to correspond to just the dates you entered.
        graph.set_xticklabels(
                [date.strftime("%Y-%m-%d %H:%M:%S") for (date, value) in attention_data]
                )

        #for item in list_mindwave_data:
        #    attention_data.append(item[3])
        #    meditation_data.append(item[4])

    def show_barchart_attention_data_mindwave(self,datetime_from, datetime_to):
        list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from,datetime_to)
        attention_data = []
        meditation_data = []
        datums = []
        x = []
        index = 0
        while index < len(list_mindwave_data):
            attention_data.append(round(list_mindwave_data[index][3] * 100,0))
            meditation_data.append(round(list_mindwave_data[index][4] * 100,0))
            try:
                datums.append(datetime.datetime.strptime(list_mindwave_data[index][1],"%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S"))
            except :
                datums.append(datetime.datetime.strptime(list_mindwave_data[index][1],"%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"))
            index += 1

        N = len(list_mindwave_data)
        if N > 0:
            ind = np.arange(N)  # the x locations for the groups
            width = 0.35       # the width of the bars

            fig, ax = plt.subplots()
            rects1 = ax.bar(ind, attention_data, width, color='r')

            rects2 = ax.bar(ind+width, meditation_data, width, color='y')

            # add some

            ax.set_ylabel('Attention + meditation value')
            ax.set_title('Attention + Meditation')
            ax.set_xticks(ind+width)
            ax.set_xticklabels( datums )

            ax.legend( (rects1[0], rects2[0]), ('Attention', 'Meditation') )
            self.autolabel(rects1,ax)
            self.autolabel(rects2,ax)

    def show_graph_comparison_attention_data_mindwave_and_userfeedback(self,datetime_from, datetime_to):
        list_mindwave_data = DAMindwave_SQLite.get_data_specific_period(datetime_from,datetime_to)

        attention_data = []
        userfeedback_data = []
        x = []
        index = 0
        while index < len(list_mindwave_data):
            try:
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S.%f")
            except :
                datetime_from_mindwave = datetime.datetime.strptime(list_mindwave_data[index][1], "%Y-%m-%d %H:%M:%S")

            try:
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S.%f")
            except :
                datetime_to_mindwave = datetime.datetime.strptime(list_mindwave_data[index][2], "%Y-%m-%d %H:%M:%S")

            if list_mindwave_data[index][5] == self.treshold_poorSignalMindwave:
                attention_data.append((datetime_from_mindwave,list_mindwave_data[index][3]))
            else:
                attention_data.append((datetime_from_mindwave,-1))
            try:
                avg_userfeedback = Userfeedback_processing.get_average_userfeedback_specific_period(datetime_from_mindwave,datetime_to_mindwave)
            except Exception.ListEmpty:
                avg_userfeedback = -1
            userfeedback_data.append((datetime_from_mindwave,avg_userfeedback))
            index += 1

        x = [date2num(date) for (date, value) in attention_data]
        y_attention = [value for (date, value) in attention_data]
        y_attention = List_operations.movingaverage(y_attention,10)
        y_userfeedback = [value for (date, value) in userfeedback_data]



        y_attention = List_operations.filter_list(y_attention)
        y_userfeedback = List_operations.filter_list(y_userfeedback)

        y_attention = List_operations.moving_median(y_attention,self.window_median)

        y_attention = List_operations.movingaverage(y_attention, self.window_other)


        fig = plt.figure("Comparison attention mindwave headset and user indicated concentration")

        graph = fig.add_subplot(111)

        # Plot the data as a red line with round markers
        graph.plot(x,y_attention,'r-o')
        graph.plot(x,y_userfeedback,'b-o')

        # Set the xtick locations to correspond to just the dates you entered.
        graph.set_xticks(x)

        # Set the xtick labels to correspond to just the dates you entered.
        graph.set_xticklabels(
                [date.strftime("%Y-%m-%d %H:%M:%S") for (date, value) in attention_data]
                )

        #for item in list_mindwave_data:
        #    attention_data.append(item[3])
        #    meditation_data.append(item[4])

    def autolabel(self,rects,ax):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, height,
                    ha='center', va='bottom')






