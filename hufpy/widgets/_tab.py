# -*- coding: utf-8 -*-
from typing import List
from types import MethodType
from ._base import Layout
from .layouts import ColumnLayout, RowLayout, StackLayout, Frame



class Tab(ColumnLayout):
    """
    Tab Layout class
    """
    def __init__(self, parent:Layout = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Tab Layout System

        Parameters
        ----------
        parent: Layout, default None
            parent of Tab
        id: str, default None
            id of Tab
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of Tab
        """
        super().__init__(parent, id, class_list, attributes)
        self.class_list.append("hufpy-tab")
        self.spacing = 0

        self.__header = RowLayout(self, self.id + "_header", [ "hufpy-tab-header" ])
        self.__header.spacing = 5
        self.append_child(self.__header)

        self.__content = StackLayout(self, self.id + "_content", [ "hufpy-tab-content" ])
        self.__content.stretch = True
        self.append_child(self.__content)

    @property
    def header(self) -> RowLayout:
        """
        header (Tab Buttons) of Tab
        """
        return self.__header
    
    @property
    def content(self) -> StackLayout:
        """
        content (Tab Items) of Tab
        """
        return self.__content

    @property
    def current_index(self) -> int:
        """
        current index(index of visible Widget)
        """
        return self.__content.current_index
    
    @current_index.setter
    def current_index(self, new_index:int):
        self.__content.current_index = new_index

class TabItem(Layout):
    """
    TabItem Widget class
    """
    def __init__(self, parent:Tab):
        super().__init__(parent.header, "label", [ "hufpy-widget", "hufpy-tab-header" ], auto_attach = True)

        self.__tab_root = parent
        self.horizontal_align = "center"
        self.vertical_align = "center"

        self.bind_command("click", "on_clicked")
        self.content = Frame(parent.content)

    @property
    def title(self) -> str:
        """
        title of TabItem
        """
        return self.get_attribute("text")
    
    @title.setter
    def title(self, new_text:str):
        self.set_attribute("text", new_text)

    @property
    def content(self) -> Layout:
        """
        content of TabItem
        """
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
        """
        clicked event of TabItem(cannot set)
        """
        return self.__on_clicked

    def __on_clicked(self):
        self.__tab_root.current_index = self.parent.children.index(self)
