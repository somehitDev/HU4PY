# -*- coding: utf-8 -*-
import os
from typing import List, Literal
from ._base import Widget, Layout


class Label(Widget):
    """
    Label Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Label Widget (uneditable text)

        Parameters
        ----------
        parent: Layout, required
            parent of Label
        id: str, default None
            id of Label
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of Label
        """
        attributes["text"] = ""
        super().__init__(parent, "label", [ "hufpy-widget" ], class_list, id, attributes)

    @property
    def text(self) -> str:
        """
        text of Label
        """
        return self.get_attribute("text")
    
    @text.setter
    def text(self, new_text:str):
        self.set_attribute("text", str(new_text))

class Image(Widget):
    """
    Image Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Widget to show Image

        Parameters
        ----------
        parent: Layout, required
            parent of Image
        id: str, default None
            id of Image
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of Image
        """
        super().__init__(parent, "div", [ "hufpy-widget-no-flex" ], class_list, id, attributes)

        self.repeat = False
        self.display_type = "fit"

    @property
    def source(self) -> str:
        """
        source of Image
        """
        return self.style.pop("background-image", "url('')")[5:-2]
    
    @source.setter
    def source(self, new_source:str):
        self.update_style_property("background-image", f"url('{os.path.realpath(new_source)}')")

    @property
    def repeat(self) -> bool:
        """
        flag to repeat image or not
        """
        return self.style.pop("background-repeat", "no-repeat") != "no-repeat"
    
    @repeat.setter
    def repeat(self, new_state:bool):
        self.update_style_property("background-repeat", "repeat" if new_state else "no-repeat")

    @property
    def display_type(self) -> Literal["contain", "cover", "fit"]:
        """
        display type of showing Image

        Options
        -------
        contain
            resize image for fully visible
        cover
            resize image to cover Image Widget, crop images over Widget
        fit
            stretch image to size of Image Widget
        """
        raw_type = self.style.pop("background-size", "100% 100%")
        return "fit" if raw_type == "100% 100%" else raw_type
    
    @display_type.setter
    def display_type(self, new_type:Literal["contain", "cover", "fit"]):
        self.update_style_property("background-size", "100% 100%" if new_type.lower() == "fit" else new_type.lower())
