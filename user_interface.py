"""
This module contains the different user interface components of the game,
such the Button and the Input class.
"""

import pygame
from constants import (UI_FONT_PATH, UI_TEXT_COLOR, UI_BACKGROUND_COLOR,
                       UI_TEXT_PROPORTION, UI_HOVER_COLOR, UI_HOVER_ALPHA_VALUE)

class Button(pygame.sprite.Sprite):
    """Class defining a button"""

    def __init__(self, x, y, width, height, text):
        """Constructor method. <x> and <y> are the coordinates
        of the button, and <text> the text displayed in it."""

        # Call to the parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Rect (coordinates and dimensions) of the button
        self.rect = pygame.Rect(x, y, width, height)

        # Font used to display the text (we make the text slighlty smaller than the button)
        text_font = pygame.font.Font(UI_FONT_PATH, int(self.rect.height * UI_TEXT_PROPORTION))

        # Size of the rendered text
        (text_width, text_height) = text_font.size(text)

        # Image of the text, represented by a Surface object
        text_image = text_font.render(
            text,
            True,
            UI_TEXT_COLOR
        )

        # Basic image of the button (without the hover effect)
        self.image_base = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # We first draw the background rectangle on it
        pygame.draw.rect(
            self.image_base,
            UI_BACKGROUND_COLOR,
            pygame.Rect(0, 0, self.width, self.height)
        )

        # Finally, we blit the text on the image of the button
        self.image_base.blit(
            text_image,
            ((self.width - text_width) / 2, (self.height - text_height) / 2)
        )

        # Hover surface of the button (hover effect)
        self.hover_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.hover_surface.fill(UI_HOVER_COLOR)
        self.hover_surface.set_alpha(UI_HOVER_ALPHA_VALUE)

        # Final image of the button, clear for now
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def collides(self, mouse_coords):
        """Method which determines if the coordinates of the click
        passed in parameters are contained in the button."""

        in_x_range = self.x_value <= mouse_coords[0] <= (self.x_value + self.width)
        in_y_range = self.y_value <= mouse_coords[1] <= (self.y_value + self.height)

        return in_x_range and in_y_range

    def update(self, mouse_coords):
        """Method called when the mouse is moved,
        to update the appearance of the button."""

        # We display the basic image of the button
        self.image.blit(self.image_base, (0, 0))

        # If the button is hovered, then we also display the hover layer
        if self.collides(mouse_coords):
            self.image.blit(self.hover_surface, (0, 0))