def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_seats_map():
    return '''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''


def get_main_seats_map():
    return get_file_content('day11_input.txt').strip()


class Map:
    def __init__(self, nu, nv, data):
        self.nu = nu
        self.nv = nv
        self.data = data

    def clone(self):
        return Map(self.nu, self.nv, list(self.data))

    def is_valid(self, i, j):
        return i >= 0 and i < self.nu and j >= 0 and j < self.nv

    def get_data(self, i, j):
        if not self.is_valid(i, j):
            return ''
        return self.data[j * self.nu + i]

    def set_data(self, i, j, value):
        self.data[j * self.nu + i] = value

    def is_floor(self, i, j):
        return self.get_data(i, j) == '.'

    def is_empty(self, i, j):
        return self.get_data(i, j) == 'L'

    def is_occupied(self, i, j):
        return self.get_data(i, j) == '#'

    def is_empty_or_floor(self, i, j):
        return self.is_empty(i, j) or self.is_floor(i, j)

    def is_occupied_or_floor(self, i, j):
        return self.is_occupied(i, j) or self.is_floor(i, j)

    def set_empty(self, i, j):
        return self.set_data(i, j, 'L')

    def set_occupied(self, i, j):
        return self.set_data(i, j, '#')

    def __str__(self):
        s = ''
        for j in range(self.nv):
            for i in range(self.nu):
                s += self.get_data(i, j)
            s += '\n'
        return s


def get_map(map_str):
    map_str = map_str.split('\n')
    nu = len(map_str[0])
    nv = len(map_str)
    data = [c for line_str in map_str for c in line_str]
    return Map(nu, nv, data)


adjacent_dirs = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, 1)]


def is_occupied_in_dir(seats_map, i, j, di, dj):
    while True:
        i += di
        j += dj
        if not seats_map.is_valid(i, j) or seats_map.is_empty(i, j):
            return False
        elif seats_map.is_occupied(i, j):
            return True


def get_n_occupied_part_1(seats_map, i, j):
    return sum(1 for (di, dj) in adjacent_dirs if seats_map.is_occupied(i+di, j+dj))


def get_n_occupied_part_2(seats_map, i, j):
    return sum(1 for (di, dj) in adjacent_dirs if is_occupied_in_dir(seats_map, i, j, di, dj))


def do_one_round(seats_map, get_n_occupied_function, max_n_occupied):
    seats_map_copy = seats_map.clone()
    for j in range(seats_map.nv):
        for i in range(seats_map.nu):
            n_occupied = get_n_occupied_function(seats_map, i, j)
            if seats_map.is_empty(i, j) and n_occupied == 0:
                seats_map_copy.set_occupied(i, j)
            elif seats_map.is_occupied(i, j) and n_occupied >= max_n_occupied:
                seats_map_copy.set_empty(i, j)
    return seats_map_copy


def do_all_rounds(seats_map, get_n_occupied_function, max_n_occupied):
    while True:
        next_seats_map = do_one_round(
            seats_map, get_n_occupied_function, max_n_occupied)
        if next_seats_map.data == seats_map.data:
            return seats_map
        seats_map = next_seats_map


def count_occupied(seats_map):
    return sum(1 for c in seats_map.data if c == '#')


def run(label, seats_map_str, get_n_occupied_function, max_n_occupied):
    seats_map = get_map(seats_map_str)
    seats_map = do_all_rounds(
        seats_map, get_n_occupied_function, max_n_occupied)
    print(' - {} {} occupied seats'.format(label, count_occupied(seats_map)))


def run_part1(label, seats_map_str):
    run(label, seats_map_str, get_n_occupied_part_1, 4)


def run_part2(label, seats_map_str):
    run(label, seats_map_str, get_n_occupied_part_2, 5)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_seats_map())
    run_part1('test2:', get_main_seats_map())
    print('Part 2')
    run_part2('test1:', get_test1_seats_map())
    run_part2('test2:', get_main_seats_map())
