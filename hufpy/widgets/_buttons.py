# -*- coding: utf-8 -*-
from types import MethodType
from ._base import Widget, Layout


class Button(Widget):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, "button", [ "hufpy-widget", "hufpy-button" ], id, attributes)

        self.__on_click, self.__on_doubleclick = None, None

    @property
    def text(self) -> str:
        return self.get_attribute("text")
    
    @text.setter
    def text(self, new_text:str):
        self.set_attribute("text", str(new_text))

    @property
    def on_clicked(self) -> MethodType:
        return self.__on_click
    
    @on_clicked.setter
    def on_clicked(self, new_callback:MethodType):
        self.__on_click = new_callback
        self.bind_command("click", "on_clicked")

    @property
    def on_double_clicked(self) -> MethodType:
        return self.__on_doubleclick
    
    @on_double_clicked.setter
    def on_double_clicked(self, new_callback:MethodType):
        self.__on_doubleclick = new_callback
        self.bind_command("dblclick", "on_double_clicked")

class ToggleButton(Button):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, id, attributes)

        self.set_attribute("data-toggled", "false")
        self.bind_command("click", "on_toggled", [ "data-toggled" ])
        self.__on_toggle = None

    @property
    def toggled(self) -> bool:
        return self.get_attribute("data-toggled")
    
    @toggled.setter
    def toggled(self, state:bool):
        self.set_attribute("data-toggled", state)

    @property
    def on_toggled(self) -> MethodType:
        return self.__on_toggled
    
    @on_toggled.setter
    def on_toggled(self, new_callback:MethodType):
        self.__on_toggle = new_callback

    def __on_toggled(self, state:bool):
        self.toggled = not self.toggled

        if self.__on_toggle:
            self.__on_toggle(not state)
