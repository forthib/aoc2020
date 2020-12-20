import itertools


def get_file_content(filename):
    with open(filename) as f:
        return f.read()


def get_test1_input():
    return get_file_content('day20_test.txt')


def get_main_input():
    return get_file_content('day20_input.txt')


def get_see_monster_input():
    return '''                  # #    ##    ##    ### #  #  #  #  #  #   '''


class Image:
    def __init__(self, ni, nj, data=None):
        self.ni = ni
        self.nj = nj
        self.data = data if data else [' '] * (ni * nj)

    def get_value(self, i, j):
        return self.data[j * self.ni + i]

    def set_value(self, i, j, value):
        self.data[j * self.ni + i] = value

    def __str__(self):
        s = ''
        for j in range(self.nj):
            for i in range(self.ni):
                s += str(self.get_value(i, j))
            s += '\n'
        return s


def decode_tile(tile_str):
    title_str, data_str = tile_str.split(':\n')
    tile_id = int(title_str[5:])
    tile = Image(10, 10, data_str.replace('\n', '').strip())
    return (tile_id, tile)


def decode_input(input_str):
    return dict([decode_tile(tile_str) for tile_str in input_str.strip().split('\n\n')])


def get_see_monster_image():
    return Image(20, 3, get_see_monster_input())


def rotated(image, edge_index):
    if edge_index == 0:
        return image
    else:
        result = Image(image.nj, image.ni)
        for j, i in itertools.product(range(image.nj), range(image.ni)):
            result.set_value(j, image.ni - i - 1, image.get_value(i, j))
        return rotated(result, edge_index - 1)


def flipped(image):
    result = Image(image.ni, image.nj)
    for j, i in itertools.product(range(image.nj), range(image.ni)):
        result.set_value(image.ni - i - 1, j, image.get_value(i, j))
    return result


def get_edges(tile):
    ni = tile.ni
    nj = tile.nj
    edge0X = ''.join([tile.get_value(0, j) for j in range(10)])
    edge1X = ''.join([tile.get_value(ni - 1, j) for j in range(10)])
    edgeX0 = ''.join([tile.get_value(i, 0) for i in range(10)])
    edgeX1 = ''.join([tile.get_value(i, nj - 1) for i in range(10)])
    return [edgeX0, edge1X, edgeX1[::-1], edge0X[::-1]]


def make_edge_to_tile_ids(tiles):
    result = dict()
    for tile_id, tile in tiles.items():
        for i, fwd_edge in enumerate(get_edges(tile)):
            rev_edge = fwd_edge[::-1]
            if fwd_edge not in result:
                result[fwd_edge] = []
            if rev_edge not in result:
                result[rev_edge] = []
            result[fwd_edge].append((tile_id, i, True))
            result[rev_edge].append((tile_id, i, False))
    return result


def count_shared_edges(tile, edge_to_tile_ids):
    return sum(1 for edge in get_edges(tile) if len(edge_to_tile_ids[edge]) > 1)


def find_corner_tile_ids(tiles, edge_to_tile_ids):
    return [tile_id for tile_id, tile in tiles.items() if count_shared_edges(tile, edge_to_tile_ids) == 2]


def find_line_tiles_id(tiles, edge_to_tile_ids, tile_id, edge_index, forward):
    yield (tile_id, edge_index, forward)
    while True:
        edge_index = (edge_index + 2) % 4
        edge = get_edges(tiles[tile_id])[edge_index]
        forward = not forward
        edge = edge if forward else edge[::-1]
        if len(edge_to_tile_ids[edge]) == 1:
            return
        tile_id, edge_index, forward = next(
            (ti, ei, fwd) for ti, ei, fwd in edge_to_tile_ids[edge] if ti != tile_id)
        yield (tile_id, edge_index, forward)


