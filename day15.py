def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''0,3,6'''


def get_main_input():
    return '''18,8,0,5,4,1,20'''


def generator(numbers):
    ages = {n: i for i, n in enumerate(numbers)}
    for n in numbers:
        yield n
    last_i = len(numbers) - 1
    last_n = numbers[-1]
    while True:
        n = last_i - ages[last_n] if last_n in ages else 0
        yield n
        ages[last_n] = last_i
        last_i += 1
        last_n = n


def run(label, input_str, index):
    gen = generator([int(s) for s in input_str.split(',')])
    for i, n in enumerate(gen):
        if i == index - 1:
            print(' - {} number #{} = {} for sequence {}'.format(label,
                                                                 index, n, input_str))
            return


if __name__ == "__main__":
    run_labels = ['test{}:'.format(i) for i in range(1, 8)] + ['main: ']
    run_sequences = ['0,3,6', '1,3,2', '2,1,3', '1,2,3',
                     '2,3,1', '3,2,1', '3,1,2', get_main_input()]
    for part_label, index in zip(['Part 1', 'Part 2'], [2020, 30000000]):
        print(part_label)
        for run_label, run_sequence in zip(run_labels, run_sequences):
            run(run_label, run_sequence, index)
