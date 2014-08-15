import webbrowser
from data_tier import DARescueTime_SQLite
from exception import Exception
from logical_tier import Data_processing
from logical_tier.mindwave import Mindwave_enumeration
from logical_tier.mindwave import Mindwave_data_processing
from logical_tier.user_gone import User_gone_processing
from logical_tier.read_detection import Read_detection_processing
from logical_tier.userfeedback import Userfeedback_processing

window_movingAverage = 10
window_movingMedian = 5
treshold_poorSignalMindwave = 0

def percentage_layout(percentage):
    if percentage == -1:
        return "unknown"
    else:
        return str(round(percentage * 100,0)) + " %"
def calculate_time_str(total_seconds):
    seconds = total_seconds % 60
    minutes = total_seconds / 60
    hours = minutes / 60

    if total_seconds < 0 :
        return '00:00:00'
    if(hours < 10):
        strHours = '0' + str(hours)
    else:
        strHours = str(hours)

    minutes = minutes % 60

    if(minutes < 10):
        strMinutes = '0' + str(minutes)
    else:
        strMinutes = str(minutes)

    if(seconds < 10):
        strSeconds = '0' + str(seconds)
    else:
        strSeconds = str(seconds)

    result = strHours + ':' + strMinutes + ':' + strSeconds
    return result

