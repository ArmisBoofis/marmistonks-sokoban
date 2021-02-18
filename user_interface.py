"""
This module contains the different user interface components of the game,
such the Button and the Input class.
"""

import pygame
from constants import (UI_FONT_PATH, UI_TEXT_COLOR, UI_BACKGROUND_COLOR,
                       UI_TEXT_PROPORTION, UI_HOVER_COLOR, UI_HOVER_ALPHA_VALUE,
                       UI_BUTTON_CHECK_PATH, UI_BUTTON_CHECK_SIZE)


class ImageSprite(pygame.sprite.Sprite):
    """Class creating a pygame sprite from an image and its coordinates"""

    def __init__(self, image_path, coords):
        """Constructor method. It initializes the image and then the sprite."""

        # Call to the parent constructor
        pygame.sprite.Sprite.__init__(self)

        # We load the image
        self.image = pygame.image.load(image_path).convert_alpha()

        # We define a rect for the sprite
        self.rect = pygame.Rect(coords, self.image.get_size())


class Button(pygame.sprite.Sprite):
    """Class defining a button"""

    def __init__(self, rect):
        """Constructor method. <rect> describes the coordinates and
        dimensions of the button."""

        # Call to the parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Attribute saving if the button is checked
        self.checked = False

        # Button check icon
        self.check_icon = pygame.image.load(
            UI_BUTTON_CHECK_PATH).convert_alpha()

        # Rect (coordinates and dimensions) of the button
        self.rect = rect

        # Basic image of the button (without the hover effect)
        self.image_base = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image_base.fill(UI_BACKGROUND_COLOR)

        # Hover surface of the button (hover effect)
        self.hover_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.hover_surface.fill(UI_HOVER_COLOR)
        self.hover_surface.set_alpha(UI_HOVER_ALPHA_VALUE)

        # Final image of the button, clear for now
        # We add some pixels in case we want to add the button-check icon
        self.image = pygame.Surface(
            (self.rect.width + UI_BUTTON_CHECK_SIZE[0] // 2,
             self.rect.height + UI_BUTTON_CHECK_SIZE[1] // 2),
            pygame.SRCALPHA
        )

    def collides(self, mouse_coords):
        """Method which determines if the coordinates of the click
        passed in parameters are contained in the button."""

        return self.rect.collidepoint(mouse_coords[0], mouse_coords[1])

    def update(self, mouse_coords):
        """Method called when the mouse is moved,
        to update the appearance of the button."""

        # We display the basic image of the button
        self.image.blit(self.image_base, (0, 0))

        # If the button is hovered, then we also display the hover layer
        if self.collides(mouse_coords):
            self.image.blit(self.hover_surface, (0, 0))

        # If the button is checked, then we display the button-check icon
        if self.checked:
            self.image.blit(
                self.check_icon,
                (self.rect.width - UI_BUTTON_CHECK_SIZE[0] // 2,
                 self.rect.height - UI_BUTTON_CHECK_SIZE[1] // 2)
            )


class TextButton(Button):
    """Class defining a button with text in it."""

    def __init__(self, rect, text):
        """Constructor method. <text> is a string
        representing the text displayed in the button.."""

        # Call to the parent constructor
        Button.__init__(self, rect)

        # Font used to display the text (we make the text slighlty smaller than the button)
        text_font = pygame.font.Font(UI_FONT_PATH, int(
            self.rect.height * UI_TEXT_PROPORTION))

        # Size of the rendered text
        (text_width, text_height) = text_font.size(text)

        # Image of the text, represented by a Surface object
        text_image = text_font.render(
            text,
            True,
            UI_TEXT_COLOR
        )

        # Finally, we blit the text on the image of the button
        self.image_base.blit(
            text_image,
            ((self.rect.width - text_width) / 2,
             (self.rect.height - text_height) / 2)
        )

        # We update the button, so that the image is filled
        self.update((0, 0))


class ImageButton(Button):
    """Class defining a button with an image in it."""

    def __init__(self, rect, image_path):
        """Constructor method, loading the image and displaying it."""

        # Call to the parent constructor
        Button.__init__(self, rect)

        # First, we load the image
        image = pygame.image.load(image_path).convert_alpha()
        (image_width, image_height) = image.get_size()

        # Then, we blit it on the button image, centering it
        self.image_base.blit(
            image,
            ((self.rect.width - image_width) / 2,
             (self.rect.height - image_height) / 2)
        )

        # We update the button, so that the image is filled
        self.update((0, 0))
