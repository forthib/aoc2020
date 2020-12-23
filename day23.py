def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '389125467'


def get_main_input():
    return '123487596'


def decode_input(input_str):
    return [int(label_str)-1 for label_str in input_str]


def make_next_cup_map(cups, n_cups):
    next_cup_map = [-1] * n_cups
    for i in range(len(cups)):
        next_cup_map[cups[i]] = cups[(i+1) % len(cups)]

    if n_cups > len(cups):
        for cup in range(len(cups), n_cups):
            next_cup_map[cup] = cup + 1
        next_cup_map[cups[-1]] = len(cups)
        next_cup_map[n_cups - 1] = cups[0]

    return next_cup_map


def do_one_move(current_cup, next_cup_map):
    n_cups = len(next_cup_map)
    cup0 = current_cup
    cup1 = next_cup_map[cup0]
    cup2 = next_cup_map[cup1]
    cup3 = next_cup_map[cup2]

    dest_cup = (cup0 + n_cups - 1) % n_cups
    while dest_cup == cup1 or dest_cup == cup2 or dest_cup == cup3:
        dest_cup = (dest_cup + n_cups - 1) % n_cups

    next_cup_map[cup0] = next_cup_map[cup3]
    next_cup_map[cup3] = next_cup_map[dest_cup]
    next_cup_map[dest_cup] = cup1

    return next_cup_map[cup0]


def run(cups, n_cups, n_moves):
    next_cup_map = make_next_cup_map(cups, n_cups)
    current_cup = cups[0]
    for _ in range(n_moves):
        current_cup = do_one_move(current_cup, next_cup_map)

    return next_cup_map


def get_labels(next_cup_map):
    cups = []
    cup = next_cup_map[0]
    while cup != 0:
        cups.append(cup)
        cup = next_cup_map[cup]
    return ''.join([str(cup+1) for cup in cups])


def run_part1(label, input_str, n_moves=100):
    cups = decode_input(input_str)
    next_cup_map = run(cups, len(cups), n_moves)
    labels = get_labels(next_cup_map)
    print(' - {} order after {} moves {}'.format(label, n_moves, labels))


def run_part2(label, input_str):
    cups = decode_input(input_str)
    next_cup_map = run(cups, 1000000, 10000000)
    cup1 = next_cup_map[0]
    cup2 = next_cup_map[cup1]
    print(' - {} result {}'.format(label, (cup1+1) * (cup2+1)))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input(), 10)
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test1:', get_test1_input())
    run_part2('main: ', get_main_input())
