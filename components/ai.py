import tcod as libtcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        monster = self.owner

        if fov_map.fov[monster.y, monster.x]:
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)
            elif target.fighter.hp > 0:
                results.extend(monster.fighter.attack(target))

        return results
