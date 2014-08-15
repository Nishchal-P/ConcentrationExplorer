from logical_tier.user_gone import User_gone_processing
from logical_tier import Data_processing

__author__ = 'Peter'

from presentation_tier import Output
import datetime
import unittest


class TestUserGoneTracker(unittest.TestCase):
    def test_list_userGone(self):
        options_reason_with_screen_attribute = [["afgeleid","afgeleid",0],["notities","notities",1],["screen","screen",1],["pauze","pauze",0]]
        options_reason = Data_processing.remove_screen_attribute(options_reason_with_screen_attribute)
        datetime_from = datetime.datetime.strptime("2013-12-28 08:00:00","%Y-%m-%d %H:%M:%S")
        datetime_to =  datetime.datetime.strptime("2013-12-28 08:30:00","%Y-%m-%d %H:%M:%S")

         # [reason,  totaal, gemiddeld, minimaal, maximaal]
        list_userGone = User_gone_processing.get_list_userGone(datetime_from,datetime_to,options_reason)
        print '---------'
        print list_userGone
        print '---------'

        #afgeleid attribuut
        self.assertEqual(list_userGone[0][1],1380)
        self.assertEqual(list_userGone[0][2],345)
        self.assertEqual(list_userGone[0][3],120)
        self.assertEqual(list_userGone[0][4],720)

        #notities attribuut
        self.assertEqual(list_userGone[1][1],240)
        self.assertEqual(list_userGone[1][2],120)
        self.assertEqual(list_userGone[1][3],120)
        self.assertEqual(list_userGone[1][4],120)

        #pauze attribuut
        self.assertEqual(list_userGone[2][1],0)
        self.assertEqual(list_userGone[2][2],0)
        self.assertEqual(list_userGone[2][3],0)
        self.assertEqual(list_userGone[2][4],0)


if __name__ == '__main__':
    unittest.main()