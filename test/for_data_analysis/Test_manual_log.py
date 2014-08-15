from for_data_analysis import Manual_log
import unittest


class test_manualLog(unittest.TestCase):
    def manual_logTest(self,manualLog):
        for i in range(0,len(manualLog)):
            print i
            if i > 55:
                pass
            self.assertTrue(manualLog[i][0] < manualLog[i][1])
            if i < len(manualLog) - 1:
                self.assertEqual(manualLog[i][1],manualLog[i+1][0])

    def test_manual_log_testpersoon_B(self):
        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_bugs_verwijderd()
        self.manual_logTest(manual_log_testpersoon_B)

    def test_manual_log_testpersoon_B_programs_websites(self):
        activities,manual_log_testpersoon_B = Manual_log.get_manual_logfile_Testpersoon_B_enkel_programmas_websites()
        self.manual_logTest(manual_log_testpersoon_B)


    def test_manual_log_testpersoon_E(self):
        activities,manual_log_testpersoon_E = Manual_log.get_manual_logfile_testpersoon_E()
        self.manual_logTest(manual_log_testpersoon_E)

    def test_manual_log_testpersoon_A(self):
        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_testpersoon_A()
        self.manual_logTest(manual_log_testpersoon_A)

    def test_manual_log_testpersoon_A_programs_websites(self):
        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_testpersoon_A_enkel_programmas_websites()
        self.manual_logTest(manual_log_testpersoon_A)

    def test_manual_log_testpersoon_A_userstates(self):
        activities,manual_log_testpersoon_A = Manual_log.get_manual_logfile_userstates_testpersoon_A()
        self.manual_logTest(manual_log_testpersoon_A)

    def test_manual_log_testpersoon_C_session_1(self):
        activities,manual_log_testpersoon_C_1 = Manual_log.get_manual_logfile_testpersoon_C_session_1()
        self.manual_logTest(manual_log_testpersoon_C_1)

    def test_manual_log_testpersoon_C_session_2(self):
        activities,manual_log_testpersoon_C_1 = Manual_log.get_manual_logfile_testpersoon_C_session_2()
        self.manual_logTest(manual_log_testpersoon_C_1)
    def test_manual_log_testpersoon_D(self):
        activities,manual_log_testpersoon_D = Manual_log.get_manual_log_testpersoon_D()
        self.manual_logTest(manual_log_testpersoon_D)


if __name__ == '__main__':
    unittest.main()