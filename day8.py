from pathlib import Path


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


class Console:
    def __init__(self):
        self.eip = 0
        self.acc = 0


def run_instr(console, instr):
    command, arg = instr.split()

    if command == 'nop':
        console.eip += 1
    elif command == 'acc':
        console.acc += int(arg)
        console.eip += 1
    elif command == 'jmp':
        console.eip += int(arg)
    else:
        raise ValueError('unsupported command')


class RunResult:
    def __init__(self, success, acc):
        self.success = success
        self.acc = acc


def run(code):
    eips = set()

    console = Console()
    while True:
        if console.eip == len(code):
            return RunResult(True, console.acc)
        if console.eip in eips:
            return RunResult(False, console.acc)
        eips.add(console.eip)

        instr = code[console.eip]
        run_instr(console, instr)


def get_test1_code():
    return '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''.split('\n')


def get_main_code():
    return get_file_content(Path('day8_input.txt')).split('\n')


def run_part1(code):
    result = run(code)
    print(' - acc: ' + str(result.acc))


def change_command(code, i):
    command, arg = code[i].split()
    if command == 'nop':
        code[i] = 'jmp ' + arg
        return True
    elif command == 'jmp':
        code[i] = 'nop ' + arg
        return True
    else:
        return False


def run_part2(code):
    for i in range(len(code)):
        fixed_code = list(code)
        if change_command(fixed_code, i):
            result = run(fixed_code)
            if result.success:
                print(' - acc: ' + str(result.acc))
                return
    print(' - not found :-(')


if __name__ == "__main__":
    print('Part 1')
    run_part1(get_test1_code())
    run_part1(get_main_code())
    print('Part 2')
    run_part2(get_test1_code())
    run_part2(get_main_code())
