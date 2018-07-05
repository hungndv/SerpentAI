from pprint import pprint
from threading import Thread
from time import sleep

from serpent.game_agent import GameAgent
from serpent.input_controller import KeyboardKey
from serpent.input_controller import MouseButton
from serpent.sprite_locator import SpriteLocator


class Serpentd2GameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

    def setup_play(self):
        self.clicked_button_single_player = False
        self.clicked_char_sorceress = False
        self.clicked_difficulty = False
        self.entered_world = False
        self.found_a_rune = False
        #pass

    def handle_play(self, game_frame):
        #print("string")
        #pprint(object)

        for i, game_frame in enumerate(self.game_frame_buffer.frames):
            self.visual_debugger.store_image_data(
                game_frame.frame,
                game_frame.frame.shape,
                str(i)
            )

        if self.entered_world is False:
            if self.clicked_button_single_player is False:
                print("clicked_button_single_player")
                location = self.find_sprite(self.game.sprites["SPRITE_BUTTON_SINGLE_PLAYER"], game_frame)
                if location is not None:
                    self.move_mouse_to_center_and_click(location)
                    self.clicked_button_single_player = True
                    return

            if self.clicked_char_sorceress is False:
                print("clicked_char_sorceress")
                location = self.find_sprite(self.game.sprites["SPRITE_TEXT_SORCERESS"], game_frame)
                if location is not None:
                    self.move_mouse_to_center_and_click(location, doubleClick=True)
                    self.clicked_char_sorceress = True
                    return

            #If need to select difficulty
            if self.clicked_difficulty is False:
                print("clicked_difficulty")
                location = self.find_sprite(self.game.sprites["SPRITE_BUTTON_NORMAL"], game_frame)
                if location is not None:
                    self.move_mouse_to_center_and_click(location)
                    self.clicked_difficulty = True
                    return

            print("entered_world")
            location = self.find_sprite(self.game.sprites["SPRITE_STATUE_MANA"], game_frame)
            if location is not None:
                self.entered_world = True
                return
        else: # entered_world

            #location = self.find_sprite(self.game.sprites["SPRITE_TEXT_RUNE"], game_frame)
            #if location is not None:
            #    print("Rune hold found!")
            if self.found_a_rune is False:
                self.input_controller.tap_key(KeyboardKey.KEY_X, 5)
                location = self.find_sprite(self.game.sprites["SPRITE_TEXT_RUNE"], game_frame)
                if location is not None:
                    self.move_mouse_to_center_and_click(location)
                else:
                    self.input_controller.release_key(KeyboardKey.KEY_X)

        #pass

    def find_sprite(self, sprite_to_locate, game_frame):
        sprite_locator = SpriteLocator()
        location = sprite_locator.locate(sprite=sprite_to_locate, game_frame=game_frame)
        return location # None if not found

    def get_center_point(self, location):
        return (int((location[3] - location[1])/2.0 + location[1]), int( (location[2] - location[0])/2.0 + location[0]))

    def move_mouse_to_center_and_click(self, location, button=MouseButton.LEFT, doubleClick=False):
        center_point = self.get_center_point(location)
        self.input_controller.move(center_point[0], center_point[1])
        self.input_controller.click(button)
        if doubleClick:
            self.input_controller.click(button)

    def threaded_function(arg):
        self.input_controller.tap_key(KeyboardKey.KEY_X, 5)