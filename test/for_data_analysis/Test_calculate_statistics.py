from for_data_analysis import Calculate_statistics

import unittest


class test_calculate_statistics(unittest.TestCase):

    def test_merge_resultTuple(self):
       result_x_A = [1,2,3,4]
       result_y_A = [0.1,0.2,0.3,0.4]
       resultTupleA = Calculate_statistics.ResultTuple(result_x_A,result_y_A)

       result_x_B = [5,6,7,8]
       result_y_B = [0.5,0.6,0.7,0.8]
       resultTupleB = Calculate_statistics.ResultTuple(result_x_B,result_y_B)

       resultTupleA.merge(resultTupleB)
       result_x_solution = [1,2,3,4,5,6,7,8]
       result_y_solution = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
       self.assertEqual(resultTupleA.result_x,result_x_solution)
       self.assertEqual(resultTupleA.result_y,result_y_solution)

    def test_ResultObject(self):
        #A
        result_x_A_1 = [1,2,3]
        result_y_A_1 = [0.1,0.2,0.3]
        resultTupleA1 = Calculate_statistics.ResultTuple(result_x_A_1,result_y_A_1)

        result_x_A_2 = [11,22,33]
        result_y_A_2 = [0.11,0.22,0.33]
        resultTupleA2 = Calculate_statistics.ResultTuple(result_x_A_2,result_y_A_2)

        result_x_A_3 = [111,222,333]
        result_y_A_3 = [0.111,0.222,0.333]
        resultTupleA3 = Calculate_statistics.ResultTuple(result_x_A_3,result_y_A_3)

        result_x_A_4 = [1111,2222,3333]
        result_y_A_4 = [0.1111,0.2222,0.3333]
        resultTupleA4 = Calculate_statistics.ResultTuple(result_x_A_4,result_y_A_4)

        result_x_A_5 = [11111,22222,33333]
        result_y_A_5 = [0.11111,0.22222,0.33333]
        resultTupleA5 = Calculate_statistics.ResultTuple(result_x_A_5,result_y_A_5)

        result_x_A_6 = [111111,222222,333333]
        result_y_A_6 = [0.111111,0.222222,0.333333]
        resultTupleA6 = Calculate_statistics.ResultTuple(result_x_A_6,result_y_A_6)

        result_x_A_7 = [1111111,2222222,3333333]
        result_y_A_7 = [0.1111111,0.2222222,0.3333333]
        resultTupleA7 = Calculate_statistics.ResultTuple(result_x_A_7,result_y_A_7)


        resultObjectA = Calculate_statistics.ResultObject()
        resultObjectA.result_timeSpent_activity_avg = resultTupleA1
        resultObjectA.result_timeSpent_activity_std = resultTupleA2

        resultObjectA.result_concentration_diff_activity_switch_avg = resultTupleA3

        resultObjectA.result_amount_used_programs_avg = resultTupleA4
        resultObjectA.result_amount_used_programs_std = resultTupleA5

        resultObjectA.amount_activities_RescueTime_interval_with_mindwave_avg = resultTupleA6
        resultObjectA.amount_activities_RescueTime_interval_with_mindwave_std = resultTupleA7




        #B
        result_x_B_1 = [4,5,6]
        result_y_B_1 = [0.4,0.5,0.6]
        resultTupleB1 = Calculate_statistics.ResultTuple(result_x_B_1,result_y_B_1)

        result_x_B_2 = [44,55,66]
        result_y_B_2 = [0.44,0.55,0.66]
        resultTupleB2 = Calculate_statistics.ResultTuple(result_x_B_2,result_y_B_2)

        result_x_B_3 = [444,555,666]
        result_y_B_3 = [0.444,0.555,0.666]
        resultTupleB3 = Calculate_statistics.ResultTuple(result_x_B_3,result_y_B_3)

        result_x_B_4 = [4444,5555,6666]
        result_y_B_4 = [0.4444,0.5555,0.6666]
        resultTupleB4 = Calculate_statistics.ResultTuple(result_x_B_4,result_y_B_4)

        result_x_B_5 = [44444,55555,66666]
        result_y_B_5 = [0.44444,0.55555,0.66666]
        resultTupleB5 = Calculate_statistics.ResultTuple(result_x_B_5,result_y_B_5)

        result_x_B_6 = [444444,555555,666666]
        result_y_B_6 = [0.444444,0.555555,0.666666]
        resultTupleB6 = Calculate_statistics.ResultTuple(result_x_B_6,result_y_B_6)

        result_x_B_7 = [4444444,5555555,6666666]
        result_y_B_7 = [0.4444444,0.5555555,0.6666666]
        resultTupleB7 = Calculate_statistics.ResultTuple(result_x_B_7,result_y_B_7)

        resultObjectB = Calculate_statistics.ResultObject()
        resultObjectB.result_timeSpent_activity_avg = resultTupleB1
        resultObjectB.result_timeSpent_activity_std = resultTupleB2

        resultObjectB.result_concentration_diff_activity_switch_avg = resultTupleB3

        resultObjectB.result_amount_used_programs_avg = resultTupleB4
        resultObjectB.result_amount_used_programs_std = resultTupleB5

        resultObjectB.amount_activities_RescueTime_interval_with_mindwave_avg = resultTupleB6
        resultObjectB.amount_activities_RescueTime_interval_with_mindwave_std = resultTupleB7
        #merge
        resultObjectA.merge(resultObjectB)

        #check
        resultTuple_solution_1 = Calculate_statistics.ResultTuple([1,2,3,4,5,6],[0.1,0.2,0.3,0.4,0.5,0.6])
        resultTuple_solution_2 = Calculate_statistics.ResultTuple([11,22,33,44,55,66],[0.11,0.22,0.33,0.44,0.55,0.66])
        resultTuple_solution_3 = Calculate_statistics.ResultTuple([111,222,333,444,555,666],[0.111,0.222,0.333,0.444,0.555,0.666])
        resultTuple_solution_4 = Calculate_statistics.ResultTuple([1111,2222,3333,4444,5555,6666],[0.1111,0.2222,0.3333,0.4444,0.5555,0.6666])
        resultTuple_solution_5 = Calculate_statistics.ResultTuple([11111,22222,33333,44444,55555,66666],[0.11111,0.22222,0.33333,0.44444,0.55555,0.66666])
        resultTuple_solution_6 = Calculate_statistics.ResultTuple([111111,222222,333333,444444,555555,666666],[0.111111,0.222222,0.333333,0.444444,0.555555,0.666666])
        resultTuple_solution_7 = Calculate_statistics.ResultTuple([1111111,2222222,3333333,4444444,5555555,6666666],[0.1111111,0.2222222,0.3333333,0.4444444,0.5555555,0.6666666])


        self.assertEqual(resultObjectA.result_timeSpent_activity_avg.result_x,resultTuple_solution_1.result_x)
        self.assertEqual(resultObjectA.result_timeSpent_activity_avg.result_y,resultTuple_solution_1.result_y)

        self.assertEqual(resultObjectA.result_timeSpent_activity_std.result_x,resultTuple_solution_2.result_x)
        self.assertEqual(resultObjectA.result_timeSpent_activity_std.result_y,resultTuple_solution_2.result_y)

        self.assertEqual(resultObjectA.result_concentration_diff_activity_switch_avg.result_x,resultTuple_solution_3.result_x)
        self.assertEqual(resultObjectA.result_concentration_diff_activity_switch_avg.result_y,resultTuple_solution_3.result_y)

        self.assertEqual(resultObjectA.result_amount_used_programs_avg.result_x,resultTuple_solution_4.result_x)
        self.assertEqual(resultObjectA.result_amount_used_programs_avg.result_y,resultTuple_solution_4.result_y)

        self.assertEqual(resultObjectA.result_amount_used_programs_std.result_x,resultTuple_solution_5.result_x)
        self.assertEqual(resultObjectA.result_amount_used_programs_std.result_y,resultTuple_solution_5.result_y)

        self.assertEqual(resultObjectA.amount_activities_RescueTime_interval_with_mindwave_avg.result_x,resultTuple_solution_6.result_x)
        self.assertEqual(resultObjectA.amount_activities_RescueTime_interval_with_mindwave_avg.result_y,resultTuple_solution_6.result_y)

        self.assertEqual(resultObjectA.amount_activities_RescueTime_interval_with_mindwave_std.result_x,resultTuple_solution_7.result_x)
        self.assertEqual(resultObjectA.amount_activities_RescueTime_interval_with_mindwave_std.result_y,resultTuple_solution_7.result_y)


if __name__ == '__main__':
    unittest.main()