__author__ = 'Peter'
import datetime
import random
import numpy as np

class ConvertToBarchartData():
    daSession = None
    daRescueTime = None
    def __init__(self,daRescueTime, daSession):

        self.daRescueTime = daRescueTime
        self.daSession = daSession

    """
    @param datetime_from
    @param datetime_to
    @return result[], array die per activiteit een lijst bevat. Deze bevat per tijdsinterval het percentage hoelang die activiteit actief was
    """
    def prepare_bar_chart_activities(self,datetime_from, datetime_to):
        #datetime_from, datetime_to = self.daSession.get_dates_session(session_id)
        unique_activities = self.daRescueTime.get_unique_activities_specific_period(datetime_from,datetime_to)
        list_activities_color = self.get_list_activities_color(unique_activities)
        list_dates = self.daRescueTime.get_dates(datetime_from,datetime_to)

        # Bevat per activiteit een lijst met per tijdsninterval met relatieve percentages hoevaak die activiteit per tijdsinterval actief was
        result = []
        for i in range(0,len(list_activities_color)):
            result.append([])
        for i_a_c in range(0,len(list_activities_color)):
            for i in range(0,len(list_dates)):
                sum_avg = 0.0
                datetime_interval_from = datetime.datetime.strptime(list_dates[i][0], "%Y-%m-%d %H:%M:%S")
                datetime_interval_to =  datetime_interval_from + datetime.timedelta(seconds=300)
                activities = self.daRescueTime.get_data_specific_period(datetime_interval_from,datetime_interval_to)
                for i_a in range(0,len(activities)):
                    if list_activities_color[i_a_c][0][0] == activities[i_a][3]:
                        sum_avg += float(activities[i_a][2])
                result[i_a_c].append(sum_avg / 300.0)

        return result,list_activities_color,list_dates

    """
    @param datetime_from, datetime_to
    @return result[], array die per activiteit een lijst bevat. Deze bevat per tijdsinterval het percentage hoelang die activiteit actief was
    """
    def prepare_bar_chart_important_activities(self,datetime_from, datetime_to):
        unique_activities = self.daRescueTime.get_unique_important_unimportant_activities_specific_period(datetime_from,datetime_to,1)
        list_activities_color = self.get_list_activities_color(unique_activities)
        list_dates = self.daRescueTime.get_dates(datetime_from,datetime_to)

        # Bevat per activiteit een lijst met per tijdsninterval met relatieve percentages hoevaak die activiteit per tijdsinterval actief was
        result = []
        for i in range(0,len(list_activities_color)):
            result.append([])
        for i_a_c in range(0,len(list_activities_color)):
            for i in range(0,len(list_dates)):
                sum_avg = 0.0
                datetime_interval_from = datetime.datetime.strptime(list_dates[i][0], "%Y-%m-%d %H:%M:%S")
                datetime_interval_to =  datetime_interval_from + datetime.timedelta(seconds=300)
                activities = self.daRescueTime.get_data_specific_period(datetime_interval_from,datetime_interval_to)
                for i_a in range(0,len(activities)):
                    if list_activities_color[i_a_c][0][0] == activities[i_a][3]:
                        sum_avg += float(activities[i_a][2])
                result[i_a_c].append(sum_avg / 300.0)

        return result,list_activities_color,list_dates


        """
    @param datetime_from, datetime_to
    @return result[], array die per activiteit een lijst bevat. Deze bevat per tijdsinterval het percentage hoelang die activiteit actief was
    """
    def prepare_bar_chart_important_unimportant_activities(self,datetime_from, datetime_to):
        color_important = [0.1,0.7,0.1]
        color_unimportant = [0.6,0.2,0.1]
        list_activities_color = [[['important'],color_important],[['unimportant'],color_unimportant]]
        list_dates = self.daRescueTime.get_dates(datetime_from,datetime_to)

        # Bevat per activiteit een lijst met per tijdsninterval met relatieve percentages hoevaak die activiteit per tijdsinterval actief was
        result = []
        for i in range(0,2):
            result.append([])

        for i in range(0,len(list_dates)):
            sum_avg_important = 0.0
            sum_avg_unimportant = 0.0
            datetime_interval_from = datetime.datetime.strptime(list_dates[i][0], "%Y-%m-%d %H:%M:%S")
            datetime_interval_to =  datetime_interval_from + datetime.timedelta(seconds=300)
            activities = self.daRescueTime.get_data_specific_period(datetime_interval_from,datetime_interval_to)
            for i_a in range(0,len(activities)):
                if activities[i_a][6] == 1:
                    sum_avg_important += float(activities[i_a][2])
                else:
                    sum_avg_unimportant += float(activities[i_a][2])

            result[0].append(sum_avg_important / 300.0)
            result[1].append(sum_avg_unimportant / 300.0)

        return result,list_activities_color,list_dates

    def get_list_activities_color(self,unique_activities):
        result = []
        colors = []
        difference_color = 15.0
        while len(unique_activities) > (100.0 / difference_color):
            difference_color -= 1.0
            if difference_color == 0:
                raise Exception.message('Too much activities, not enough colors')

        for i in range(0,len(unique_activities)):
            upper_bound = int(100.0 / difference_color)
            r = float(float((random.randint(0,upper_bound)) * difference_color)/100.0)
            g = float(float((random.randint(0,upper_bound)) * difference_color)/100.0)
            b = float(float((random.randint(0,upper_bound)) * difference_color)/100.0)

            while  [r,g,b] in colors:
                r = float(float((random.randint(0,upper_bound)) * difference_color)/100.0)
                g = float(float((random.randint(0,upper_bound)) * difference_color)/100.0)
                b = float(float((random.randint(0,upper_bound)) * difference_color)/100.0)

            colors.append([r,g,b])
            #result.append([unique_activities[i],i * x])
            result.append([unique_activities[i],[r,g,b]])
        return result




    """
    @param datetime_from, datetime_to
    @return result[], array die per activiteit een lijst bevat. Deze bevat per tijdsinterval het percentage hoelang die activiteit actief was
    """
    def prepare_bar_chart_subjects(self,datetime_from, datetime_to):
        unique_activities = self.daRescueTime.get_subject_period_only_subjectName(datetime_from,datetime_to)
        list_activities_color = self.get_list_activities_color(unique_activities)
        list_dates = self.daRescueTime.get_dates(datetime_from,datetime_to)

        # Bevat per activiteit een lijst met per tijdsninterval met relatieve percentages hoevaak die activiteit per tijdsinterval actief was
        result = []
        for i in range(0,len(list_activities_color)):
            result.append([])
        for i_a_c in range(0,len(list_activities_color)):
            for i in range(0,len(list_dates)):
                sum_avg = 0.0
                datetime_interval_from = datetime.datetime.strptime(list_dates[i][0], "%Y-%m-%d %H:%M:%S")
                datetime_interval_to =  datetime_interval_from + datetime.timedelta(seconds=300)
                activities = self.daRescueTime.get_subjects_period_all_fields(datetime_interval_from,datetime_interval_to)
                for i_a in range(0,len(activities)):
                    if list_activities_color[i_a_c][0][0] == activities[i_a][3]:
                        sum_avg += float(activities[i_a][2])
                result[i_a_c].append(sum_avg / 300.0)

        return result,list_activities_color,list_dates


