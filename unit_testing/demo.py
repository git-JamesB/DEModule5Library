class Calculator:
    def __init__(self, a ,b):
        self.a = a
        self.b = b

    def do_sum(self):
        return self.a + self.b
    
    def do_product(self):
        return self.a * self.b
    
    def do_subtract(self):
        return self.a - self.b
    
    def do_divide(self):
        return self.a / self.b

#myCalc = Calculator(4, 5)
#myCalc2 = Calculator(12, 44)
#print(f'First result {myCalc.do_sum()} and second result {myCalc2.do_product()}')

if __name__ == "__main__":
    calc = Calculator(float(input('Input first number')), float(input('Input second number')))
    print(calc.do_product())