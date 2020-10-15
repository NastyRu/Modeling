import datetime
import csv
import random
import numpy

def get_time():
    now = datetime.datetime.now()

    minute = int(now.minute)
    second = int(now.second)

    if (0 == minute):
        minute = 60

    if (0 == second):
        second = 60

    return int(now.hour), minute, second

def read_csv(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ';')
        return list(csv_reader)

def get_table_number(table, i, j, num, count):
    res = []
    for c in range(count):
        res_v = 0
        num_v = num
        while (num_v > 0):
            ost = j % 5
            if (1 == ost):
                res_p = int(table[i - 1][j // 5]) // pow(10, 4)
            elif (2 == ost):
                res_p = int(table[i - 1][j // 5]) // pow(10, 3) % 10
            elif (3 == ost):
                res_p = int(table[i - 1][j // 5]) // pow(10, 2) % 10
            elif (4 == ost):
                res_p = int(table[i - 1][j // 5]) // pow(10, 1) % 10
            else:
                res_p = int(table[i - 1][j // 5 - 1]) % 10
            num_v -= 1
            res_v = res_v * 10 + res_p
            j += 1
            if (j > 60):
                j = 1
                i += 1
            if (i > 60):
                i = 1
        if (res_v < pow(10, num - 1)):
            res_v += pow(10, num - 1)
        res.append(res_v)
    return res

def alg_generator(num, count):
    res = []
    for c in range(count):
        res.append(random.randint(pow(10, num - 1), pow(10, num) - 1))
    return res

def table_generator(num, count):
    hour, minute, second = get_time()
    if (hour % 2):
        table = read_csv("odd_table.csv")
    else:
        table = read_csv("even_table.csv")
    return get_table_number(table, second, minute, num, count)

def frequency_creteria(list, num):
    freq = [0 for i in range(5)]

    if (1 == num):
        begin = 0
        delta = 2
    else:
        delta = (pow(10, num) - pow(10, num - 1)) // 5
        begin = pow(10, num - 1)

    for elem in list:
        if (elem < begin + delta):
            freq[0] += 1
        elif (elem < begin + 2 * delta):
            freq[1] += 1
        elif (elem < begin + 3 * delta):
            freq[2] += 1
        elif (elem < begin + 4 * delta):
            freq[3] += 1
        else:
            freq[4] += 1

    return freq

def frequency_creteria2(list, num):
    mean = numpy.mean(list)
    disp = numpy.sqrt(numpy.var(list))

    if (1 == num):
        begin = 0
    else:
        begin = pow(10, num - 1)
    end = pow(10, num)

    count = 0
    for elem in list:
        if (mean - disp) < elem < (mean + disp):
            count += 1

    return [(2 * disp / (end - begin)), count / len(list)]

def table_print(list1, list2, list3, n):
    print("   |   N   |   1   |   2   |   3   |")
    print("   |_______________________________|")
    if (n > 10):
        for i in range(5):
            print("   |%6d |   %d   |  %d   |  %d  |" % (i + 1, list1[i], list2[i], list3[i]))
        print("   |                  ...          |")
        for i in range(n - 5, n):
            print("   |%6d |   %d   |  %d   |  %d  |" % (i + 1, list1[i], list2[i], list3[i]))
    else:
        for i in range(n):
            print("   |%6d |   %d   |  %d   |  %d  |" % (i + 1, list1[i], list2[i], list3[i]))

    ofreq1, pfreq1 = frequency_creteria2(list1, 1)
    ofreq2, pfreq2 = frequency_creteria2(list2, 2)
    ofreq3, pfreq3 = frequency_creteria2(list3, 3)
    print("Ожидаемый  | %.2f  | %.2f  | %.2f  |" % (ofreq1, ofreq2, ofreq3))
    print("Полученный | %.2f  | %.2f  | %.2f  |" % (pfreq1, pfreq2, pfreq3))

def main():
    n = 10
    alg_list1 = alg_generator(1, n)
    table_list1 = table_generator(1, n)
    alg_list2 = alg_generator(2, n)
    table_list2 = table_generator(2, n)
    alg_list3 = alg_generator(3, n)
    table_list3 = table_generator(3, n)

    print("Программный генератор")
    table_print(alg_list1, alg_list2, alg_list3, n)
    print()
    print("Табличный генератор")
    table_print(table_list1, table_list2, table_list3, n)

if __name__ == "__main__":
    main()
