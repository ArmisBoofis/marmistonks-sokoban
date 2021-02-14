"""
This module contains the different user interface components of the game,
such the Button and the Input class.
"""

import pygame
from constants import (UI_FONT_PATH, UI_TEXT_COLOR, UI_BACKGROUND_COLOR,
                       UI_TEXT_PROPORTION, UI_HOVER_COLOR, UI_HOVER_ALPHA_VALUE)

class Button():
    """Class defining a button"""

    def __init__(self, x, y, width, height, text):
        """Constructor method. <x> and <y> are the coordinates
        of the button, and <text> the text displayed in it."""

        # Coordinates and size of the button
        self.x_value, self.y_value, self.width, self.height = x, y, width, height

        # Attribute storing the current state of the button (hovered or not)
        self.hovered = False

        # Font used to display the text (we make the text slighlty smaller than the button)
        text_font = pygame.font.Font(UI_FONT_PATH, int(self.height * UI_TEXT_PROPORTION))

        # Size of the rendered text
        (text_width, text_height) = text_font.size(text)

        # Image of the text, represented by a Surface object
        text_image = text_font.render(
            text,
            True,
            UI_TEXT_COLOR
        )

        # Final image of the Button
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # We first draw the background rectangle on it
        pygame.draw.rect(
            self.image,
            UI_BACKGROUND_COLOR,
            pygame.Rect(0, 0, self.width, self.height)
        )

        # Finally, we blit the text on the image of the button
        self.image.blit(
            text_image,
            ((self.width - text_width) / 2, (self.height - text_height) / 2)
        )

    def on_mouse_move(self, mouse_x, mouse_y):
        """Method called when the mouse is moved,
        to update the appearance of the button."""

        self.hovered = self.collides(mouse_x, mouse_y)

    def draw(self, screen):
        """Method used to draw the button on the screen, at the right coordinates"""

        # We blit on the screen the basic appearance of the button
        screen.blit(
            self.image,
            (self.x_value, self.y_value)
        )

        # If the button is hovered, then we have to add a thin white layer
        if self.hovered:
            # Configuration of the layer displayed iver the button
            hover_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            hover_surface.fill(UI_HOVER_COLOR)
            hover_surface.set_alpha(UI_HOVER_ALPHA_VALUE)

            # Then we blit this surface on the button
            screen.blit(
                hover_surface,
                (self.x_value, self.y_value)
            )

    def collides(self, mouse_x, mouse_y):
        """Method which determines if the coordinates of the click
        passed in parameters are contained in the button."""

        in_x_range = self.x_value <= mouse_x <= (self.x_value + self.width)
        in_y_range = self.y_value <= mouse_y <= (self.y_value + self.height)

        return in_x_range and in_y_range
