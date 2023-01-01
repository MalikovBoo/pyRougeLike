import sys
import os
import glob
from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap

import tcod as libtcod


os.environ["path"] = os.path.dirname(sys.executable) + ";" + os.environ["path"]
DATA_FOLDER = "data"
FONT_FILE = os.path.join(DATA_FOLDER, "dejavu10x10_gs_tc.png")


def main():
    screen_width = 80
    screen_height = 50
    map_width = 80
    map_height = 45
    max_rooms = 30
    room_min_size = 6
    room_max_size = 10

    colors = {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150)
    }
    game_map = GameMap(map_width, map_height)
    player = Entity(int(screen_width/2), int(screen_height/2), "@", libtcod.white)
    npc = Entity(int(screen_width/2), int(screen_height/2) - 5, "Q", libtcod.yellow)
    entities = [player, npc]

    game_map.make_map(room_min_size, room_max_size, map_width, map_height, max_rooms, player)

    libtcod.console_set_custom_font(FONT_FILE, libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, "tutorial", False)
    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, game_map, entities, screen_width, screen_height, colors)
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x+dx, player.y+dy):
                player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
