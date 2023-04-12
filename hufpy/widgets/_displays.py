# -*- coding: utf-8 -*-
import os
from typing import Literal
from ._base import Widget, Layout


class Label(Widget):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        attributes["text"] = ""
        super().__init__(parent, "label", [ "hufpy-widget" ], id, attributes)

    @property
    def text(self) -> str:
        return self.get_attribute("text")
    
    @text.setter
    def text(self, new_text:str):
        self.set_attribute("text", str(new_text))

class Image(Widget):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, "div", [ "hufpy-widget-no-flex" ], id, attributes)

        self.repeat = False
        self.display_type = "fit"

    @property
    def source(self) -> str:
        return self.style.pop("background-image", "url('')")[5:-2]
    
    @source.setter
    def source(self, new_source:str):
        self.update_style_property("background-image", f"url('{os.path.realpath(new_source)}')")

    @property
    def repeat(self) -> bool:
        return self.style.pop("background-repeat", "no-repeat") != "no-repeat"
    
    @repeat.setter
    def repeat(self, new_state:bool):
        self.update_style_property("background-repeat", "repeat" if new_state else "no-repeat")

    @property
    def display_type(self) -> Literal["contain", "cover", "fit"]:
        raw_type = self.style.pop("background-size", "100% 100%")
        return "fit" if raw_type == "100% 100%" else raw_type
    
    @display_type.setter
    def display_type(self, new_type:Literal["contain", "cover", "fit"]):
        self.update_style_property("background-size", "100% 100%" if new_type.lower() == "fit" else new_type.lower())
