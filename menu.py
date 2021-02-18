"""
Module managing the menus, from which the user can select the views,
the levels, the characters...
"""

import sys
import pygame
from os import listdir
from user_interface import ImageSprite, TextButton
from constants import (WINDOW_SIZE, MENU_BACKGROUND_COLOR, MAIN_MENU_BUTTONS,
                       MAIN_MENU_BUTTONS_SIZE, MENU_BUTTONS_MARGIN,
                       MAIN_MENU_BUTTONS_Y, MAIN_MENU_SPRITES, LEVEL_MENU_BUTTONS_SIZE,
                       LEVEL_MENU_LEVELS_PATH)


class MenuManager():
    """Generic class managing a menu with a set of buttons and sprites to display"""

    def __init__(self, screen, buttons, sprites):
        """Constructor method. It initializes the image of the menu and the buttons."""

        # First, we store the screen as an attribute
        self.screen = screen

        # Then we can initialize the background of the menu
        self.background = pygame.Surface(WINDOW_SIZE)
        self.background.fill(MENU_BACKGROUND_COLOR)

        # We create a sprite group for the buttons
        self.buttons_group = pygame.sprite.Group()
        self.buttons_actions = []

        for button in buttons:
            self.buttons_group.add(button[0])
            self.buttons_actions.append(button[1])

        # Then we create a sprite group for the other sprites
        self.sprites_group = pygame.sprite.Group()

        for sprite in sprites:
            self.sprites_group.add(sprite)

    def mainloop(self):
        """Method called to invoke the main loop of the menu (opening it).
        It returns a view code, which corresponds to the next view to be displayed."""

        while True:
            # Events processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # If the mouse moves, we have to update the buttons
                if event.type == pygame.MOUSEMOTION:
                    self.buttons_group.update(pygame.mouse.get_pos())

                # If the mouse is clicked, we have to check for all the buttons
                # If one is clicked, we will change the view accordingly
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()

                    for index, button in enumerate(self.buttons_group):
                        if button.collides(mouse_position):
                            return self.buttons_actions[index]

            # We draw all the elements of the menu
            self.screen.blit(self.background, (0, 0))
            self.buttons_group.draw(self.screen)
            self.sprites_group.draw(self.screen)

            # Updating the screen
            pygame.display.flip()

########################### Main Menu ##############################


def get_main_menu_elements():
    """Function returning the buttons and
    sprites displayed in the main menu."""

    # Initialization of the buttons
    main_menu_buttons = []
    button_x, button_y = (
        WINDOW_SIZE[1] - MAIN_MENU_BUTTONS_SIZE[0]) / 2, MAIN_MENU_BUTTONS_Y

    for button_info in MAIN_MENU_BUTTONS:
        main_menu_buttons.append((TextButton(
            pygame.Rect(
                (button_x, button_y),
                MAIN_MENU_BUTTONS_SIZE
            ),
            button_info[0]
        ), button_info[1]))

        button_y += MAIN_MENU_BUTTONS_SIZE[1] + MENU_BUTTONS_MARGIN

    # Initialization of the sprites
    main_menu_sprites = []

    for (image_path, coords) in MAIN_MENU_SPRITES:
        main_menu_sprites.append(ImageSprite(image_path, coords))

    # We return the diferent elements we have created
    return (main_menu_buttons, main_menu_sprites)

########################### Level Menu #############################


def get_level_menu_elements():
    """Function returning the buttons
    displayed in the level menu."""

    # List of the files contained in the levels directory
    # We sort it, so that the levels are in ascending order
    levels_list = sorted(listdir(LEVEL_MENU_LEVELS_PATH))

    # List of all the buttons of the level menu
    level_menu_buttons = []
    nb_horizontal_buttons = WINDOW_SIZE[0] // (
        LEVEL_MENU_BUTTONS_SIZE[0] + MENU_BUTTONS_MARGIN)
    x_value = (WINDOW_SIZE[0] - nb_horizontal_buttons *
               (LEVEL_MENU_BUTTONS_SIZE[0] + MENU_BUTTONS_MARGIN) + MENU_BUTTONS_MARGIN) // 2

    # For each file, we create a button
    for index, level in enumerate(levels_list):
        level_menu_buttons.append((TextButton(
            pygame.Rect(
                (x_value + (index % nb_horizontal_buttons * (LEVEL_MENU_BUTTONS_SIZE[0] + MENU_BUTTONS_MARGIN)),
                 (index // nb_horizontal_buttons) * (LEVEL_MENU_BUTTONS_SIZE[1] + MENU_BUTTONS_MARGIN) + MENU_BUTTONS_MARGIN),
                LEVEL_MENU_BUTTONS_SIZE
            ),
            str(index),
        ), '{}/{}'.format(LEVEL_MENU_LEVELS_PATH, level)))

    return level_menu_buttons
