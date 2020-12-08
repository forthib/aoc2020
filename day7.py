def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def parse_lhs(lhs):
    return lhs.replace('bags', '').strip()


def parse_rhs(rhs):
    result = dict()
    for rhs_part in rhs.split(','):
        rhs_part = rhs_part.replace('bags', '').replace(
            'bag', '').replace('.', '').strip()
        if rhs_part != 'no other':
            pos = rhs_part.find(' ')
            n = int(rhs_part[:pos])
            key = rhs_part[pos+1:]
            result[key] = n
    return result


def parse_rule(rule_str):
    lhs, rhs = rule_str.split('contain')
    lhs = parse_lhs(lhs)
    rhs = parse_rhs(rhs)
    return (lhs, rhs)


def parse_rules(rules_str):
    rules = dict()
    for rule_str in rules_str.strip().split('\n'):
        lhs, rhs = parse_rule(rule_str)
        rules[lhs] = rhs
    return rules


def bag_contains(rules, outer_bag, inner_bag, containing_bags):
    if outer_bag in containing_bags:
        return containing_bags[outer_bag]

    for bag in rules[outer_bag]:
        if bag == inner_bag or bag_contains(rules, bag, inner_bag, containing_bags):
            containing_bags[outer_bag] = True
            return True
    containing_bags[outer_bag] = False
    return False


def count_bag_names_containing(rules, bag):
    bags = dict()
    n = 0
    for lhs in rules:
        if bag_contains(rules, lhs, bag, bags):
            n += 1
    return n


def count_bags(rules, outer_bag):
    rhs = rules[outer_bag]
    n = 0
    for inner_bag in rhs:
        n += rhs[inner_bag] * (count_bags(rules, inner_bag) + 1)
    return n


def get_test1_rules():
    return '''light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''


def get_test2_rules():
    return '''shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.'''


def get_main_rules():
    return get_file_content('day7_input.txt')


def run_part1(name, rules_str):
    print(' - ' + name + ': ' + str(count_bag_names_containing(parse_rules(rules_str), 'shiny gold')))


def run_part2(name, rules_str):
    print(' - ' + name + ': ' + str(count_bags(parse_rules(rules_str), 'shiny gold')))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test', get_test1_rules())
    run_part1('main', get_main_rules())
    print('Part 2')
    run_part2('test 1', get_test1_rules())
    run_part2('test 2', get_test2_rules())
    run_part2('main  ', get_main_rules())
