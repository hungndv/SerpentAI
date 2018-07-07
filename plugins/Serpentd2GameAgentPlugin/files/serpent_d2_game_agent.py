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
from .helpers.utils import print_t


class Serpentd2GameAgent(GameAgent):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.frame_handlers["PLAY"] = self.handle_play

        self.frame_handler_setups["PLAY"] = self.setup_play

    def setup_play(self):
        self.entered_world = False
        self.is_picking = False
        self.last_item_loc = None
        self.k = PyKeyboard()
        self.pressed_item_key = False
        self.last_life_res = None
        self.last_mana_res = None
        self.game_frame = None
        self.is_mana_thread_running = False
        self.is_life_thread_running = False
        #pass

    def handle_play(self, game_frame):
        self.game_frame = game_frame
        #for i, game_frame in enumerate(self.game_frame_buffer.frames):
        #    self.visual_debugger.store_image_data(
        #        game_frame.frame,
        #        game_frame.frame.shape,
        #        str(i)
        #    )

        location = self.find_sprite("SPRITE_BUTTON_SINGLE_PLAYER")
        if location is not None:
            self.move_mouse_to_center_and_click(location)
            print_t("Click Single Player")
            return

        location = self.find_sprite("SPRITE_TEXT_SORCERESS")
        if location is not None :
            if not self.is_char_open(): # char panel has the class name
                self.move_mouse_to_center_and_click(location, doubleClick=True)
                print_t("Click Sorceress Player")
                returnx

        #If need to select difficulty
        location = self.find_sprite("SPRITE_BUTTON_NIGHTMARE")
        if location is not None:
            self.move_mouse_to_center_and_click(location)
            print_t("Select Difficulty")
            return

        location = self.find_sprite("SPRITE_STATUE_MANA")
        if location is None:
            return
        else:
            if  not self.is_mini_map_shown() \
                and not self.is_char_open() \
                and not self.is_inventory_open() \
                and not self.is_stash_open(): # if mini map is not show, press tab to show it
                self.k.tap_key(self.k.tab_key)
                print_t("Show mini map")
                sleep(0.2)
                return

            Thread(target=self.check_to_restore_life, args=(), daemon=True).start()
            Thread(target=self.check_to_restore_mana, args=(), daemon=True).start()

            if self.is_mini_map_shown() and not self.is_in_town() and not self.is_inventory_open(): # not find rune in town
                print_t("IS NOT IN TOWN")
                self.find_rune()
        #pass

    def find_sprite(self, sprite_name):
        sprite_locator = SpriteLocator()
        location = sprite_locator.locate(sprite=self.game.sprites[sprite_name], game_frame=self.game_frame)
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

    def hold_key_down(self):
        print_t("Hold X key...")
        self.input_controller.tap_key(KeyboardKey.KEY_X, 60*60*24)

    def check_to_restore_life(self):
        location = self.find_sprite("SPRITE_LIFE_LEVEL")
        if location is None:
            if self.last_life_res is None or (datetime.now() - self.last_life_res).seconds > 10:
                self.release_item_key()
                location = self.find_sprite("SPRITE_BELT_COL_1")
                if location is None:
                    self.input_controller.tap_key(KeyboardKey.KEY_1)
                    print_t("Press key 1 to restore life")
                    self.last_life_res = datetime.now()
                    return
                location = self.find_sprite("SPRITE_BELT_COL_2")
                if location is None:
                    self.input_controller.tap_key(KeyboardKey.KEY_2)
                    print_t("Press key 2 to restore life")
                    self.last_life_res = datetime.now()
                    return
                print_t("Out of health potions")

    def check_to_restore_mana(self):
        location = self.find_sprite("SPRITE_MANA_LEVEL")
        if location is None:
            if self.last_mana_res is None or (datetime.now() - self.last_mana_res).seconds > 10:
                self.release_item_key()
                location = self.find_sprite("SPRITE_BELT_COL_3")
                if location is None:
                    self.input_controller.tap_key(KeyboardKey.KEY_3)
                    print_t("Press key 3 to restore mana")
                    self.last_mana_res = datetime.now()
                    return
                location = self.find_sprite("SPRITE_BELT_COL_4")
                if location is None:
                    self.input_controller.tap_key(KeyboardKey.KEY_4)
                    print_t("Press key 4 to restore mana")
                    self.last_mana_res = datetime.now()
                    return
                print_t("Out of mana potions")

    def release_item_key(self):
        if self.pressed_item_key is True:
            self.k.release_key('x')
            self.pressed_item_key = False

    def find_rune(self):
        if self.pressed_item_key is False:
            self.k.press_key('x')
            self.pressed_item_key = True
            return

        if self.is_picking is False:
            #location = self.find_sprite("SPRITE_RUNE_DROP") # is not working if it's behind the wall :(
            location = self.find_sprite("SPRITE_TEXT_RUNE")
            locInv = self.find_sprite("SPRITE_INVENTORY_OPEN")
            locSta = self.find_sprite("SPRITE_STASH_OPEN")
            if location is not None:
                if (locInv is not None and location[3] > locInv[1]) or locSta is not None: #rune text is inside inventory or stash is open
                    return
                print_t("Picking a rune")
                self.is_picking = True
                self.move_mouse_to_center_and_click(location, duration=0)
                self.last_item_loc = location
            else:
                self.release_item_key()
        else:
            location = self.find_sprite("SPRITE_TEXT_RUNE")
            if location is not None:
                print_t("Picking a rune...")
                if location[0] == self.last_item_loc[0] and location[1] == self.last_item_loc[1]: # char is not moving
                    print_t("Picking another rune...")
                    self.move_mouse_to_center_and_click(location, duration=1)
                self.last_item_loc = location
            else:
                print_t("Picked a rune")
                self.last_item_loc = None
                self.is_picking = False
                x, y = win32api.GetCursorPos()
                self.input_controller.move(x + 45, y + 35, 0) # move cursor to another place, to avoid the cursor overlapping on item name
                self.release_item_key()

    def is_in_town(self):
        return True if  self.is_in_rouge_encampment() \
                        or self.is_in_lut_gholein() \
                        or self.is_in_kurast_docks() else False

    def is_in_rouge_encampment(self):
        return True if self.find_sprite("SPRITE_TEXT_ROGUE_ENCAMPMENT") is not None else False

    def is_in_lut_gholein(self):
        return True if self.find_sprite("SPRITE_TEXT_LUT_GHOLEIN") is not None else False

    def is_in_kurast_docks(self):
        return True if self.find_sprite("SPRITE_TEXT_KURAST_DOCKS") is not None else False

    def is_mini_map_shown(self):
        return True if  self.find_sprite("SPRITE_MNMAP_NPC") is not None \
                        or self.find_sprite("SPRITE_TEXT_EXPANSION_UPPER_RIGHT") is not None \
                        or self.find_sprite("SPRITE_MNMAP_CHAR") is not None \
                    else False

    def is_char_open(self):
        return True if self.find_sprite("SPRITE_CHAR_OPEN") is not None else False

    def is_inventory_open(self):
        return True if self.find_sprite("SPRITE_INVENTORY_OPEN") is not None else False

    def is_stash_open(self):
        return True if self.find_sprite("SPRITE_STASH_OPEN") is not None else False
