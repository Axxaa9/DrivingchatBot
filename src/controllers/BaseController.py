from src.helpers.config import get_settings, Settings
import os
import random as rn
import string


class BaseController:
    def __init__(self):
        self.app_sesttings = get_settings()

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.assets_dir = os.path.join(
            self.base_dir,
            "assets"
        )
        