def add_table_per_activiteit(result_html, list_important_activities, list_unimportant_activities,list_subjects):

    result_html += "<div id=\"activiteiten\">" + "\n"
    result_html += "<h2>Information about your activities on the computer:</h2>"
    result_html += "<table>"
    result_html += "\t" + "<tr><th>Studies</th><th>Unimportant activities</th></tr>"
    result_html += "\t" + "<tr><td>"

    # Important activities
    result_html += "\t" + "<table>"
    result_html += "\t" + "\t" + "<tr>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Activity</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Time (HH:MM:SS)</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg concentration</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg eyes detected</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg concentration mindwave</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg meditation mindwave</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg read</th>" + "\n"
    result_html += "\t" + "\t" + "</tr>" + "\n"



    for index in range(1,len(list_important_activities)):
        result_html += "\t" + "<tr>" + "\n"
        result_html += "\t" + "\t" + "<td>" + str(list_important_activities[index][0]) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + calculate_time_str(list_important_activities[index][1]) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][2]) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][3]) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][5]) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][6]) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][7]) + "</td>" + "\n"

        result_html +=  "\t" + "</tr>"
    result_html += "</table>" + "\n"


    result_html += "\t" + "</td><td>"

    # Unimportant activities
    if len(list_unimportant_activities) == 0:
        result_html += "empty"
    else:
        result_html += "\t" + "<table>"
        result_html += "\t" + "\t" + "<tr>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Activity</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Time (HH:MM:SS)</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Avg concentration mindwave</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Avg meditation mindwave</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Avg read</th>" + "\n"
        result_html += "\t" + "\t" + "</tr>" + "\n"


        for row in list_unimportant_activities:
            print row
            result_html += "\t" + "<tr>" + "\n"

            result_html += "\t" + "\t" + "<td>" + str(row[0]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(row[1]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + percentage_layout(row[2]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + percentage_layout(row[3]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + percentage_layout(row[4]) + "</td>" + "\n"

            result_html += "\t" + "</tr>" + "\n"
        result_html += "</table>" + "\n"
    result_html += "\t" + "</td></tr>"
    result_html += "</table>"

    result_html += "</div>"
    return result_html


def add_table_per_activity_with_subjects(result_html, list_important_activities, list_unimportant_activities,list_subjects):

    result_html += "<div id=\"activiteiten\">" + "\n"
    result_html += "<h2>Information about your activities on the computer:</h2>"
    result_html += "<table>"
    result_html += "\t" + "<tr><th>Studies</th><th>Unimportant activities</th></tr>"
    result_html += "\t" + "<tr><td>"

    # Important activities
    result_html += "\t" + "<table>"
    result_html += "\t" + "\t" + "<tr>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Subject</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Activity</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Time (HH:MM:SS)</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg concentration</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg eyes detected</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg concentration mindwave</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg meditation mindwave</th>" + "\n"
    result_html += "\t" + "\t" + "\t" + "<th>Avg read</th>" + "\n"
    result_html += "\t" + "\t" + "</tr>" + "\n"


    for item in list_subjects:
        first_item_added = False
        teller = 0
        for row in list_important_activities:
            if row[8]==item[0]:
                teller += 1



        for index in range(0,len(list_important_activities)):
            if list_important_activities[index][8]==item[0]:
                result_html += "\t" + "<tr>" + "\n"
                if first_item_added is False:
                    result_html +=  "\t" + "\t" + "<td rowspan=" + str(teller) + ">" + str(item[1]) + "</td>" + "\n"
                    first_item_added = True

                result_html += "\t" + "\t" + "<td>" + str(list_important_activities[index][0]) + "</td>" + "\n"
                result_html += "\t" + "\t" + "<td>" + calculate_time_str(list_important_activities[index][1]) + "</td>" + "\n"
                result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][2]) + "</td>" + "\n"
                result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][3]) + "</td>" + "\n"
                """
                result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][5]) + "</td>" + "\n"
                result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][6]) + "</td>" + "\n"
                """
                result_html += "\t" + "\t" + "<td>" + add_mindwave_bucket(list_important_activities[index][5]) + "</td>" + "\n"
                result_html += "\t" + "\t" + "<td>" + add_mindwave_bucket(list_important_activities[index][6]) + "</td>" + "\n"
                result_html += "\t" + "\t" + "<td>" + percentage_layout(list_important_activities[index][7]) + "</td>" + "\n"
                result_html += "\t" + "</tr>" + "\n"


    result_html += "</table>" + "\n"


    result_html += "\t" + "</td><td>"

    # Unimportant activities
    if len(list_unimportant_activities) == 0:
        result_html += "empty"
    else:
        result_html += "\t" + "<table>"
        result_html += "\t" + "\t" + "<tr>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Activity</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Time (HH:MM:SS)</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Avg concentration mindwave</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Avg meditation mindwave</th>" + "\n"
        result_html += "\t" + "\t" + "\t" + "<th>Avg read</th>" + "\n"
        result_html += "\t" + "\t" + "</tr>" + "\n"


        for row in list_unimportant_activities:
            print row
            result_html += "\t" + "<tr>" + "\n"

            result_html += "\t" + "\t" + "<td>" + str(row[0]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(row[1]) + "</td>" + "\n"
            #result_html += "\t" + "\t" + "<td>" + percentage_layout(row[2]) + "</td>" + "\n"
#            result_html += "\t" + "\t" + "<td>" + percentage_layout(row[3]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + add_mindwave_bucket(row[2]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + add_mindwave_bucket(row[3]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + percentage_layout(row[4]) + "</td>" + "\n"
            result_html += "\t" + "</tr>" + "\n"
        result_html += "</table>" + "\n"
    result_html += "\t" + "</td></tr>"
    result_html += "</table>"

    result_html += "</div>"
    return result_html

def add_mindwave_bucket(mindwave_bucket):
    result_html = "<table>" + "\n"
    result_html += "\t" + "<tr>" + "\n"
    for i in range(0,len(mindwave_bucket)):
        result_html += "\t" + "\t" + "<th>" + Mindwave_enumeration.get_label(i) + "</th>" + "\n"
    result_html += "\t" + "</tr>" + "\n"
    result_html += "\t" + "<tr>" + "\n"
    for i in range(0,len(mindwave_bucket)):
        result_html += "\t" + "\t" + "<td>" + percentage_layout(mindwave_bucket[i]) + "</td>" + "\n"
    result_html += "\t" + "</tr>" + "\n"
    result_html += "</table>" + "\n"
    return result_html



def add_table_per_activiteit_userGone(options_reason, result_html, test):
    result_html += "<div id=\"details_activiteit\">" + "\n"
    result_html += "<h2>This table shows the duration of the time that you were not looking at the screen:</h2>"
    result_html += "<table>"
    result_html += "\t" + "<tr>" + "\n"
    result_html += "<th>Activity</th>"
    for row in options_reason:
        result_html += "\t" + "\t" + "<th>" + row[0] + "</th>" + "\n"
    result_html += "\t" + "</tr>" + "\n"
    for item in test:
        result_html += "\t" + "<tr>" + "\n"
        result_html += "\t" + "\t" + "<td>" + item[0] + "</td>" + "\n"
        for cel in item[4]:
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(cel[1])) + "</td>" + "\n"
        result_html += "\t" + "</tr>" + "\n"
    result_html += "</table>" + "\n"
    result_html += "</div>" + "\n"
    return result_html


