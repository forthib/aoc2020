from lark import Lark, Tree, Token


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''1 + 2 * 3 + 4 * 5 + 6'''


def get_test2_input():
    return '''1 + (2 * 3) + (4 * (5 + 6))'''


def get_test3_input():
    return '''2 * 3 + (4 * 5)'''


def get_test4_input():
    return '''5 + (8 * 3 + 9 + 3 * 4 * 3)'''


def get_test5_input():
    return '''5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'''


def get_test6_input():
    return '''((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'''


def get_main_input():
    return get_file_content('day18_input.txt').strip()


def eval(tree):
    if tree.data in ['start', 'sum', 'product', 'atom']:
        return eval(tree.children[0])
    elif tree.data == 'add':
        return eval(tree.children[0]) + eval(tree.children[1])
    elif tree.data == 'mul':
        return eval(tree.children[0]) * eval(tree.children[1])
    elif tree.data == 'number':
        return int(tree.children[0])


def run(label, input_str, grammar_str):
    grammar = Lark(grammar_str)
    value = sum(eval(grammar.parse(expr_str))
                for expr_str in input_str.strip().split('\n'))
    print(' - {} {}'.format(label, value))


def run_part1(label, input_str):
    grammar_str = '''
    start: sum
    sum: atom
        | sum "+" atom  -> add
        | sum "*" atom  -> mul
    atom: NUMBER        -> number
        | "(" sum ")"
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
    '''
    run(label, input_str, grammar_str)


def run_part2(label, input_str):
    grammar_str = '''
    start: product
    product: sum
        | sum "*" product -> mul
    sum: atom
        | sum "+" atom    -> add
    atom: NUMBER          -> number
        | "(" product ")"
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
    '''
    run(label, input_str, grammar_str)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('test2:', get_test2_input())
    run_part1('test3:', get_test3_input())
    run_part1('test4:', get_test4_input())
    run_part1('test5:', get_test5_input())
    run_part1('test6:', get_test6_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test1:', get_test1_input())
    run_part2('test2:', get_test2_input())
    run_part2('test3:', get_test3_input())
    run_part2('test4:', get_test4_input())
    run_part2('test5:', get_test5_input())
    run_part2('test6:', get_test6_input())
    run_part2('main: ', get_main_input())
