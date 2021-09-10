import unittest
from bin.parsing import check_opening_time
from bin.main import main
import sys
import io

def stub_stdout(testcase_inst):
    stderr = sys.stderr
    stdout = sys.stdout
    
    def cleanup():
        sys.stderr = stderr
        sys.stdout = stdout
    
    testcase_inst.addCleanup(cleanup)
    sys.stderr = io.StringIO()
    sys.stdout = io.StringIO()

class TestParser(unittest.TestCase):

    def test_input_main_args_len(self):
        # error input args length
        sys.argv = ['tests']
        with self.assertRaises(Exception) as context:
            main()
        self.assertTrue('please input the opening_time and date' == str(context.exception))

    def test_input_main_input_format(self):
        # error input format
        sys.argv = ['tests', 'Mo-Fr 03:09-17:28|2021-09-07T17:31:00Z']
        with self.assertRaises(RuntimeError) as context:
            main()
        self.assertTrue('The opening_time and date parameteres are invalid' == str(context.exception))


    def test_input_main_ok(self):
        # correct input
        stub_stdout(self)
        sys.argv = ['tests', 'Mo-Fr 03:09-17:28,2021-09-07T17:31:00Z']
        main()
        self.assertTrue(str(sys.stdout.getvalue()), "Close\n")
    
    @staticmethod
    def gen_test_func(argv, out):
        def func(self):
            is_opening = check_opening_time(argv[0], argv[1])
            self.assertEqual(is_opening, out)
        return func

    def test_opening_time(self):
        # error opening time
        opening_time = 'Su- 03:09-17:28'
        data = '2005-11-07T07:33:20Z'
        with self.assertRaises(RuntimeError) as context:
            check_opening_time(opening_time, data)
        self.assertTrue('Invalid opening_time foramt' == str(context.exception))

    def test_date(self):
        # error date
        opening_time = 'Su 13:09-17:28'
        data = '2005-11-07T7.33'
        with self.assertRaises(ValueError) as context:
            check_opening_time(opening_time, data)
        self.assertTrue('%Y-%m-%dT%H:%M:%Sz' in str(context.exception))

def gen_test_cases():
    input_list = [
        {
            "argv":['Mo-Fr 03:09-17:30', '2021-09-07T17:30:50Z'],
            "name":'time_exceeds_maxmuim_time',
            "out":False
        },
        {
            "argv": ['Mo-Fr 10:09-17:32', '2021-09-07T10:08:59Z'],
            "name": 'time_less_than_minimun_time',
            "out": False
        },
        {
            "argv":['Mo-Fr 03:09-17:32', '2021-09-07T17:31:00Z'],
            "name":'time_is_ok(start_day_less_than_end_day)',
            "out":True
        },
        {
            "argv": ['Sa-Tu 03:09-17:32', '2021-09-07T17:31:00Z'],
            "name": 'time_is_ok(start_day_more_than_end_day)',
            "out": True
        },
        {
            "argv": ['Sa-Tu 03:09-17:32', '2021-09-08T17:31:00Z'],
            "name": 'day_exceeds_maximun_day',
            "out": False
        },
        {
            "argv": ['Sa-Tu 03:09-17:32', '2021-09-10T17:31:00Z'],
            "name": 'day_less_than_minimun_day',
            "out": False
        },
        {
            "argv": ['03:09-17:32', '2021-09-07T17:31:00Z'],
            "name": 'time_is_ok(open_every_day)',
            "out": True
        },
        {
            "argv": ['Mo 03:09-17:32', '2021-09-07T17:31:00Z'],
            "name": 'time_not_at_opening_day',
            "out": False
        },
        {
            "argv": ['Tu 03:09-17:32', '2021-09-07T17:31:00Z'],
            "name": 'time_is_ok(single_day)',
            "out": True
        },
        {
            "argv": ['Tu 03:09-17:31', '2021-09-07T17:31:00Z'],
            "name": 'time_reach_lower_boundary',
            "out": True
        },
        {
            "argv": ['Tu 10:09-17:31', '2021-09-07T10:09:00Z'],
            "name": 'time_reach_upper_boundary',
            "out": True
        }
    ]
    for item in input_list:
        setattr(TestParser, 'test_'+item["name"], TestParser.gen_test_func(item["argv"], item["out"]))

if __name__ == '__main__':
    gen_test_cases()
    unittest.main(verbosity=2)































