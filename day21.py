def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)'''


def get_main_input():
    return get_file_content('day21_input.txt')


def decode_line(line_str):
    food_str, allergen_str = line_str.split(' (contains ')
    food = food_str.split(' ')
    allergens = allergen_str[:-1].split(', ')
    return (food, allergens)


def decode_input(input_str):
    return [decode_line(line_str) for line_str in input_str.strip().split('\n')]


def make_allergen_map(foods):
    allergen_map = dict()
    for food, allergens in foods:
        for allergen in allergens:
            if allergen not in allergen_map:
                allergen_map[allergen] = set(food)
            else:
                allergen_map[allergen] &= set(food)
    return allergen_map


def reduce_one(allergen_map):
    unique_ingredients = set([list(ingredients)[
                             0] for allergen, ingredients in allergen_map.items() if len(ingredients) == 1])
    reduced = False
    for ingredients in allergen_map.values():
        if len(ingredients) > 1:
            ingredients -= unique_ingredients
            reduced = True
    return reduced


def reduce_all(allergen_map):
    while True:
        if not reduce_one(allergen_map):
            break


def make_reduced_allergen_map(foods):
    allergen_map = make_allergen_map(foods)
    reduce_all(allergen_map)
    return allergen_map


def make_ingredient_map(foods):
    allergen_map = make_reduced_allergen_map(foods)
    return dict([(list(ingredients)[0], allergen) for allergen, ingredients in allergen_map.items() if len(ingredients) == 1])


def run_part1(label, input_str):
    foods = decode_input(input_str)
    ingredient_map = make_ingredient_map(foods)

    n = sum(1 for food, _ in foods for ing in food if ing not in ingredient_map)
    print(' - {} {} allergen free ingredients'.format(label, n))


def run_part2(label, input_str):
    foods = decode_input(input_str)
    ingredient_map = make_ingredient_map(foods)

    ingredient_list = list(ingredient_map.items())
    ingredient_list = [ingredient for ingredient, _ in sorted(
        ingredient_list, key=lambda value: value[1])]
    print(' - {} ingredient list {}'.format(label, ','.join(ingredient_list)))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test1:', get_test1_input())
    run_part2('main: ', get_main_input())
