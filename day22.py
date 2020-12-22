def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10'''


def get_test2_input():
    return '''Player 1:
43
19

Player 2:
2
29
14'''


def get_main_input():
    return get_file_content('day22_input.txt')


def decode_input(input_str):
    return ([int(card_str) for card_str in deck_str[10:].split('\n')] for deck_str in input_str.strip().split('\n\n'))


def check_deck_history(history, deck):
    deck = tuple(deck)
    result = deck in history
    history.add(deck)
    return result


def rules_part1(card1, card2, deck1, deck2):
    return card1 > card2


def rules_part2(card1, card2, deck1, deck2):
    if card1 > len(deck1) or card2 > len(deck2):
        return card1 > card2
    return run_game(deck1[:card1], deck2[:card2], rules_part2)


def run_game(deck1, deck2, rules):
    deck_history1 = set()
    deck_history2 = set()
    while len(deck1) and len(deck2):
        if check_deck_history(deck_history1, deck1) or check_deck_history(deck_history2, deck2):
            return True
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)
        if rules(card1, card2, deck1, deck2):
            deck1.append(card1)
            deck1.append(card2)
        else:
            deck2.append(card2)
            deck2.append(card1)

    return bool(len(deck1))


def compute_score(deck):
    return sum((i + 1) * card for i, card in enumerate(reversed(deck)))


def run(label, input_str, rules):
    deck1, deck2 = decode_input(input_str)
    result = run_game(deck1, deck2, rules)
    winner_deck = deck1 if result else deck2
    print(' - {} {}'.format(label, compute_score(winner_deck)))


def run_part1(label, input_str):
    run(label, input_str, rules_part1)


def run_part2(label, input_str):
    run(label, input_str, rules_part2)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test1:', get_test1_input())
    run_part2('test2:', get_test2_input())
    run_part2('main: ', get_main_input())
