# -*- coding: utf-8 -*-
from typing import List
from types import MethodType
from ._base import Widget, Layout


class Button(Widget):
    """
    Button Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Button Widget

        Parameters
        ----------
        parent: Layout, required
            parent of Button
        id: str, default None
            id of Button
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of Button
        """
        super().__init__(parent, "button", [ "hufpy-widget-no-flex", "hufpy-button" ], class_list, id, attributes)

        self.__on_click, self.__on_doubleclick = None, None
        self.set_additional_style("active", {}, False)

    @property
    def text(self) -> str:
        """
        text of Button
        """
        return self.get_attribute("text")
    
    @text.setter
    def text(self, new_text:str):
        self.set_attribute("text", str(new_text))

    @property
    def active_foreground(self) -> str:
        return self.get_additional_style("active", "foreground")
    
    @active_foreground.setter
    def active_foreground(self, new_foreground:str):
        self.set_additional_style("active", { "foreground": new_foreground })

    @property
    def active_background(self) -> str:
        return self.get_additional_style("active", "background")
    
    @active_background.setter
    def active_background(self, new_background:str):
        self.set_additional_style("active", { "background": new_background })

    @property
    def on_clicked(self) -> MethodType:
        """
        clicked event of Button

        event: MethodType
        """
        return self.__on_click
    
    @on_clicked.setter
    def on_clicked(self, new_callback:MethodType):
        self.__on_click = new_callback
        self.bind_command("click", "on_clicked")

    @property
    def on_double_clicked(self) -> MethodType:
        """
        double clicked event of Button

        event: MethodType
        """
        return self.__on_doubleclick
    
    @on_double_clicked.setter
    def on_double_clicked(self, new_callback:MethodType):
        self.__on_doubleclick = new_callback
        self.bind_command("dblclick", "on_double_clicked")

class ToggleButton(Button):
    """
    ToggleButton Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        ToggleButton Widget

        Parameters
        ----------
        parent: Layout, requried
            parent of ToggleButton
        id: str, default None
            id of ToggleButton
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of ToggleButton
        """
        super().__init__(parent, id, class_list, attributes)

        self.set_attribute("data-toggled", "false")
        self.bind_command("click", "on_toggled", [ "data-toggled" ])
        self.__on_toggle = None

    @property
    def toggled(self) -> bool:
        """
        toggled state of ToggleButton
        """
        return self.get_attribute("data-toggled")
    
    @toggled.setter
    def toggled(self, state:bool):
        self.set_attribute("data-toggled", state)

    @property
    def on_toggled(self) -> MethodType:
        """
        toggled event of ToggleButton

        event: MethodType[bool]
        """
        return self.__on_toggled
    
    @on_toggled.setter
    def on_toggled(self, new_callback:MethodType):
        self.__on_toggle = new_callback

    def __on_toggled(self, state:bool):
        self.toggled = not self.toggled

        if self.__on_toggle:
            self.__on_toggle(not state)
