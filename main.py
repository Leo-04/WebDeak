from menu import Menu
import os
import sys

dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))

BUTTON_GRID_PATH = f"{dir_path}/server/button_grid.html"
INDEX_PATH = f"{dir_path}/server/index.html"
ERROR_PATH = f"{dir_path}/server/error.html"
ACCESS_DENIED_PATH = f"{dir_path}/server/access_denied.html"
WHITELIST_PATH = f"{dir_path}/server/whitelist.txt"
LAYOUT_PATH = f"{dir_path}/server/layout.json"
STYLE_PATH = f"{dir_path}/UI/style.style"


def main():
    Menu(BUTTON_GRID_PATH, INDEX_PATH, ERROR_PATH, ACCESS_DENIED_PATH, LAYOUT_PATH, WHITELIST_PATH, STYLE_PATH).run()


if __name__ == "__main__":
    main()
