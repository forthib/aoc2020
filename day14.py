import itertools


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''


def get_test2_input():
    return '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1'''


def get_main_input():
    return get_file_content('day14_input.txt').strip()


def decode_command(command_str):
    lhs, rhs = command_str.split('=')
    lhs = int(lhs.strip()[4:-1])
    rhs = int(rhs.strip())
    return (lhs, rhs)


def set_bit(value, i, bit):
    if bit == 0:
        return value & ~(1 << i)
    elif bit == 1:
        return value | (1 << i)


def apply_mask(value, mask):
    for i, c in enumerate(reversed(mask)):
        if c == '0' or c == '1':
            value = set_bit(value, i, int(c))
    return value


def bit_absorbing_or(c1, c2):
    if c1 == 'X' or c2 == 'X':
        return 'X'
    elif c1 == '1' or c2 == '1':
        return '1'
    else:
        return '0'


def bitwise_operation(addr1, addr2, operation):
    return ''.join([operation(c1, c2) for c1, c2 in zip(addr1, addr2)])


def bitwise_absorbing_or(addr1, addr2):
    return bitwise_operation(addr1, addr2, bit_absorbing_or)


def apply_mask_on_address(address, mask):
    return bitwise_absorbing_or(bin(address)[2:].zfill(36), mask)


def develop(addr):
    nx = sum(1 for c in addr if c == 'X')
    for x_values in itertools.product(['0', '1'], repeat=nx):
        ix = 0
        addr_list = [c for c in addr]
        for i, c in enumerate(addr):
            if c == 'X':
                addr_list[i] = x_values[ix]
                ix += 1
        yield ''.join(addr_list)


def run_part1(label, input_str):
    commands = input_str.split('\n')
    memory = dict()
    mask = ''.join(['X'] * 36)
    for command in commands:
        if command.startswith('mask'):
            mask = command.split('=')[1].strip()
        else:
            address, value = decode_command(command)
            memory[address] = apply_mask(value, mask)
    memory_sum = sum(value for _, value in memory.items())
    print(' - {} sum {}'.format(label, memory_sum))


def run_part2(label, input_str):
    commands = input_str.split('\n')
    commands_history = []
    mask = ''.join(['X'] * 36)
    for command in commands:
        if command.startswith('mask'):
            mask = command.split('=')[1].strip()
        else:
            address, value = decode_command(command)
            floating_address = apply_mask_on_address(address, mask)
            commands_history.append((set(develop(floating_address)), value))

    memory_sum = 0
    used_addresses = set()
    for addresses, value in reversed(commands_history):
        memory_sum += value * len(addresses - used_addresses)
        used_addresses |= addresses

    print(' - {} sum {}'.format(label, memory_sum))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test2:', get_test2_input())
    run_part2('main: ', get_main_input())
