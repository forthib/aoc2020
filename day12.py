def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_instructions():
    return '''F10
N3
F7
R90
F11'''


def get_main_instructions():
    return get_file_content('day12_input.txt').strip()


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self):
        return abs(self.x) + abs(self.y)


def rotate(coord, angle):
    sign = 1 if angle > 0 else -1
    for _ in range(int(abs(angle) / 90)):
        x = - sign * coord.y
        y = sign * coord.x
        coord.x = x
        coord.y = y


def apply_instr(instr, ship, waypoint, nsew_coord):
    action = instr[0]
    value = int(instr[1:])
    if action == 'N':
        nsew_coord.y += value
    elif action == 'S':
        nsew_coord.y -= value
    elif action == 'E':
        nsew_coord.x += value
    elif action == 'W':
        nsew_coord.x -= value
    elif action == 'L':
        rotate(waypoint, value)
    elif action == 'R':
        rotate(waypoint, -value)
    elif action == 'F':
        ship.x += waypoint.x * value
        ship.y += waypoint.y * value


def apply_instr_part1(instr, ship, waypoint):
    apply_instr(instr, ship, waypoint, ship)


def apply_instr_part2(instr, ship, waypoint):
    apply_instr(instr, ship, waypoint, waypoint)


def run(label, way_point, instructions_str, apply_instr_function):
    ship = Coord(0, 0)
    for instr in instructions_str.split('\n'):
        apply_instr_function(instr, ship, way_point)
    print(' - {} position ({}, {}) distance {}'.format(label,
                                                       ship.x, ship.y, ship.distance()))


def run_part1(label, instructions_str):
    run(label, Coord(1, 0), instructions_str, apply_instr_part1)


def run_part2(label, instructions_str):
    run(label, Coord(10, 1), instructions_str, apply_instr_part2)


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_instructions())
    run_part1('main: ', get_main_instructions())
    print('Part 2')
    run_part2('test1:', get_test1_instructions())
    run_part2('main: ', get_main_instructions())
