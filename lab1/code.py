from math import *

def pikar(approx, x):
    switcher = {
            1 : pow(x, 3) / 3.0,
            2 : pow(x, 3) / 3.0 + pow(x, 7) / 63.0,
            3 : pow(x, 3) / 3.0 + pow(x, 7) / 63.0 + 2 * pow(x, 11) / 2079.0
                + pow(x, 15) / 59535.0,
            4 : pow(x, 3) / 3.0 + pow(x, 7) / 63.0 + 2 * pow(x, 11) / 2079.0
                + 13 * pow(x, 15) / 218295.0 + 82 * pow(x, 19) / 37328445.0
                + 662 * pow(x, 23) / 10438212015.0 + 4 * pow(x, 27) / 3341878155.0
                + pow(x, 31) / 109876902975.0
            }
    return switcher.get(approx, "Invalid approx")

def explicit_function(x, h):
    f = 0
    x0 = h
    while (x0 < x + h / 2):
        f += h * (x0 * x0 + f * f)
        x0 += h
    return f

def notexplicit_function(x, h):
    f = 0
    x0 = h
    while (x0 < x + h):
        descr = 1 - 4 * h * (h * x0 * x0 + f)
        if (descr >= 0):
            f1 = (1 + sqrt(descr)) / 2 / h
            f2 = (1 - sqrt(descr)) / 2 / h
            f = f1 if f2 < 0 else f2 if f1 < 0 else min(f1, f2)
        x0 += h
    return f

def main():
    i = 0
    print('Pikar')
    print('   X  | 1 approx| 2 approx| 3 approx| 4 approx')
    while(i < 3):
        print('%5.2f | %4.5f | %4.5f | %4.5f | %4.5f' % (i, pikar(1, i), pikar(2, i), pikar(3, i), pikar(4, i)))
        i += 0.1

    i = 0
    print('Explicit function')
    print('   X  |    -1   |    -2   |    -3   |    -4  |    -5  |    -6   ')
    while(i < 2):
        print('%5.2f | %4.5f | %4.5f | %4.5f | %4.5f| %4.5f| %4.5f' % (i, explicit_function(i, 0.1), explicit_function(i, 0.01), explicit_function(i, 0.001), explicit_function(i, 0.0001), explicit_function(i, 0.00001), explicit_function(i, 0.000001)))
        i += 0.1

    i = 0
    print('Not explicit function')
    print('   X  |    -1   |    -2   |    -3   |    -4   |    -5   |  -6  ')
    while(i < 2):
        print('%5.2f | %7.5f | %7.5f | %7.5f | %7.5f| %7.5f| %7.5f' % (i, notexplicit_function(i, 0.1), notexplicit_function(i, 0.01), notexplicit_function(i, 0.001), notexplicit_function(i, 0.0001), notexplicit_function(i, 0.00001), notexplicit_function(i, 0.000001)))
        i += 0.1

if __name__ == "__main__":
    main()
