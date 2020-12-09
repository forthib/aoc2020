def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_data():
    return '''35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''


def get_main_data():
    return get_file_content('day9_input.txt').strip()


def is_valid_value(value, data, first_index, preamble_size):
    for i in range(first_index, first_index + preamble_size):
        for j in range(i + 1, first_index + preamble_size):
            if value == data[i] + data[j]:
                return True
    return False


def get_data_from_data_str(data_str):
    return [int(value_str) for value_str in data_str.split('\n')]


def find_invalid_value(data, preamble_size):
    for i in range(preamble_size, len(data)):
        if not is_valid_value(data[i], data, i - preamble_size, preamble_size):
            return data[i]


def find_contiguous_sum_indexes(data, preamble_size, invalid_value):
    for i in range(len(data)):
        sum = 0
        for j in range(i, len(data)):
            sum += data[j]
            if sum == invalid_value:
                return (i, j + 1)
            elif sum > invalid_value:
                break


def run_part1(name, data_str, preamble_size):
    data = get_data_from_data_str(data_str)
    invalid_value = find_invalid_value(data, preamble_size)
    print(' - {}: invalid number {}'.format(name, invalid_value))


def run_part2(name, data_str, preamble_size):
    data = get_data_from_data_str(data_str)
    invalid_value = find_invalid_value(data, preamble_size)
    first, last = find_contiguous_sum_indexes(data, preamble_size, invalid_value)
    min_value = min(data[first:last])
    max_value = max(data[first:last])
    print(' - {}: encryption weakness {}'.format(name, min_value + max_value))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1', get_test1_data(), 5)
    run_part1('main ', get_main_data(), 25)
    print('Part 2')
    run_part2('test1', get_test1_data(), 5)
    run_part2('main ', get_main_data(), 25)
