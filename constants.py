"""
This module contains all the constants useful in the application.
"""
import pygame

############################ Background ############################

 # Path to the textures of the background
BACKGROUND_TEXTURES_PATH = 'sprites/background_textures.png'
TILE_SIZE = 32 # Size in pixels of each tile

# The different tile codes used in the level files :
EMPTY = 0 # Tile code for an empty tile
WALL = 1 # Tile code for a wall
CRATE = 2 # Tile code for a crate
TROPHY = 3 # Tile code for a trophy
RED_CRATE = 4 # Tile code for a red crate
CHARACTER = 5 # Tile code for the characters
PLAYER_TELEPORTER = 6 # Tile code for the player teleporter

############################ Character #############################

# Dictionary describing the information (height, width, path to the texture) of each character
CHARACTERS_INFO = [
    {
        'height': 28,
        'width': 18,
        'textures_path': 'sprites/characters/mario_textures.png'
    },
    {
        'height': 30,
        'width': 16,
        'textures_path': 'sprites/characters/luigi_textures.png'
    },
    {
        'height': 32,
        'width': 16,
        'textures_path': 'sprites/characters/peach_textures.png'
    },
    {
        'height': 27,
        'width': 16,
        'textures_path': 'sprites/characters/toad_textures.png'
    }
]

# Dictionary describing the different movements that a character can do
CHARACTER_DIRECTIONS = {
    pygame.K_DOWN: {
        'texture_pos': 0,
        'dx': 0,
        'dy': 1
    },
    pygame.K_UP: {
        'texture_pos': 1,
        'dx': 0,
        'dy': -1
    },
    pygame.K_RIGHT: {
        'texture_pos': 2,
        'dx': 1,
        'dy': 0
    },
    pygame.K_LEFT: {
        'texture_pos': 3,
        'dx': -1,
        'dy': 0
    }
}

############################## Game ################################

# Size of the buttons displayed in the game
GAME_BUTTONS_HEIGHT = 50
GAME_BUTTONS_WIDTH = 150

# Space between the buttons and the bottom of the window
GAME_BUTTONS_Y_MARGIN = 16

############################## Views ###############################

GAME_VIEW = 0 # View set when the game is running
MAIN_MENU_VIEW = 1 # View set when the main menu is displayed
LEVEL_EDITOR_VIEW = 2 # View set when the level editor is running
CHARACTER_CHOICE_VIEW = 3 # View set when the character choice menu is displayed
MANUAL_VIEW = 4 # View set when the manual is displayed

############################## Menus ###############################

MENU_BACKGROUND_COLOR = (133, 0, 24) # Background color

# Margin applied around the different buttons
MENU_BUTTONS_Y_MARGIN = 25

# Size of the buttons
MENU_BUTTONS_WIDTH = 425
MENU_BUTTONS_HEIGHT = 50

########################### Main Menu ##############################

# Initial y value of the different buttons
MAIN_MENU_BUTTONS_Y = 225

# Buttons of the main menu and their corresponding view
MAIN_MENU_BUTTONS = [
    ('Jouer à Mario Sokoban', GAME_VIEW),
    ('Éditeur de niveaux', GAME_VIEW),
    ('Choix des personnages', GAME_VIEW),
    ("Mode d'emploi", GAME_VIEW)
]

# Paths to the different images displayed in the main menu
MAIN_MENU_LOGO_PATH = 'sprites/main_menu/mario_sokoban_logo.png'
MAIN_MENU_CIRCLE_ENIX_PATH = 'sprites/main_menu/circle_enix.png'
MAIN_MENU_FROM_HARDWARE_PATH = 'sprites/main_menu/from_hardware.png'
MAIN_MENU_JAZZ_STAR_PATH = 'sprites/main_menu/jazz_star.png'

######################### User Interface ###########################

UI_FONT_PATH = 'fonts/ui_font.ttf' # Path of the font file
UI_TEXT_COLOR = (255, 255, 255) # Color of the rendered text
UI_TEXT_PROPORTION = 0.5 # Proportion of the height of the components used by the text

UI_HOVER_ALPHA_VALUE = 75 # Amount of transparency of the hover surface
UI_HOVER_COLOR = (255, 255, 255) # Color of the layer added when the UI components are hovered
UI_BACKGROUND_COLOR = (55, 0, 10) # Color of the background

############################## Window ##############################

WINDOW_TITLE = 'Mario Sokoban' # Title of the window
WINDOW_TILE_SIZE = 20 # Size of the window, in terms of tile
WINDOW_ICON_PATH = 'sprites/window_icon.png' # Path to the image of the icon of the window
WINDOW_SIZE = (WINDOW_TILE_SIZE * TILE_SIZE, WINDOW_TILE_SIZE * TILE_SIZE) # Size of the window
