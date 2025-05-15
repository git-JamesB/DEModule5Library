import unittest as ut
import pandas as pd
import custom_functions as cf


class TestOp(ut.TestCase):
    def setUp(self):
        self.record = pd.DataFrame(columns = ['Id', 'Books', 'Book checkout', 'Book Returned', 'Days allowed to borrow', 'Customer ID'],
                                   data = [[1, 'test book', '"12/05/2025"', '14/05/2025', '2 weeks', '2']] )
        #apply custom functions to test
        self.modifieddf = cf.dupecheck(df = self.record)
        self.modifieddf = cf.todatetime(df = self.modifieddf, column = 'Book Returned')
        self.modifieddf = cf.todatetime(df = self.modifieddf, column = 'Book checkout')
        self.modifieddf = cf.dateDuration(date1 = 'Book checkout', date2 = 'Book Returned', df = self.modifieddf)

# Check duration column is an integer
    def test_duration_int(self):
        self.assertTrue(pd.api.types.is_integer_dtype(self.modifieddf['date_delta']), "The delta col is not an integer!")

# Check todatetime
    def test_datetime(self):
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(self.modifieddf['Book Returned']), "Column needs produce a datetime!")

# Check dedupe
    def test_deduper(self):
        self.assertEqual(len(self.modifieddf), 1, "Should remove duplicates to leave 1 row!")
        self.assertTrue(self.modifieddf.duplicated().count()) == 0, "Output should contain no duplicates!"


if __name__ == '__main__':
    ut.main()