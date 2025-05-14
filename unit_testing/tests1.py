import unittest as ut
from demo import Calculator

class TestOp(ut.TestCase):
    def setUp(self):
        self.calculation = Calculator(8, 2)

    #functions must be named test_<something>
    def test_sum(self):
        self.assertEqual(self.calculation.do_sum(), 10, 'The sum is wrong!')

    def test_product(self):
        self.assertEqual(self.calculation.do_product(), 16, 'The product is wrong!')
    
    def test_divide(self):
        self.assertEqual(self.calculation.do_divide(), 4, 'The divide is wrong!')

    def test_subtract(self):
        self.assertEqual(self.calculation.do_subtract(), 6, 'The subtract is wrong!')

if __name__ == '__main__':
    ut.main()