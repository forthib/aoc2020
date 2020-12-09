import string


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_expected_field():
    return ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']


def get_expected_field_minus_cid():
    return ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


def get_test1_passports():
    return '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''


def get_test2_invalid_passports():
    return '''eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007'''


def get_test3_valid_passports():
    return '''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'''


def get_main_passports():
    return get_file_content('day4_input.txt').strip()


def get_passport(passport_str):
    passport = dict()
    for s in passport_str.replace('\n', ' ').split():
        key, value = s.split(':')
        passport[key] = value
    return passport


def is_valid_number_in_range(s, min, max):
    if not s.isdigit():
        return False
    s = int(s)
    return s >= min and s <= max


def is_valid_byr(byr):
    return len(byr) == 4 and is_valid_number_in_range(byr, 1920, 2002)


def is_valid_iyr(iyr):
    return len(iyr) == 4 and is_valid_number_in_range(iyr, 2010, 2020)


def is_valid_eyr(eyr):
    return len(eyr) == 4 and is_valid_number_in_range(eyr, 2020, 2030)


def is_valid_hgt(hgt):
    if hgt.endswith('cm'):
        return is_valid_number_in_range(hgt[:-2], 150, 193)
    elif hgt.endswith('in'):
        return is_valid_number_in_range(hgt[:-2], 59, 76)
    else:
        return False


def is_valid_hcl(hcl):
    return hcl.startswith('#') and len(hcl[1:]) == 6 and all(c in string.hexdigits for c in hcl[1:])


def is_valid_ecl(ecl):
    return ecl in 'amb blu brn gry grn hzl oth'.split()


def is_valid_pid(pid):
    return len(pid) == 9 and pid.isdigit()


def is_valid_value(key, value):
    valid_functions = {'byr': is_valid_byr, 'iyr': is_valid_iyr, 'eyr': is_valid_eyr,
                       'hgt': is_valid_hgt, 'hcl': is_valid_hcl, 'ecl': is_valid_ecl, 'pid': is_valid_pid}
    return valid_functions[key](value) if key in valid_functions else True


def test_valid_value(key, value):
    valid_str = 'valid:  ' if is_valid_value(key, value) else 'invalid:'
    print(' - {} {} {}'.format(key, valid_str, value))


def is_valid_part1(passport):
    for key in get_expected_field_minus_cid():
        if key not in passport:
            return False
    return True


def is_valid_part2(passport):
    for key in get_expected_field_minus_cid():
        if key not in passport or not is_valid_value(key, passport[key]):
            return False
    return True


def run(name, passports_str, is_valid_function):
    passports = [get_passport(passport_str)
                 for passport_str in passports_str.split('\n\n')]
    passports = [p for p in passports if is_valid_function(p)]
    print(' - {}: valid passports {}'.format(name, len(passports)))


def run_part1(name, passports_str):
    run(name, passports_str, is_valid_part1)


def run_part2(name, passports_str):
    run(name, passports_str, is_valid_part2)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1', get_test1_passports())
    run_part1('main ', get_main_passports())
    print('Part 2')
    test_valid_value('byr', '2002')
    test_valid_value('byr', '2003')
    test_valid_value('hgt', '60in')
    test_valid_value('hgt', '190cm')
    test_valid_value('hgt', '190in')
    test_valid_value('hgt', '190')
    test_valid_value('hcl', '#123abc')
    test_valid_value('hcl', '#123abz')
    test_valid_value('hcl', '123abc')
    test_valid_value('ecl', 'brn')
    test_valid_value('ecl', 'wat')
    test_valid_value('pid', '000000001')
    test_valid_value('pid', '0123456789')
    run_part2('test invalid', get_test2_invalid_passports())
    run_part2('test valid  ', get_test3_valid_passports())
    run_part2('main        ', get_main_passports())
