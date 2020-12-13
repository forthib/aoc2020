def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''939
7,13,x,x,59,x,31,19'''


def get_test2_input():
    return '''17,x,13,19'''


def get_test3_input():
    return '''67,7,59,61'''


def get_test4_input():
    return '''67,x,7,59,61'''


def get_test5_input():
    return '''67,7,x,59,61'''


def get_test6_input():
    return '''1789,37,47,1889'''


def get_main_input():
    return get_file_content('day13_input.txt').strip()


def decode_input(input_str):
    split_input_str = input_str.split('\n')
    if len(split_input_str) == 1:
        earliest_time_str = '0'
        bus_ids_str = input_str
    else:
        earliest_time_str, bus_ids_str = split_input_str
    earliest_time = int(earliest_time_str)
    bus_ids = [(int(bus_id_str), i) for i, bus_id_str in enumerate(
        bus_ids_str.split(',')) if bus_id_str != 'x']
    return (earliest_time, bus_ids)


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def find_next_bus(earliest_time, bus_ids):
    bus_ids = set([bus_id for bus_id, _ in bus_ids])
    while True:
        primes = prime_factors(earliest_time)
        primes = [prime for prime in primes if prime in bus_ids]
        if len(primes) > 0:
            return (primes[0], earliest_time)
        earliest_time += 1


def find_time_2(start_time, id1, id2, delay):
    time = start_time
    while True:
        if (time + delay) % id2 == 0:
            return time
        time += id1


def find_time_n(bus_ids):
    time = 0
    bus_id = 1
    for next_bus_id, delay in bus_ids:
        time = find_time_2(time, bus_id, next_bus_id, delay)
        bus_id *= next_bus_id
    return time


def run_part1(label, input_str):
    earliest_time, bus_ids = decode_input(input_str)
    bus_id, bus_time = find_next_bus(earliest_time, bus_ids)
    waiting_time = bus_time - earliest_time
    print(' - {} bus id {} x waiting time {} = {}'.format(label,
                                                          bus_id, waiting_time, bus_id * waiting_time))


def run_part2(label, input_str):
    _, bus_ids = decode_input(input_str)
    time = find_time_n(bus_ids)
    print(' - {} time {}'.format(label, time))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test1:', get_test1_input())
    run_part2('test2:', get_test2_input())
    run_part2('test3:', get_test3_input())
    run_part2('test4:', get_test4_input())
    run_part2('test5:', get_test5_input())
    run_part2('main: ', get_main_input())
