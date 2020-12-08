def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_boarding_pass():
    return '''FBFBBFFRLR'''


def get_test2_boarding_pass():
    return '''BFFFBBFRRR'''


def get_test3_boarding_pass():
    return '''FFFBBBFRRR'''


def get_test4_boarding_pass():
    return '''BBFFBBFRLL'''


def get_main_boarding_passes():
    return get_file_content('day5_input.txt').strip()


def get_row(row_str):
    row_bin = [0 if c == 'F' else 1 for c in row_str]
    row = 0
    for digit in row_bin:
        row = (row << 1) + digit
    return row


def get_col(col_str):
    col_bin = [0 if c == 'L' else 1 for c in col_str]
    col = 0
    for digit in col_bin:
        col = (col << 1) + digit
    return col


def get_row_col_seatid(boarding_pass):
    row = get_row(boarding_pass[:7])
    col = get_col(boarding_pass[7:])
    return (row, col, row * 8 + col)


def test_part1(name, boarding_pass):
    row, col, seatid = get_row_col_seatid(boarding_pass)
    print(' - {}: row {}, column {}, seat ID {}'.format(name, row, col, seatid))


def run_part1(name, boarding_passes):
    seatids = [get_row_col_seatid(boarding_pass)[2] for boarding_pass in boarding_passes.split('\n')]
    print(' - {}: highest seat id {}'.format(name, max(seatids)))


def run_part2(name, boarding_passes):
    seatids = sorted([get_row_col_seatid(boarding_pass)[2] for boarding_pass in boarding_passes.split('\n')])
    first = seatids[0]
    last = seatids[-1]
    seatids = set(seatids)
    for seatid in range(first, last + 1):
        if seatid not in seatids:
            print(' - {}: my seat id {}'.format(name, seatid))


if __name__ == "__main__":
    print('Part 1')
    test_part1('test1', get_test1_boarding_pass())
    test_part1('test2', get_test2_boarding_pass())
    test_part1('test3', get_test3_boarding_pass())
    test_part1('test4', get_test4_boarding_pass())
    run_part1('main ', get_main_boarding_passes())
    print('Part 1')
    run_part2('main ', get_main_boarding_passes())
