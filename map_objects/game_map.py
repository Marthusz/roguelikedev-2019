from random import randint, sample, shuffle

from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = []
        num_rooms = 0

        print('Generating rooms...')

        for r in range(max_rooms):
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            if w%2 == 0:
                w -= 1

            if h%2 == 0:
                h -= 1

            x = randint(1, map_width - w)
            y = randint(1, map_height - h)

            if x%2 == 0:
                x -= 1

            if y%2 == 0:
                y -= 1

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    player.x = new_x
                    player.y = new_y

                rooms.append(new_room)
                num_rooms += 1

        print("Generating corridors...")
        grow_directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for y in range(1, map_height, 2):
            for x in range(1, map_width, 2):
                if self.tiles[x][y].blocked:
                    self.tiles[x][y].blocked = False
                    self.tiles[x][y].block_sight = False
                    print('Starting grow from ({0}, {1})'.format(x, y))

                    # List for growable cells
                    cells = []
                    cells.append((x, y))

                    while len(cells) > 0:
                        shuffle(cells)
                        # Get first cell
                        cell = cells[0]

                        # Calculate the possible grow directions
                        directions = []

                        for dir in grow_directions:
                            movement = (cell[0] + dir[0]*3, cell[1] + dir[1]*3)
                            # Checking if possible move is in bounds
                            if movement[0] >= 1 and movement[0] < map_width and movement[1] >= 1 and movement[1] < map_height:
                                if self.tiles[cell[0] + dir[0]*2][cell[1] + dir[1]*2].block_sight:
                                    directions.append(dir)

                        if len(directions) != 0:
                            choice = sample(directions, 1)[0]
                            self.tiles[cell[0]+choice[0]][cell[1]+choice[1]].blocked = False
                            self.tiles[cell[0]+choice[0]][cell[1]+choice[1]].block_sight = False
                            self.tiles[cell[0]+choice[0]*2][cell[1]+choice[1]*2].blocked = False
                            self.tiles[cell[0]+choice[0]*2][cell[1]+choice[1]*2].block_sight = False
                            cells.append((cell[0]+choice[0]*2, cell[1]+choice[1]*2))
                        else:
                            cells = cells[1:len(cells)]


        print("Map finished!")
        print('Number of rooms: {0}'.format(len(rooms)))

    def create_room(self, room):
        for x in range(room.x1, room.x2):
            for y in range(room.y1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2)+1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