def get_arranged_tile_ids(tiles, edge_to_tile_ids):
    corner_tile_id = find_corner_tile_ids(tiles, edge_to_tile_ids)[0]
    corner_u_edge_index, corner_v_edge_index = (i for i, edge in enumerate(
        get_edges(tiles[corner_tile_id])) if len(edge_to_tile_ids[edge]) == 1)

    first_column = list(find_line_tiles_id(tiles, edge_to_tile_ids, corner_tile_id,
                                           corner_u_edge_index, corner_u_edge_index == (corner_v_edge_index + 1) % 4))

    result = list()
    for first_tile_id, first_u_edge_index, first_forward in first_column:
        if first_forward:
            first_v_edge_index = (first_u_edge_index + 3) % 4
        else:
            first_v_edge_index = (first_u_edge_index + 1) % 4
        for tile_id, edge_index, forward in find_line_tiles_id(tiles, edge_to_tile_ids, first_tile_id, first_v_edge_index, first_forward):
            if forward:
                result.append((tile_id, (edge_index + 1) % 4, True))
            else:
                result.append((tile_id, (edge_index + 3) % 4, False))

    ni = len(first_column)
    nj = len(result) // ni
    return Image(ni, nj, result)


def assemble_image(tiles, arranged_tile_ids):
    assembled_image = Image(8 * arranged_tile_ids.ni,
                            8 * arranged_tile_ids.nj)
    for j, i in itertools.product(range(arranged_tile_ids.nj), range(arranged_tile_ids.ni)):
        tile_id, edge_index, forward = arranged_tile_ids.get_value(i, j)
        tile_image = tiles[tile_id]
        tile_image = rotated(tile_image, edge_index)
        tile_image = tile_image if forward else flipped(tile_image)
        for jx, ix in itertools.product(range(8), range(8)):
            assembled_image.set_value(
                i * 8 + ix, j * 8 + jx, tile_image.get_value(ix + 1, jx + 1))
    return assembled_image


def is_see_monster(image, i0, j0, sm):
    for j, i in itertools.product(range(sm.nj), range(sm.ni)):
        if sm.get_value(i, j) == '#' and image.get_value(i0 + i, j0 + j) != '#':
            return False
    return True


def remove_see_monster(image, i0, j0, sm):
    for j, i in itertools.product(range(sm.nj), range(sm.ni)):
        if sm.get_value(i, j) == '#':
            image.set_value(i0 + i, j0 + j, '.')


def count_see_monsters(image):
    sm = get_see_monster_image()
    cpt = 0
    roughness_image = Image(image.ni, image.nj, list(image.data))
    for j, i in itertools.product(range(image.nj - sm.nj), range(image.ni - sm.nj)):
        if is_see_monster(image, i, j, sm):
            cpt += 1
            remove_see_monster(roughness_image, i, j, sm)
    roughness = sum(1 for c in roughness_image.data if c == '#')
    return (cpt, roughness)


def multiply(values):
    result = 1
    for value in values:
        result *= value
    return result


def run_part1(label, input_str):
    tiles = decode_input(input_str)
    edge_to_tile_ids = make_edge_to_tile_ids(tiles)
    corner_tile_ids = find_corner_tile_ids(tiles, edge_to_tile_ids)
    print(' - {} tiles {} multiplied {}'.format(label,
                                                corner_tile_ids, multiply(corner_tile_ids)))


def run_part2(label, input_str):
    tiles = decode_input(input_str)
    edge_to_tile_ids = make_edge_to_tile_ids(tiles)
    arranged_tile_ids = get_arranged_tile_ids(tiles, edge_to_tile_ids)
    image = assemble_image(tiles, arranged_tile_ids)

    for edge_index, forward in itertools.product(range(4), [True, False]):
        transformed_image = rotated(image, edge_index)
        transformed_image = transformed_image if forward else flipped(
            transformed_image)
        n, roughness = count_see_monsters(transformed_image)
        if n > 0:
            print(' - {} {} see monsters -> roughness {}'.format(label, n, roughness))


if __name__ == "__main__":
    print('Part 1')
    run_part1('test1:', get_test1_input())
    run_part1('main: ', get_main_input())
    print('Part 2')
    run_part2('test1:', get_test1_input())
    run_part2('main: ', get_main_input())
