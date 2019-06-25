import tcod as libtcod

def render_all(src_con, dst_con, entities, game_map, screen_width, screen_height, colors):
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                src_con.tiles['bg'][x, y, :3] = colors.get('dark_wall')
            else:
                src_con.tiles['bg'][x, y, :3] = colors.get('dark_ground')

    for entity in entities:
        draw_entity(src_con, entity)

    src_con.blit(dst_con)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity):
    con.tiles['fg'][entity.x, entity.y, :3] = entity.color
    # Index this array with console.ch[i, j]  # order='C' or console.ch[x, y]  # order='F'.
    con.tiles['ch'][entity.x, entity.y] = ord(entity.char)

def clear_entity(con, entity):
    con.tiles['ch'][entity.x, entity.y] = ord(' ')
