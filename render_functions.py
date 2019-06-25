import tcod as libtcod

def render_all(src_con, dst_con, entities, game_map, screen_width, screen_height, colors):
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                libtcod.console_set_char_background(src_con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
            else:
                libtcod.console_set_char_background(src_con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    for entity in entities:
        draw_entity(src_con, entity)

    src_con.blit(dst_con)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    con.default_fg = entity.color
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
