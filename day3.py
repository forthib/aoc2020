def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_map():
    return '''..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#'''


def get_main_map():
    return get_file_content('day3_input.txt').strip()


class Map:
    def __init__(self, map_str):
        map_str = map_str.split('\n')
        self.nu = len(map_str[0])
        self.nv = len(map_str)
        self.data = [c for line_str in map_str for c in line_str]

    def is_tree(self, i, j):
        i = i % self.nu
        return self.data[j * self.nu + i] == '#'


def count_trees(tree_map, slope_u, slope_v):
    return sum(1 for index in range(int(tree_map.nv / slope_v)) if tree_map.is_tree(index * slope_u, index * slope_v))


def multiply(values):
    result = 1
    for value in values:
        result *= value
    return result


def run_part1(name, tree_map_str):
    tree_map = Map(tree_map_str)
    n_trees = count_trees(tree_map, 3, 1)
    print(' - {} {} trees'.format(name, n_trees))


def run_part2(name, tree_map_str):
    tree_map = Map(tree_map_str)
    n_trees_list = [count_trees(tree_map, slope_u, slope_v) for i, (
        slope_u, slope_v) in enumerate([(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])]
    print(' - {} trees {} answer {}'.format(name,
                                            n_trees_list, multiply(n_trees_list)))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_map())
    run_part1('main: ', get_main_map())
    print('Part 2')
    run_part2('test1:', get_test1_map())
    run_part2('main: ', get_main_map())
