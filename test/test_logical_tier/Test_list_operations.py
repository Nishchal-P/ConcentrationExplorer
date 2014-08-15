from logical_tier import List_operations

__author__ = 'Peter'
import unittest


class TestListOperations(unittest.TestCase):
    def test_moving_median_mindwave_array_1(self):


        mindwaveArray = [0.20,0.10,0.30,0.80,0.40,0.21,0.54,0.25,0.45,0.90]
        result = List_operations.moving_median(mindwaveArray,3)

        self.assertEqual(round(result[0],2),round(0.20,2))
        self.assertEqual(round(result[1],2),round(0.15,2))
        self.assertEqual(round(result[2],2),round(0.2,2))
        self.assertEqual(round(result[3],2),round(0.3,2))
        self.assertEqual(round(result[4],2),round(0.4,2))
        self.assertEqual(round(result[5],2),round(0.4,2))
        self.assertEqual(round(result[6],2),round(0.4,2))
        self.assertEqual(round(result[7],2),round(0.25,2))
        self.assertEqual(round(result[8],2),round(0.45,2))
        self.assertEqual(round(result[9],2),round(0.45,2))

    def test_moving_median_mindwave_array_2(self):
        mindwaveArray = [0.20,0.10,0.30,0.80,0.40,0.21,0.54,0.25,0.45,0.90]
        result = List_operations.moving_median(mindwaveArray,5)

        self.assertEqual(round(result[0],2),round(0.20,2))
        self.assertEqual(round(result[1],2),round(0.15,2))
        self.assertEqual(round(result[2],2),round(0.2,2))
        self.assertEqual(round(result[3],2),round(0.25,2))
        self.assertEqual(round(result[4],2),round(0.3,2))
        self.assertEqual(round(result[5],2),round(0.3,2))
        self.assertEqual(round(result[6],2),round(0.4,2))
        self.assertEqual(round(result[7],2),round(0.4,2))
        self.assertEqual(round(result[8],2),round(0.40,2))
        self.assertEqual(round(result[9],2),round(0.45,2))

    def test_moving_median_mindwave_array_3(self):
        mindwaveArray = [0.20,0.10,0.30,0.80,0.40,0.21,0.54,0.25,0.45,0.90]
        result = List_operations.moving_median(mindwaveArray,1)

        self.assertEqual(round(result[0],2),round(0.20,2))
        self.assertEqual(round(result[1],2),round(0.1,2))
        self.assertEqual(round(result[2],2),round(0.3,2))
        self.assertEqual(round(result[3],2),round(0.80,2))
        self.assertEqual(round(result[4],2),round(0.4,2))
        self.assertEqual(round(result[5],2),round(0.21,2))
        self.assertEqual(round(result[6],2),round(0.54,2))
        self.assertEqual(round(result[7],2),round(0.25,2))
        self.assertEqual(round(result[8],2),round(0.45,2))
        self.assertEqual(round(result[9],2),round(0.90,2))

    def test_moving_median_middle_1(self):
        mindwaveArray = [0.20,0.10,0.30,0.80,0.40,0.21,0.54,0.25,0.45,0.90]
        result = List_operations.moving_median_middle(mindwaveArray,5)

        self.assertEqual(round(result[0],2),round(0.2,2))
        self.assertEqual(round(result[1],2),round(0.25,2))
        self.assertEqual(round(result[2],2),round(0.3,2))
        self.assertEqual(round(result[3],2),round(0.30,2))
        self.assertEqual(round(result[4],2),round(0.4,2))
        self.assertEqual(round(result[5],2),round(0.4,2))
        self.assertEqual(round(result[6],2),round(0.4,2))
        self.assertEqual(round(result[7],2),round(0.45,2))
        self.assertEqual(round(result[8],2),round(0.49,2))
        self.assertEqual(round(result[9],2),round(0.45,2))

    def test_moving_median_mindwave_array_2(self):
        mindwaveArray = [0.20,0.10,0.30,0.80,0.40,0.21,0.54,0.25,0.45,0.90]
        result = List_operations.moving_median_middle(mindwaveArray,1)

        self.assertEqual(round(result[0],2),round(0.20,2))
        self.assertEqual(round(result[1],2),round(0.1,2))
        self.assertEqual(round(result[2],2),round(0.3,2))
        self.assertEqual(round(result[3],2),round(0.80,2))
        self.assertEqual(round(result[4],2),round(0.4,2))
        self.assertEqual(round(result[5],2),round(0.21,2))
        self.assertEqual(round(result[6],2),round(0.54,2))
        self.assertEqual(round(result[7],2),round(0.25,2))
        self.assertEqual(round(result[8],2),round(0.45,2))
        self.assertEqual(round(result[9],2),round(0.90,2))

    def test_moving_median_mindwave_array_3(self):
        mindwaveArray = [0.20,0.10,0.30,0.80,0.40,0.21,0.54,0.25,0.45,0.90]
        result = List_operations.moving_median_middle(mindwaveArray,3)

        self.assertEqual(round(result[0],2),round(0.15,2))
        self.assertEqual(round(result[1],2),round(0.20,2))
        self.assertEqual(round(result[2],2),round(0.3,2))
        self.assertEqual(round(result[3],2),round(0.4,2))
        self.assertEqual(round(result[4],2),round(0.4,2))
        self.assertEqual(round(result[5],2),round(0.4,2))
        self.assertEqual(round(result[6],2),round(0.25,2))
        self.assertEqual(round(result[7],2),round(0.45,2))
        self.assertEqual(round(result[8],2),round(0.45,2))
        self.assertEqual(round(result[9],2),round(0.68,2))
    def test_get_1D_list_from_2D_doubles_removed(self):
        list = []

        list.append([None,None,"Peter"])
        list.append([None,None,"Peter"])
        list.append([None,None,"AAA"])
        list.append([None,None,"AA"])
        list.append([None,None,"AB"])
        list.append([None,None,"AC"])
        list.append([None,None,"AAA"])
        result = List_operations.get_1D_list_from_2D_doubles_removed(list,2)
        self.assertEqual(len(result),5)
        self.assertEqual(result[0],"Peter")
        self.assertEqual(result[1],"AAA")
        self.assertEqual(result[2],"AA")
        self.assertEqual(result[3],"AB")
        self.assertEqual(result[4],"AC")

    def test_delete_entry(self):
        a = [5,8,9,6,4,5,1,2,3]
        a_deleted = List_operations.delete_entry(a,3)
        self.assertEqual(len(a) - 1,len(a_deleted))
        self.assertEqual(a[0],a_deleted[0])
        self.assertEqual(a[1],a_deleted[1])
        self.assertEqual(a[2],a_deleted[2])
        self.assertEqual(a[4],a_deleted[3])
        self.assertEqual(a[5],a_deleted[4])
        self.assertEqual(a[6],a_deleted[5])
        self.assertEqual(a[7],a_deleted[6])
        self.assertEqual(a[8],a_deleted[7])
if __name__ == '__main__':
    unittest.main()