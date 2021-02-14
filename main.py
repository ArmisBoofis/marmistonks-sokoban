"""
This module contains the main program of the Mario Sokoban.
Specifically, it displays the different views of the game (menus,
level editor, the game itself...)
"""

import pygame
from game import GameManager
from main_menu import MainMenuManager
from constants import WINDOW_SIZE, WINDOW_TITLE, WINDOW_ICON_PATH, GAME_VIEW, MAIN_MENU_VIEW

if __name__ == '__main__':
    pygame.init()

    # Initialization of the window
    pygame.display.set_caption(WINDOW_TITLE) # Title
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.DOUBLEBUF | pygame.HWSURFACE) # Size
    pygame.display.set_icon(pygame.image.load(WINDOW_ICON_PATH).convert_alpha()) # Icon

    # Currently displayed view
    view = MAIN_MENU_VIEW

    main_menu = MainMenuManager(screen) # Initialization of the main menu
    game = GameManager(screen) # Initialization of the game

    # Main loop
    while True:
        # Depending on the current view, we update the display
        if view == MAIN_MENU_VIEW:
            view = main_menu.mainloop()

        elif view == GAME_VIEW:
            game.parse('level_10.txt', 0)
            game.mainloop()

    pygame.quit()
