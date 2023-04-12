# -*- coding: utf-8 -*-
from types import MethodType
from ._base import Layout
from .layouts import ColumnLayout, RowLayout, StackLayout, Frame



class Tab(ColumnLayout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, id, attributes)
        self.class_list.append("hufpy-tab")
        self.spacing = 0

        self.__header = RowLayout(self, self.id + "_header")
        self.__header.spacing = 5
        self.append_child(self.__header)

        self.__content = StackLayout(self, self.id + "_content")
        self.__content.stretch = True
        self.append_child(self.__content)

    @property
    def header(self) -> RowLayout:
        return self.__header
    
    @property
    def content(self) -> StackLayout:
        return self.__content

    @property
    def current_index(self) -> int:
        return self.__content.current_index
    
    @current_index.setter
    def current_index(self, new_index:int):
        self.__content.current_index = new_index

class TabItem(Layout):
    def __init__(self, parent:Tab):
        super().__init__(parent.header, "label", [ "hufpy-widget", "hufpy-tab-header" ], auto_attach = True)

        self.__tab_root = parent
        self.horizontal_align = "center"
        self.vertical_align = "center"

        self.bind_command("click", "on_clicked")
        self.content = Frame(parent.content)

    @property
    def title(self) -> str:
        return self.get_attribute("text")
    
    @title.setter
    def title(self, new_text:str):
        self.set_attribute("text", new_text)

    @property
    def content(self) -> Layout:
        return self.__tab_root.content.children[self.parent.children.index(self)]

    @content.setter
    def content(self, new_content:Layout):
        if not new_content.parent == self.__tab_root.content:
            try:
                old_content = self.__tab_root.content.children[self.parent.children.index(self)]
                old_content.delete()
            except IndexError:
                pass

            new_content.parent.remove_child(new_content)
            self.__tab_root.content.insert_child(new_content, self.parent.children.index(self))
            new_content.parent = self.__tab_root.content
            new_content.class_list.append("hufpy-tab-content")

        new_content.update_style_property("width", "100%")
        new_content.update_style_property("height", "100%")

        self.__tab_root.current_index = 0

    @property
    def on_clicked(self) -> MethodType:
        return self.__on_clicked

    def __on_clicked(self):
        self.__tab_root.current_index = self.parent.children.index(self)
