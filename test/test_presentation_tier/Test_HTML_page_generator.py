from presentation_tier import HTML_page_generator
import unittest


class TestHTMLPageGenerator(unittest.TestCase):
    def test_calculate_time_str(self):
        result = HTML_page_generator.calculate_time_str(300)
        self.assertEqual(result,'00:05:00')

        result = HTML_page_generator.calculate_time_str(123)
        self.assertEqual(result,'00:02:03')

        result = HTML_page_generator.calculate_time_str(2)
        self.assertEqual(result,'00:00:02')

        result = HTML_page_generator.calculate_time_str(4005)
        self.assertEqual(result,'01:06:45')

        result = HTML_page_generator.calculate_time_str(12501)
        self.assertEqual(result,'03:28:21')


if __name__ == '__main__':
    unittest.main()