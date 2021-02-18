"""
This module contains the main program of the Mario Sokoban.
Specifically, it displays the different views of the game (menus,
level editor, the game itself...)
"""

import pygame
from game import GameManager
from menu import MenuManager, get_main_menu_elements, get_level_menu_elements
from constants import (WINDOW_SIZE, WINDOW_TITLE, WINDOW_ICON_PATH,
                       GAME_VIEW, MAIN_MENU_VIEW, LEVEL_CHOICE_MENU_VIEW)

if __name__ == '__main__':
    pygame.init()

    # Initialization of the window
    pygame.display.set_caption(WINDOW_TITLE)  # Title
    screen = pygame.display.set_mode(
        WINDOW_SIZE, pygame.DOUBLEBUF | pygame.HWSURFACE)  # Size
    pygame.display.set_icon(pygame.image.load(
        WINDOW_ICON_PATH).convert_alpha())  # Icon

    # Currently displayed view
    view = MAIN_MENU_VIEW

    # Initialization of the main menu
    (main_menu_buttons, main_menu_sprites) = get_main_menu_elements()
    main_menu = MenuManager(screen, main_menu_buttons, main_menu_sprites)

    # Initialization of the levels menu
    level_menu_buttons = get_level_menu_elements()
    level_menu = MenuManager(screen, level_menu_buttons, [])

    # Initialisation of the game
    game = GameManager(screen)

    # Main loop
    while True:
        # Depending on the current view, we update the display
        if view == MAIN_MENU_VIEW:
            view = main_menu.mainloop()

        elif view == LEVEL_CHOICE_MENU_VIEW:
            view = GAME_VIEW
            next_level = level_menu.mainloop()

        elif view == GAME_VIEW:
            game.parse(next_level, 0)
            game.mainloop()

    pygame.quit()
