def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12'''


def get_test2_input():
    return '''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9'''


def get_main_input():
    return get_file_content('day16_input.txt').strip()


def decode_range(range_str):
    first_str, last_str = range_str.split('-')
    return (int(first_str), int(last_str))


def decode_rule(rule_str):
    field, ranges_str = rule_str.split(':')
    ranges = [decode_range(range_str.strip())
              for range_str in ranges_str.split('or')]
    return (field, ranges)


def decode_ticket(ticket_str):
    return [int(value_str) for value_str in ticket_str.strip().split(',')]


def decode_input(input_str):
    input_str = input_str.replace('your ticket:', '#')
    input_str = input_str.replace('nearby tickets:', '#')
    rules_str, your_ticket_str, nearby_tickets_str = input_str.split('#')

    rules = dict([decode_rule(rule_str)
                  for rule_str in rules_str.strip().split('\n')])
    your_ticket = decode_ticket(your_ticket_str)
    nearby_tickets = [decode_ticket(
        ticket_str) for ticket_str in nearby_tickets_str.strip().split('\n')]

    return (rules, your_ticket, nearby_tickets)


def multiply(values):
    result = 1
    for value in values:
        result *= value
    return result


def is_value_in_ranges(value, ranges):
    for first, last in ranges:
        if value >= first and value <= last:
            return True
    return False


def are_values_in_ranges(values, ranges):
    return all(is_value_in_ranges(value, ranges) for value in values)


def is_valid_value(value, rules):
    for _, ranges in rules.items():
        if is_value_in_ranges(value, ranges):
            return True
    return False


def get_ticket_invalid_values(ticket, rules):
    return [value for value in ticket if not is_valid_value(value, rules)]


def get_tickets_invalid_values(tickets, rules):
    values = list()
    for ticket in tickets:
        values += get_ticket_invalid_values(ticket, rules)
    return values


def filter_value_fields(value_fields, rules, values):
    return [field for field in value_fields if are_values_in_ranges(values, rules[field])]


def filter_values_fields(values_fields, rules, tickets):
    for i, value_fields in enumerate(values_fields):
        values = [ticket[i] for ticket in tickets]
        values_fields[i] = set(
            filter_value_fields(value_fields, rules, values))


def remove_positionned_fields(values_fields):
    unique_fields = set([field for value_fields in values_fields if len(
        value_fields) == 1 for field in value_fields])
    for i, value_fields in enumerate(values_fields):
        if len(value_fields) != 1:
            values_fields[i] = value_fields - unique_fields


def find_fields(rules, your_ticket, nearby_tickets):
    nearby_tickets = [ticket for ticket in nearby_tickets if len(
        get_ticket_invalid_values(ticket, rules)) == 0]
    all_tickets = nearby_tickets + [your_ticket]

    values_fields = [set([field for field in rules])] * len(your_ticket)
    filter_values_fields(values_fields, rules, all_tickets)
    while not all(len(f) == 1 for f in values_fields):
        remove_positionned_fields(values_fields)
    return [list(value_fields)[0] for value_fields in values_fields]


def run_part1(label, input_str):
    rules, _, nearby_tickets = decode_input(input_str)
    invalid_values = get_tickets_invalid_values(nearby_tickets, rules)
    print(' - {} error rate {}'.format(label, sum(invalid_values)))


def test_part2(label, input_str):
    rules, your_ticket, nearby_tickets = decode_input(input_str)
    fields = find_fields(rules, your_ticket, nearby_tickets)
    print(' - {} fields {}'.format(label, fields))


def run_part2(label, input_str):
    rules, your_ticket, nearby_tickets = decode_input(input_str)
    fields = find_fields(rules, your_ticket, nearby_tickets)
    target_values = [your_ticket[i] for i, field in enumerate(
        fields) if field.startswith('departure')]
    print(' - {} result {} with values {}'.format(label,
                                                  multiply(target_values), target_values))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    test_part2('test1:', get_test1_input())
    test_part2('test2:', get_test2_input())
    run_part2('main: ', get_main_input())
