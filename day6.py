import string


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_answers():
    return '''abcx
abcy
abcz'''


def get_test2_answers():
    return '''abc

a
b
c

ab
ac

a
a
a
a

b'''


def get_main_answers():
    return get_file_content('day6_input.txt').strip()


def count_answers_anyone(answers_group):
    answers_set = set()
    for answers in answers_group:
        answers_set |= set(answers)
    return len(answers_set)


def count_answers_everyone(answers_group):
    answers_set = set(string.ascii_lowercase)
    for answers in answers_group:
        answers_set &= set(answers)
    return len(answers_set)


def run(name, answers_groups_str, count_function):
    answers_groups = [answers_group_str.split(
        '\n') for answers_group_str in answers_groups_str.split('\n\n')]
    sizes_groups = [count_function(answers_group)
                    for answers_group in answers_groups]
    print(' - {}: {}'.format(name, sum(sizes_groups)))


def run_part1(name, answers_groups_str):
    run(name, answers_groups_str, count_answers_anyone)


def run_part2(name, answers_groups_str):
    run(name, answers_groups_str, count_answers_everyone)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1', get_test1_answers())
    run_part1('test2', get_test2_answers())
    run_part1('main ', get_main_answers())
    print('Part 2')
    run_part2('test1', get_test1_answers())
    run_part2('test2', get_test2_answers())
    run_part2('main ', get_main_answers())
