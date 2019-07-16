import tcod as libtcod
import tcod.event as event

from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
from random import shuffle

import warnings
warnings.filterwarnings("default", category=DeprecationWarning)

def main():
    screen_width = 61
    screen_height = 40
    map_width = screen_width
    map_height = screen_height - 3

    room_max_size = 13
    room_min_size = 5
    max_rooms = 100

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': libtcod.Color(0, 0, 50),
        'dark_ground': libtcod.Color(25, 25, 50),
        'light_wall': libtcod.Color(100, 100, 50),
        'light_ground': libtcod.Color(200, 200, 200)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '\u263A', libtcod.black, 'player', blocks=True, fighter=fighter_component)
    entities = [player]

    libtcod.console_set_custom_font('Aesomatica_16x16.png', libtcod.FONT_LAYOUT_CP437)

    root_console = libtcod.console_init_root(screen_width, screen_height, 'libtcod tutorial revised', False, renderer=libtcod.RENDERER_OPENGL2, vsync=True, order='F')
    con = libtcod.console.Console(screen_width, screen_height, order='F')

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    game_state = GameStates.PLAYER_TURN

    while True:
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm)

        render_all(con, root_console, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors)
        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        for ev in event.get():
            if ev.type == 'QUIT':
                raise SystemExit()
            elif ev.type == 'KEYDOWN':
                action = handle_keys(ev)

                move = action.get('move')
                fullscreen = action.get('fullscreen')
                exit = action.get('exit')

                player_turn_results = []


                if move and game_state == GameStates.PLAYER_TURN:
                    dx, dy = move
                    destination_x = player.x + dx
                    destination_y = player.y + dy

                    if not game_map.is_blocked(destination_x, destination_y):
                        target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                        if target:
                            player_turn_results.extend(player.fighter.attack(target))
                        else:
                            player.move(dx, dy)
                            fov_recompute = True

                        game_state = GameStates.ENEMY_TURN

                if exit:
                    raise SystemExit()

                if fullscreen:
                    libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

                for player_turn_result in player_turn_results:
                    message = player_turn_result.get('message')
                    dead_entity = player_turn_result.get('dead')

                    if message:
                        print(message)

                    if dead_entity:
                        if dead_entity == player:
                            message, game_state = kill_player(dead_entity)
                        else:
                            message = kill_monster(dead_entity)

                        print(message)

                        if game_state == GameStates.PLAYER_DEAD:
                            break

                if game_state == GameStates.ENEMY_TURN:
                    for entity in entities[1:]:
                        if entity.ai:
                            enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                            for enemy_turn_result in enemy_turn_results:
                                message = enemy_turn_result.get('message')
                                dead_entity = enemy_turn_result.get('dead')

                                if message:
                                    print(message)

                                if dead_entity:
                                    if dead_entity == player:
                                        message, game_state = kill_player(dead_entity)
                                    else:
                                        message = kill_monster(dead_entity)

                                    print(message)

                                    if game_state == GameStates.PLAYER_DEAD:
                                        break

                    else:
                        game_state = GameStates.PLAYER_TURN


if __name__ == '__main__':
    main()
