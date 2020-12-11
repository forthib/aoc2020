def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_report():
    return '''1721
979
366
299
675
1456'''


def get_main_report():
    return get_file_content('day1_input.txt').strip()


def run_part1(name, values_str):
    values = [int(value_str) for value_str in values_str.split('\n')]
    a, b = [(a, b) for a in values for b in values if a + b == 2020][0]
    print(' - {} {}x{}={}'.format(name, a, b, a * b))


def run_part2(name, values_str):
    values = [int(value_str) for value_str in values_str.split('\n')]
    a, b, c = [(a, b, c)
               for a in values for b in values for c in values if a + b + c == 2020][0]
    print(' - {} {}x{}x{}={}'.format(name, a, b, c, a * b * c))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_report())
    run_part1('main: ', get_main_report())
    print('Part 2')
    run_part2('test1:', get_test1_report())
    run_part2('main: ', get_main_report())