def add_table_userGone(datetime_from, datetime_to, options_reason, result_html, test):
       # Tabel afgeleid, notities, ...
    list_userGone = User_gone_processing.get_list_userGone(datetime_from, datetime_to, options_reason)
    result_html += "<div id=\"details_userGone\">" + "\n"
    result_html += "<h2>This table shows the reason why you were not looking at the screen and the relative duration:</h2>"

    result_html += "<table>"
    result_html += "\t" + "<tr>" + "\n"
    result_html += "\t" + "\t" + "<th></th>" + "\n"
    result_html += "\t" + "\t" + "<th>Total</th>" + "\n"
    result_html += "\t" + "\t" + "<th>Average</th>" + "\n"
    result_html += "\t" + "\t" + "<th>Minimum</th>" + "\n"
    result_html += "\t" + "\t" + "<th>Maximum</th>" + "\n"
    result_html += "\t" + "</tr>" + "\n"
    for item in list_userGone:
        result_html += "\t" + "<tr>" + "\n"
        result_html += "\t" + "\t" + "<th>" + item[0] + "</th>" + "\n"
        result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[1])) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[2])) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[3])) + "</td>" + "\n"
        result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[4])) + "</td>" + "\n"

        result_html += "\t" + "</tr>" + "\n"
    result_html += "</table>" + "\n"
    result_html += "</div>" + "\n"
    return result_html

def add_table_workSession(datetime_from, datetime_to, options_reason,treshold_important_unimportant, result_html):
    try:
        # Tabel afgeleid, notities, ...
        list_worksessions = Data_processing.get_list_work_sessions(datetime_from, datetime_to, options_reason,treshold_important_unimportant,'')
        result_html += "<div id=\"work_session\">" + "\n"
        result_html += "<h2>This table shows an overview of your work sessions:</h2>"

        result_html += "<table>"
        result_html += "\t" + "<tr>" + "\n"
        result_html += "\t" + "\t" + "<th>From</th>" + "\n"
        result_html += "\t" + "\t" + "<th>To</th>" + "\n"
        result_html += "\t" + "\t" + "<th>Reason</th>" + "\n"
        result_html += "\t" + "\t" + "<th>Studying</th>" + "\n"
        result_html += "\t" + "\t" + "<th>Time seconds</th>" + "\n"
        result_html += "\t" + "</tr>" + "\n"
        for item in list_worksessions:
            result_html += "\t" + "<tr>" + "\n"
            result_html += "\t" + "\t" + "<td>" + str(item[0].strftime("%Y-%m-%d %H:%M:%S")) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + str(item[1].strftime("%Y-%m-%d %H:%M:%S")) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + str(item[2]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + str(item[3]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[4])) + "</td>" + "\n"

            result_html += "\t" + "</tr>" + "\n"
        result_html += "</table>" + "\n"
        result_html += "</div>" + "\n"
    except Exception.ListEmpty, e:
        result_html += "<p>" + str(e) + "</p>"
    return result_html

def add_table_workSession_gem_min_max(datetime_from, datetime_to, options_reason,treshold_important_unimportant, result_html):

    # Tabel afgeleid, notities, ...
    try:
        list_worksessions = Data_processing.get_list_work_sessions(datetime_from, datetime_to, options_reason,treshold_important_unimportant,'')

        # [isStudying, reason, total, amount, avg, min, max]
        list_worksessions_avg_min_max = Data_processing.get_list_workSession_amount_details(list_worksessions,options_reason)

        result_html += "<div id=\"work_session\">" + "\n"
        result_html += "<h2>This table gives information about your work sessions:</h2>"

        result_html += "<table>"
        result_html += "\t" + "<tr>" + "\n"
        result_html += "\t" + "\t" + "<th></th>" + "\n"
        result_html += "\t" + "\t" + "<th>Total</th>" + "\n"
        result_html += "\t" + "\t" + "<th>Amount</th>" + "\n"
        result_html += "\t" + "\t" + "<th>Average duration</th>" + "\n"
        result_html += "\t" + "\t" + "<th>Minimal duration</th>" + "\n"
        result_html += "\t" + "\t" + "<th>Maximal duration</th>" + "\n"
        result_html += "\t" + "</tr>" + "\n"

        for item in list_worksessions_avg_min_max:
            result_html += "\t" + "<tr>" + "\n"
            result_html += "\t" + "\t" + "<th>" + str(item[1]) + "</th>" + "\n"
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[2])) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + str(item[3]) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[4])) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[5])) + "</td>" + "\n"
            result_html += "\t" + "\t" + "<td>" + calculate_time_str(int(item[6])) + "</td>" + "\n"

            result_html += "\t" + "</tr>" + "\n"
        result_html += "</table>" + "\n"
        result_html += "</div>" + "\n"

    except  Exception.ListEmpty, e:
        result_html += "<p>" + str(e) + "</p>" + "\n"
    return result_html




