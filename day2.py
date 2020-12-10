def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_passwords():
    return '''1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc'''


def get_main_passwords():
    return get_file_content('day2_input.txt').strip()


def get_password(password_str):
    policy, password = password_str.split(':')
    lh, letter = policy.split()
    lh = lh.split('-')
    policy = {'index1': int(lh[0]), 'index2': int(lh[1]), 'letter': letter}
    password = {'policy': policy, 'password': password.strip()}
    return password


def is_valid_part1(password):
    policy = password['policy']
    n = sum(1 for c in password['password'] if c == policy['letter'])
    return n >= policy['index1'] and n <= policy['index2']


def is_valid_part2(password):
    policy = password['policy']
    index1 = policy['index1'] - 1
    index2 = policy['index2'] - 1
    letter = policy['letter']
    passwd = password['password']
    letter1 = passwd[index1] if index1 < len(passwd) else ''
    letter2 = passwd[index2] if index2 < len(passwd) else ''
    return (letter1 == letter) != (letter2 == letter)


def run(name, passwords_str, is_valid_function):
    passwords = [get_password(p) for p in passwords_str.split('\n')]
    count = sum(1 for p in passwords if is_valid_function(p))
    print(' - {} {} valid passwords'.format(name, count))


def run_part1(name, passwords_str):
    run(name, passwords_str, is_valid_part1)


def run_part2(name, passwords_str):
    run(name, passwords_str, is_valid_part2)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_passwords())
    run_part1('main: ', get_main_passwords())
    print('Part 2')
    run_part2('test1:', get_test1_passwords())
    run_part2('main: ', get_main_passwords())
