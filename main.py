import sys
import os
import glob
from input_handlers import handle_keys

import tcod as libtcod


os.environ["path"] = os.path.dirname(sys.executable) + ";" + os.environ["path"]
DATA_FOLDER = "data"
FONT_FILE = os.path.join(DATA_FOLDER, "dejavu10x10_gs_tc.png")


def main():
    screen_width = 80
    screen_height = 50

    player_x = int(screen_width/2)
    player_y = int(screen_height/2)

    libtcod.console_set_custom_font(FONT_FILE, libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(screen_width, screen_height, "tutorial", False)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_put_char(0, player_x, player_y, "@", libtcod.BKGND_NONE)
        libtcod.console_flush()

        action = handle_keys(key)
        # key = libtcod.console_check_for_keypress()

        move = action.get("move")
        exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        if move:
            dx, dy = move
            player_x += dx
            player_y += dy

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
