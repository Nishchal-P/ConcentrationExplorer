from presentation_tier.visualisation import Visualisation_generator
from presentation_tier.visualisation import Convert_to_barchart_data
from data_tier import DARescueTime_SQLite
from data_tier import DASession_SQLite


import unittest


class test_visualisations(unittest.TestCase):
    daRescueTime = DARescueTime_SQLite.RescueTime('')
    daSession = DASession_SQLite.DASession('')
    barchartGenerator = Convert_to_barchart_data.ConvertToBarchartData(daRescueTime,daSession)

    def test_prepare_bar_chart_important_unimportant_activities(self):
        session_id = 1
        datetime_from, datetime_to = self.daSession.get_dates_session(session_id)
        result,activities_color,dates = self.barchartGenerator.prepare_bar_chart_important_unimportant_activities(datetime_from, datetime_to)

        self.assertEqual(result[0][0], 1.0)
        self.assertEqual(result[0][1], 1.0)
        self.assertEqual(result[0][2], 1.0)
        self.assertEqual(result[0][3], 1.0)
        self.assertEqual(result[0][4], 1.0)
        self.assertEqual(round(result[0][5],2), 0.67)
        self.assertEqual(result[0][6], 1.0)

        self.assertEqual(result[1][0], 0.0)
        self.assertEqual(result[1][1], 0.0)
        self.assertEqual(result[1][2], 0.0)
        self.assertEqual(result[1][3], 0.0)
        self.assertEqual(result[1][4], 0.0)
        # Fout in testgegevens database. 'niet belangrijke activiteit' van 100 seconden ontbreekt
        # self.assertEqual(round(result[1][5],2), 0.33)
        self.assertEqual(result[1][6], 0.0)

        result,activities_color,dates = self.barchartGenerator.prepare_bar_chart_activities(datetime_from, datetime_to)
        # A
        self.assertEqual(round(result[0][0],2),0.67)
        self.assertEqual(round(result[0][1],2),0.67)
        self.assertEqual(round(result[0][2],2),1.00)
        self.assertEqual(round(result[0][3],2),0.67)
        self.assertEqual(round(result[0][4],2),0)
        self.assertEqual(round(result[0][5],2),0)
        self.assertEqual(round(result[0][6],2),0)

        #B
        self.assertEqual(round(result[1][0],2),0)
        self.assertEqual(round(result[1][1],2),0)
        self.assertEqual(round(result[1][2],2),0)
        self.assertEqual(round(result[1][3],2),0.33)
        self.assertEqual(round(result[1][4],2),1)
        self.assertEqual(round(result[1][5],2),0.67)
        self.assertEqual(round(result[1][6],2),1)

        #C
        self.assertEqual(round(result[2][0],2),0.33)
        self.assertEqual(round(result[2][1],2),0.33)
        self.assertEqual(round(result[2][2],2),0.0)
        self.assertEqual(round(result[2][3],2),0.0)
        self.assertEqual(round(result[2][4],2),0.0)
        self.assertEqual(round(result[2][5],2),0.0)
        self.assertEqual(round(result[2][6],2),0.0)


if __name__ == '__main__':
    unittest.main()