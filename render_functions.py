import tcod as libtcod

def render_all(src_con, dst_con,entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        src_con.tiles['bg'][x, y, :3] = colors.get('light_wall')
                    else:
                        src_con.tiles['bg'][x, y, :3] = colors.get('light_ground')

                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        src_con.tiles['bg'][x, y, :3] = colors.get('dark_wall')
                    else:
                        src_con.tiles['bg'][x, y, :3] = colors.get('dark_ground')

    for entity in entities:
        draw_entity(src_con, entity, fov_map)

    src_con.blit(dst_con)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        con.tiles['fg'][entity.x, entity.y, :3] = entity.color
        # Index this array with console.ch[i, j]  # order='C' or console.ch[x, y]  # order='F'.
        con.tiles['ch'][entity.x, entity.y] = ord(entity.char)

def clear_entity(con, entity):
    con.tiles['ch'][entity.x, entity.y] = ord(' ')
