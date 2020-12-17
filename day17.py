import itertools


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return '''.#.
..#
###'''


def get_main_input():
    return get_file_content('day17_input.txt').strip()


class CubeMap:
    def __init__(self, ni, nj, nk, nl, data=None):
        self.ni = ni
        self.nj = nj
        self.nk = nk
        self.nl = nl
        self.data = data if data else ['.'] * (ni * nj * nk * nl)

    def get_index(self, i, j, k, l):
        return ((l * self.nk + k) * self.nj + j) * self.ni + i

    def get_data(self, i, j, k, l):
        if i < 0 or i >= self.ni or j < 0 or j >= self.nj or k < 0 or k >= self.nk or l < 0 or l >= self.nl:
            return '.'
        return self.data[self.get_index(i, j, k, l)]

    def set_data(self, i, j, k, l, value):
        self.data[self.get_index(i, j, k, l)] = value

    def is_active(self, i, j, k, l):
        return self.get_data(i, j, k, l) == '#'

    def set_active(self, i, j, k, l, active):
        self.set_data(i, j, k, l, '#' if active else '.')

    def __str__(self):
        s = ''
        for l, k in itertools.product(range(self.nl), range(self.nk)):
            s += '\nk={} l={}\n'.format(k, l)
            for j in range(self.nj):
                for i in range(self.ni):
                    s += self.get_data(i, j, k, l)
                s += '\n'
        return s


def decode_input(map_str):
    map_str = map_str.strip().split('\n')
    ni = len(map_str[0])
    nj = len(map_str)
    data = [c for line_str in map_str for c in line_str]
    return CubeMap(ni, nj, 1, 1, data)


def get_neighbors_indexes(i, j, k, l):
    for dl, dk, dj, di in itertools.product(range(-1, 2), repeat=4):
        if di != 0 or dj != 0 or dk != 0 or dl != 0:
            yield (i + di, j + dj, k + dk, l + dl)


def get_slice_i_indexes(cube_map, i):
    for l, k, j in itertools.product(range(cube_map.nl), range(cube_map.nk), range(cube_map.nj)):
        yield (i, j, k, l)


def get_slice_j_indexes(cube_map, j):
    for i, l, k in itertools.product(range(cube_map.ni), range(cube_map.nl), range(cube_map.nk)):
        yield (i, j, k, l)


def get_slice_k_indexes(cube_map, k):
    for j, i, l in itertools.product(range(cube_map.nj), range(cube_map.ni), range(cube_map.nl)):
        yield (i, j, k, l)


def get_slice_l_indexes(cube_map, l):
    for k, j, i in itertools.product(range(cube_map.nk), range(cube_map.nj), range(cube_map.ni)):
        yield (i, j, k, l)


def count_active_neighbors(cube_map, i, j, k, l):
    return sum(1 for i2, j2, k2, l2 in get_neighbors_indexes(i, j, k, l) if cube_map.is_active(i2, j2, k2, l2))


def has_any_active(cube_map, indexes):
    return any(cube_map.is_active(i, j, k, l) for i, j, k, l in indexes)


def first_last_of(iterable, predicate):
    first = next(value for value in iterable if predicate(value))
    last = next(value for value in reversed(iterable) if predicate(value))
    return (first, last)


def first_last_inactive_slice(cube_map, n, slice_function):
    return first_last_of(range(n), lambda i: has_any_active(cube_map, slice_function(cube_map, i)))


def reduce_map(cube_map):
    first_i, last_i = first_last_inactive_slice(
        cube_map, cube_map.ni, get_slice_i_indexes)
    first_j, last_j = first_last_inactive_slice(
        cube_map, cube_map.nj, get_slice_j_indexes)
    first_k, last_k = first_last_inactive_slice(
        cube_map, cube_map.nk, get_slice_k_indexes)
    first_l, last_l = first_last_inactive_slice(
        cube_map, cube_map.nl, get_slice_l_indexes)

    ni = last_i - first_i + 1
    nj = last_j - first_j + 1
    nk = last_k - first_k + 1
    nl = last_l - first_l + 1

    reduced_map = CubeMap(ni, nj, nk, nl)
    for l, k, j, i in itertools.product(range(nl), range(nk), range(nj), range(ni)):
        if cube_map.is_active(i + first_i, j + first_j, k + first_k, l + first_l):
            reduced_map.set_active(i, j, k, l, True)
    return reduced_map


def next_cycle(cube_map, use_l_dimension):
    ni = cube_map.ni
    nj = cube_map.nj
    nk = cube_map.nk
    nl = cube_map.nl
    dl = 1 if use_l_dimension else 0
    next_map = CubeMap(ni + 2, nj + 2, nk + 2, nl + 2 * dl)

    for l, k, j, i in itertools.product(range(nl + 2 * dl), range(nk + 2), range(nj + 2), range(ni + 2)):
        n_active_neighbors = count_active_neighbors(
            cube_map, i - 1, j - 1, k - 1, l - dl)
        active = cube_map.is_active(i - 1, j - 1, k - 1, l - dl)
        if active:
            if n_active_neighbors != 2 and n_active_neighbors != 3:
                active = False
        else:
            if n_active_neighbors == 3:
                active = True
        next_map.set_active(i, j, k, l, active)

    next_map = reduce_map(next_map)
    return next_map


def run(label, input_str, use_l_dimension):
    cube_map = decode_input(input_str)
    for _ in range(6):
        cube_map = next_cycle(cube_map, use_l_dimension)
    n_active_cubes = sum(1 for c in cube_map.data if c == '#')
    print(' - {} active cubes {}'.format(label, n_active_cubes))


def run_part1(label, input_str):
    run(label, input_str, False)


def run_part2(label, input_str):
    run(label, input_str, True)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test1:', get_test1_input())
    run_part2('main: ', get_main_input())
