# -*- coding: utf-8 -*-
import os, sys, webview, json, threading
from typing import Union, Dict, Any, List
from ._base import Widget, Layout
from .layouts import ColumnLayout, RowLayout, Frame
from ._displays import Label
from ._buttons import Button
from .. import _shared



class _TitleBar(RowLayout):
    def __init__(self, parent:Union["Window", "Dialog"], id:str, class_list:List[str], attributes:dict = {}):
        super().__init__(parent, id, class_list, attributes)

        if sys.platform == "darwin":
            self.__close_btn = Button(self, f"{self.id}_closebutton", [ "hufpy-window-titlebar-closebutton" ])
            self.append_child(self.__close_btn)
            self.__label = Label(self, f"{self.id}_label", [ "hufpy-window-titlebar-label" ])
            self.append_child(self.__label)
        else:
            self.__label = Label(self, f"{self.id}_label", [ "hufpy-window-titlebar-label" ])
            self.append_child(self.__label)
            self.__close_btn = Button(self, f"{self.id}_closebutton", [ "hufpy-window-titlebar-closebutton" ])
            self.append_child(self.__close_btn)

        self.__label.horizontal_align = "center"
        self.__label.vertical_align = "center"
        self.__label.stretch = True

        self.__close_btn.text = "x"
        self.__close_btn.bind_command("click", "close", [], parent.id)

    @property
    def title(self) -> str:
        return self.__label.text
    
    @title.setter
    def title(self, new_title:str):
        self.__label.text = new_title

class Window(ColumnLayout):
    def __init__(self, parent:"Window" = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        super().__init__(parent if parent else _shared.application_body, id, class_list + [ "hufpy-window" ], attributes)
        self.visible = False

        self.__titlebar = _TitleBar(self, f"{self.id}_titlebar", [ "hufpy-window-titlebar" ])
        self.append_child(self.__titlebar)
        self.__content = Frame(self, f"{self.id}_content", [ "hufpy-window-content" ])
        self.append_child(self.__content)

        modal_background = Widget(self.__content, "div", [ "hufpy-modal-background" ], auto_attach = True)
        modal_background.set_attribute("data-visible", "false")
        modal_background.update_style_property("height", "calc(100% - 19px)")
        modal_background.update_style_property("top", "19px")

        self.width = 600
        self.height = 400

    @property
    def parent(self) -> "Window":
        return super().parent

    @property
    def title(self) -> str:
        return self.__titlebar.title
    
    @title.setter
    def title(self, new_title:str):
        self.__titlebar.title = new_title

    @property
    def content(self) -> Layout:
        return self.__content.children[1] if len(self.__content.children > 1) else None

    @content.setter
    def content(self, new_content:Layout):
        if self.content:
            self.__content.remove_child(self.content)

        new_content.class_list.append(".hufpy-window-content")
        new_content.update_style_property("width", "100%")
        new_content.update_style_property("height", "100%")

        new_content.parent.remove_child(new_content)
        self.__content.append_child(new_content)
        new_content.parent = self.__content

    @property
    def width(self) -> int:
        """
        width of widget
        """
        return int(self.style.pop("width")[:-2])
    
    @width.setter
    def width(self, new_width:int):
        self.update_style_property("left", f"calc(50% - {new_width / 2}px)")
        self.update_style_property("width", f"{new_width}px")

    @property
    def height(self) -> int:
        """
        height of widget
        """
        return int(self.style.pop("height")[:-2])
    
    @height.setter
    def height(self, new_height:int):
        self.update_style_property("top", f"calc(50% - {new_height / 2}px)")
        self.update_style_property("height", f"{new_height}px")

    @property
    def x(self) -> int:
        return int(self.style.pop("left", "0px")[:-2])
    
    @x.setter
    def x(self, new_x:int):
        self.update_style_property("left", f"{new_x}px")

    @property
    def y(self) -> int:
        return int(self.style.pop("top", "0px")[:-2])
    
    @y.setter
    def y(self, new_y:int):
        self.update_style_property("top", f"{new_y}px")


    def show_modal_background(self):
        self.api.app_window.evaluate_js(f'document.querySelector("#{self.id} .hufpy-modal-background").setAttribute("data-visible", "true");')

    def close_modal_background(self):
        self.api.app_window.evaluate_js(f'document.querySelector("#{self.id} .hufpy-modal-background").setAttribute("data-visible", "false");')


    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def close(self):
        self.delete()


class Dialog(Window):
    def __init__(self, parent:Window = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        self.__real_parent = parent if parent else _shared.application_body

        super().__init__(_shared.application_body, id, class_list, attributes)

        self.class_list.remove("hufpy-window")
        self.class_list.append("hufpy-dialog")

    def show(self):
        self.__real_parent.show_modal_background()
        super().show()

    def hide(self):
        self.__real_parent.show_modal_background()
        super().hide()

    def close(self):
        self.__real_parent.show_modal_background()
        super().close()
