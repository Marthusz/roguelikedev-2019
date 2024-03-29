import tcod as libtcod
import math

from render_functions import RenderOrder

class Entity:
    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        dx = int(round(dx/distance))
        dy = int(round(dy/distance))

        if not (game_map.is_blocked(self.x+dx, self.y+dy) or get_blocking_entities_at_location(entities, self.x+dx, self.y+dy)):
            self.move(dx, dy)

    def move_astar(self, target, entities, game_map):
        fov = libtcod.map.Map(game_map.width, game_map.height)

        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                fov.transparent[y1, x1] = not game_map.tiles[x1][y1].block_sight
                fov.walkable[y1, x1] = not game_map.tiles[x1][y1].blocked

        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                fov.transparent[entity.y, entity.x] = True
                fov.walkable[entity.y, entity.x] = False

        my_path = libtcod.path_new_using_map(fov, 1.41)

        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y
        else:
            self.move_towards(target.x, target.y, game_map, entities)

        # DeprecationWarning: libtcod objects are deleted automatically.
        # libtcod.path_delete(my_path)

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
