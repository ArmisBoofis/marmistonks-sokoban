"""
Module managing the main menu, from which the user can select the views to be displayed,
such as the game view, the editor view...
"""

import sys
import pygame
from user_interface import Button
from constants import (WINDOW_SIZE, MENU_BACKGROUND_COLOR, MAIN_MENU_BUTTONS,
                       MENU_BUTTONS_HEIGHT, MENU_BUTTONS_WIDTH, MENU_BUTTONS_Y_MARGIN,
                       MAIN_MENU_BUTTONS_Y, MAIN_MENU_LOGO_PATH, MAIN_MENU_CIRCLE_ENIX_PATH,
                       MAIN_MENU_FROM_HARDWARE_PATH, MAIN_MENU_JAZZ_STAR_PATH)

class MainMenuManager():
    """Class managing and displaying the main menu"""
    def __init__(self, screen):
        """Constructor method. It initializes the image of the menu and the buttons."""

        # First, we store the screen as an attribute
        self.screen = screen

        # Basic image
        self.image = pygame.Surface(WINDOW_SIZE)

        # Setting of the background color
        pygame.draw.rect(
            self.image,
            MENU_BACKGROUND_COLOR,
            pygame.Rect((0, 0), WINDOW_SIZE)
        )

        # Initialization of the buttons
        self.buttons = []
        button_x, button_y = (WINDOW_SIZE[1] - MENU_BUTTONS_WIDTH) / 2, MAIN_MENU_BUTTONS_Y

        for button_info in MAIN_MENU_BUTTONS:
            self.buttons.append((Button(
                button_x,
                button_y,
                MENU_BUTTONS_WIDTH,
                MENU_BUTTONS_HEIGHT,
                button_info[0]
            ), button_info[1]))

            button_y += MENU_BUTTONS_HEIGHT + MENU_BUTTONS_Y_MARGIN

        # Initialization of the different images displayed in the main menu
        self.logo_image = pygame.image.load(MAIN_MENU_LOGO_PATH).convert_alpha()
        self.from_hardware_image = pygame.image.load(MAIN_MENU_FROM_HARDWARE_PATH).convert_alpha()
        self.circle_enix_image = pygame.image.load(MAIN_MENU_CIRCLE_ENIX_PATH).convert_alpha()
        self.jazz_star_image = pygame.image.load(MAIN_MENU_JAZZ_STAR_PATH).convert_alpha()

        # Computation of the different coordinates of these images
        self.logo_coords = (
            (WINDOW_SIZE[0] - self.logo_image.get_width()) / 2,
            (MAIN_MENU_BUTTONS_Y - self.logo_image.get_height()) / 2
        )

        # Height of the space under the list of buttons
        bottom_space = (
            WINDOW_SIZE[1] - (
                MAIN_MENU_BUTTONS_Y + len(self.buttons) * (
                    MENU_BUTTONS_HEIGHT + MENU_BUTTONS_Y_MARGIN
                ) - MENU_BUTTONS_Y_MARGIN)
        )

        self.from_hardware_coords = (
            WINDOW_SIZE[0] / 4 - self.from_hardware_image.get_width() / 2,
            WINDOW_SIZE[1] - (bottom_space / 2 + self.from_hardware_image.get_height() / 2)
        )

        self.circle_enix_coords = (
            WINDOW_SIZE[0] / 2 - self.circle_enix_image.get_width() / 2,
            WINDOW_SIZE[1] - (bottom_space / 2 + self.circle_enix_image.get_height() / 2)
        )

        self.jazz_star_coords = (
            3 * WINDOW_SIZE[0] / 4 - self.jazz_star_image.get_width() / 2,
            WINDOW_SIZE[1] - (bottom_space / 2 + self.jazz_star_image.get_height() / 2)
        )

    def mainloop(self):
        """Main event loop of the main menu."""

        while True:
            # Events processing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # If the mouse moves, we have to update the buttons
                if event.type == pygame.MOUSEMOTION:
                    mouse_position = pygame.mouse.get_pos()

                    for button in self.buttons:
                        button[0].on_mouse_move(mouse_position[0], mouse_position[1])

                # If the mouse is clicked, we have to check for all the buttons
                # If one is clicked, we will change the view accordingly
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()

                    for button in self.buttons:
                        if button[0].collides(mouse_position[0], mouse_position[1]):
                            return button[1]

            # We draw all the elements of the menu
            self.screen.blit(self.image, (0, 0))

            # Then we draw the different images of the menu
            self.screen.blit(self.logo_image, self.logo_coords)
            self.screen.blit(self.from_hardware_image, self.from_hardware_coords)
            self.screen.blit(self.circle_enix_image, self.circle_enix_coords)
            self.screen.blit(self.jazz_star_image, self.jazz_star_coords)

            for button in self.buttons:
                button[0].draw(self.screen)

            # Updating the screen
            pygame.display.flip()