def show_results(datetime_from, datetime_to,options_reason_with_screen_attribute,treshold_important_unimportant):
    options_reason = Data_processing.remove_screen_attribute(options_reason_with_screen_attribute)
    result_css = '<style media="screen" type="text/css">' + "\n"
    result_css += '\t' + 'table, td,th {' + '\n'
    result_css += '\t' + '\t' + 'border: 1px solid black; margin: 2px;border-collapse:collapse;padding: 5px;' + '\n'
    result_css += '\t' + '}' + '\n'
    result_css += '\t' + 'div {' + '\n'
    result_css += '\t' + '\t' + 'margin: 20px;'
    result_css += '\t' + '}'
    result_css += '</style>'


    important_activities = Data_processing.getListImportantActivities_V2_buckets(datetime_from,datetime_to,options_reason,'')
    unimportant_activities = Data_processing.getListUnimportantActivities_V2_buckets(datetime_from,datetime_to,'')

    darescuetime = DARescueTime_SQLite.RescueTime('')
    list_subjects = darescuetime.get_subject_period(datetime_from,datetime_to)

    result_html = "<!DOCTYPE html>" + "\n"
    result_html += "<html>" + "\n"
    result_html += "<head>" + "\n"
    result_html += "\t" + "<title>Results session</title>" + "\n"
    result_html += result_css
    result_html += "</head>" + "\n"
    result_html += "<body>" + "\n"

    # Tabel per activiteit
    result_html = add_table_per_activity_with_subjects(result_html, important_activities, unimportant_activities,list_subjects)



# Tabel per activitiet, hoeveel afgeleid, notities, ...
    result_html = add_table_userGone(datetime_from, datetime_to, options_reason, result_html, important_activities)

#Add table per activiteit user gone
    result_html = add_table_per_activiteit_userGone(options_reason, result_html, important_activities)

#tabel worksessies min max avg ...
    result_html = add_table_workSession_gem_min_max(datetime_from,datetime_to,options_reason,treshold_important_unimportant,result_html)
# tabel worksessies
    result_html = add_table_workSession(datetime_from,datetime_to,options_reason,treshold_important_unimportant,result_html)

    result_html += "<h2>Some additional information:</h2>"

    result_html += '<p>' + 'average eyes detected = ' + percentage_layout(User_gone_processing.get_eyes_detected_specific_period(datetime_from,datetime_to)) + '</p>' + '\n'
    try:
        avg_concentration_userfeedback = Userfeedback_processing.get_average_userfeedback_specific_period(datetime_from, datetime_to)
    except Exception.ListEmpty, e:
        avg_concentration_userfeedback = -1

    avg_reading = Read_detection_processing.get_average_reading_specific_period(datetime_from, datetime_to)

    result_html += '<p>' +  'average concentration userfeedback = ' + percentage_layout(avg_concentration_userfeedback) + '</p>' + '\n'
    attention_mindwave, meditation_mindwave = Mindwave_data_processing.get_average_attention_meditation_specific_period(datetime_from,datetime_to)
    result_html += '<p>' +  'average concentration mindwave = ' + percentage_layout(attention_mindwave) + '\n'
    result_html += '<p>' +  'average meditation mindwave = ' + percentage_layout(meditation_mindwave) + '</p>' + '\n'
    result_html += '<p>' +  'average read = ' + percentage_layout(avg_reading) + '</p>' + '\n'


    #print df['Date'].unique()
    #df.to_csv('rt_data_interval_activity_20120901.csv', index=False)

    result_html += "</body>" + "\n"
    result_html += "</html>" + "\n"

    result_page = open("result_page.htm","wb")
    result_page.write(result_html)
    result_page.close()

    new = 2
    url = "result_page.htm"
    webbrowser.open(url,new=new)

    #print result_html
