import tcod as libtcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner

        if fov_map.fov[monster.y, monster.x]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)
            elif target.fighter.hp > 0:
                print('The {0} insults you! Your ego is damaged!'.format(monster.name))