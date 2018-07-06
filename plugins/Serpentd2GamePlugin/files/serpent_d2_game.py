from serpent.game import Game

from .api.api import d2API

from serpent.utilities import Singleton




class Serpentd2Game(Game, metaclass=Singleton):

    def __init__(self, **kwargs):
        kwargs["platform"] = "executable"

        kwargs["window_name"] = "Diablo II"



        #kwargs["executable_path"] = "D:/Softwares/Diablo 2/Diablo 2/PlugY.exe -w"



        super().__init__(**kwargs)

        self.api_class = d2API
        self.api_instance = None

    @property
    def screen_regions(self):
        regions = {
            "BUTTON_SINGLE_PLAYER": (301, 336, 315, 465)
        }

        return regions

    @property
    def ocr_presets(self):
        presets = {
            "SAMPLE_PRESET": {
                "extract": {
                    "gradient_size": 1,
                    "closing_size": 1
                },
                "perform": {
                    "scale": 10,
                    "order": 1,
                    "horizontal_closing": 1,
                    "vertical_closing": 1
                }
            }
        }

        return presets
