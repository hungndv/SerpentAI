import win32api

from datetime import datetime
from pykeyboard import PyKeyboard
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
        self.is_picking = False
        self.last_item_loc = None
        self.hold_key_down_thread = Thread(target=self.hold_key_down, args=())
        self.hold_key_down_thread.daemon = True
        self.k = PyKeyboard()
        #pass

    def handle_play(self, game_frame):
        #pprint(object)

        #for i, game_frame in enumerate(self.game_frame_buffer.frames):
        #    self.visual_debugger.store_image_data(
        #        game_frame.frame,
        #        game_frame.frame.shape,
        #        str(i)
        #    )

        if self.entered_world is False:
            if self.clicked_button_single_player is False:
                location = self.find_sprite(self.game.sprites["SPRITE_BUTTON_SINGLE_PLAYER"], game_frame)
                if location is not None:
                    self.move_mouse_to_center_and_click(location)
                    self.clicked_button_single_player = True
                    return

            if self.clicked_char_sorceress is False:
                location = self.find_sprite(self.game.sprites["SPRITE_TEXT_SORCERESS"], game_frame)
                if location is not None:
                    self.move_mouse_to_center_and_click(location, doubleClick=True)
                    self.clicked_char_sorceress = True
                    return

            #If need to select difficulty
            if self.clicked_difficulty is False:
                location = self.find_sprite(self.game.sprites["SPRITE_BUTTON_NORMAL"], game_frame)
                if location is not None:
                    self.move_mouse_to_center_and_click(location)
                    self.clicked_difficulty = True
                    return

            location = self.find_sprite(self.game.sprites["SPRITE_STATUE_MANA"], game_frame)
            if location is not None:
                self.entered_world = True
                self.print_t("entered_world");
                return
        else: # entered_world
            if self.is_picking is False:
                #location = self.find_sprite(self.game.sprites["SPRITE_RUNE_DROP"], game_frame) # is not working if it's behind the wall :(
                self.k.press_key(self.k.alt_key)

                location = self.find_sprite(self.game.sprites["SPRITE_TEXT_RUNE"], game_frame)
                locInv = self.find_sprite(self.game.sprites["SPRITE_INVENTORY_OPEN"], game_frame)
                locSta = self.find_sprite(self.game.sprites["SPRITE_STASH_OPEN"], game_frame)
                if location is not None:
                    if (locInv is not None and location[3] > locInv[1]) or locSta is not None: #rune text is inside inventory or stash is open
                        return
                    self.print_t("Picking a rune")
                    self.is_picking = True
                    self.move_mouse_to_center_and_click(location, duration=0)
                    self.last_item_loc = location
            else:
                location = self.find_sprite(self.game.sprites["SPRITE_TEXT_RUNE"], game_frame)
                if location is not None:
                    self.print_t("Picking a rune...")
                    if location[0] == self.last_item_loc[0] and location[1] == self.last_item_loc[1]: # char is not moving
                        self.print_t("Picking another rune...")
                        self.move_mouse_to_center_and_click(location, duration=1)
                    self.last_item_loc = location
                else:
                    self.print_t("Picked a rune")
                    self.last_item_loc = None
                    self.is_picking = False
                    x, y = win32api.GetCursorPos()
                    self.input_controller.move(x + 45, y + 35, 0) # move cursor to another place, to avoid the cursor overlapping on item name
                    self.k.release_key(self.k.alt_key)
        #pass

    def find_sprite(self, sprite_to_locate, game_frame):
        sprite_locator = SpriteLocator()
        location = sprite_locator.locate(sprite=sprite_to_locate, game_frame=game_frame)
        return location # None if not found

    def get_center_point(self, location):
        return (int((location[3] - location[1])/2.0 + location[1]), int( (location[2] - location[0])/2.0 + location[0]))

    def move_mouse_to_center_and_click(self, location, button=MouseButton.LEFT, doubleClick=False, duration=0.25):
        center_point = self.get_center_point(location)
        self.input_controller.move(center_point[0], center_point[1], 0)
        sleep(0.5);
        self.input_controller.click(button, duration=duration)
        if doubleClick:
            self.input_controller.click(button, duration=duration)

    def print_t(self, content):
        print(f"{datetime.now()} - {content}")

    def hold_key_down(self):
        self.print_t("Hold X key...")
        self.input_controller.tap_key(KeyboardKey.KEY_X, 60*60*24)