import HTML_page_generator
from matplotlib import pyplot as plt
from visualisation import Visualisation_generator

def show_results(datetime_from, datetime_to,options_reason_with_screen_attribute,treshold_important_unimportant):
    HTML_page_generator.show_results(datetime_from, datetime_to,options_reason_with_screen_attribute,treshold_important_unimportant)
    showgraph(datetime_from, datetime_to, options_reason_with_screen_attribute)

# graphs
def showgraph(datetime_from, datetime_to,options_reason):
    visualisations_inst = Visualisation_generator.Visualisations('')
    #visualisations_inst.show_barchart_important_activity_details(datetime_from, datetime_to,options_reason)
    visualisations_inst.show_graph_attention_data_mindwave(datetime_from, datetime_to)

    visualisations_inst.show_barchart_subjects_mindwave_avg(datetime_from, datetime_to)
    visualisations_inst.show_barchart_subjects(datetime_from, datetime_to)
    visualisations_inst.show_barchart_activities_mindwave_attention_avg(datetime_from, datetime_to)

    visualisations_inst.show_barchart_important_unimportant_mindwave(datetime_from, datetime_to)
    visualisations_inst.show_barchart_important_unimportant_mindwave_avg(datetime_from, datetime_to)

    visualisations_inst.show_barchart_activities(datetime_from, datetime_to)
    visualisations_inst.show_barchart_activities_mindwave_avg(datetime_from, datetime_to)

    visualisations_inst.show_barchart_important_activities(datetime_from, datetime_to)
    visualisations_inst.show_barchart_important_activities_mindwave_avg(datetime_from, datetime_to)

   # show_barchart_attention_data_mindwave(datetime_from, datetime_to)
    """
    try:
        visualisations_inst.show_graph_comparison_attention_data_mindwave_and_userfeedback(datetime_from,datetime_to)
    except Exception, e:
        print str(e)
    """
    plt.show()
