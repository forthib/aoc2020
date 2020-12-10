def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_joltages():
    return '''16
10
15
5
1
11
7
19
6
12
4'''


def get_test2_joltages():
    return '''28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3'''


def get_main_joltages():
    return get_file_content('day10_input.txt').strip()


def get_joltages(joltages_str):
    joltages = [int(j) for j in joltages_str.split('\n')]
    joltages.append(0)
    joltages.append(max(joltages) + 3)
    return sorted(joltages)


def get_choices(index, joltages):
    choices = list()
    for i in range(1, 4):
        if index < len(joltages) - i and joltages[index + i] - joltages[index] <= 3:
            choices.append(index + i)
    return choices


def count_arrangements_rec(choices, counts, index=0):
    if index == len(choices) - 1:
        return 1
    if index in counts:
        return counts[index]
    cpt = 0
    for next_index in choices[index]:
        cpt += count_arrangements_rec(choices, counts, next_index)
    counts[index] = cpt
    return cpt


def count_arrangements(joltages):
    choices = [get_choices(i, joltages) for i in range(len(joltages))]
    counts = dict()
    return count_arrangements_rec(choices, counts)


def run_part1(label, joltages_str):
    joltages = get_joltages(joltages_str)

    diffs = [j-i for i, j in zip(joltages[:-1], joltages[1:])]
    one_jolt_diff = diffs.count(1)
    three_jolt_diff = diffs.count(3)
    distribution = one_jolt_diff * three_jolt_diff

    print(' - {} one-jolt {} three-jolt {} distribution joltage {}'.format(label,
                                                                           one_jolt_diff, three_jolt_diff, distribution))


def run_part2(label, joltages_str):
    joltages = get_joltages(joltages_str)
    print(' - {} arrangements {}'.format(label, count_arrangements(joltages)))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_joltages())
    run_part1('test2:', get_test2_joltages())
    run_part1('main: ', get_main_joltages())
    print('Part 2')
    run_part2('test1:', get_test1_joltages())
    run_part2('test2:', get_test2_joltages())
    run_part2('main: ', get_main_joltages())
