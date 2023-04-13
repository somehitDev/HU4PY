# -*- coding: utf-8 -*-
from typing import List
from ._base import Widget, Layout



class Frame(Layout):
    """
    Frame Layout class
    """
    def __init__(self, parent:Layout = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Frame Layout(non-flex) class

        Parameters
        ----------
        parent: Layout, default None
            parent of Frame
        id: str, default None
            id of Frame
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes ot Frame
        """
        super().__init__(parent, "div", [ "hufpy-widget-no-flex", "hufpy-frame" ], class_list, id, attributes)

class FieldSet(Layout):
    """
    FieldSet Layout class
    """
    def __init__(self, parent:Layout = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        FieldSet Layout (same as GroupBox)

        Parameters
        ----------
        parent: Layout, default None
            parent of FieldSet
        id: str, default None
            id of FieldSet
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of FieldSet
        """
        super().__init__(parent, "fieldset", [ "hufpy-widget-no-flex", "hufpy-fieldset" ], class_list, id, attributes)

        self.__legend = Widget(self, "legend", [ "hufpy-widget-no-flex", "hufpy-fieldset-legend" ], auto_attach = True)

    @property
    def title(self) -> str:
        """
        title of FieldSet
        """
        return self.__legend.get_attribute("text")
    
    @title.setter
    def title(self, new_title:str):
        self.__legend.set_attribute("text", new_title)

class ColumnLayout(Layout):
    """
    Column(Vertical) Layout class
    """
    def __init__(self, parent:Layout = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Column Layout (same as VerticalBox)

        Parameters
        ----------
        parent: Layout, default None
            parent of ColumnLayout
        id: str, default None
            id of ColumnLayout
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of ColumnLayout
        """
        attributes["data-spacing"] = "0"
        super().__init__(parent, "div", [ "hufpy-widget", "huf-column-layout" ], class_list, id, attributes)

        self.__global_css_id = f"style_{self.id}"

    @property
    def spacing(self) -> int:
        """
        spacing between children of ColumnLayout
        """
        return self.get_attribute("data-spacing")
    
    @spacing.setter
    def spacing(self, new_spacing:int):
        self.set_attribute("data-spacing", new_spacing)
        self.api.add_global_css(self.__global_css_id, f"""
#""" + self.id + """ > *:not([style*="display: none"]):not(:last-child) {
    margin-bottom: """ + str(new_spacing) + """px
}
""")

class RowLayout(Layout):
    """
    Row(Horizontal) Layout class
    """
    def __init__(self, parent:Layout = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Row Layout (same as HorizontalBox)

        Parameters
        ----------
        parent: Layout, default None
            parent of RowLayout
        id: str, default None
            id of RowLayout
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of RowLayout
        """
        attributes["data-spacing"] = "0"
        super().__init__(parent, "div", [ "hufpy-widget", "huf-row-layout" ], class_list, id, attributes)

        self.__global_css_id = f"style_{self.id}"

    @property
    def spacing(self) -> int:
        """
        spacing between children of RowLayout
        """
        return self.get_attribute("data-spacing")
    
    @spacing.setter
    def spacing(self, new_spacing:int):
        self.set_attribute("data-spacing", new_spacing)
        self.api.add_global_css(self.__global_css_id, f"""
#""" + self.id + """ > *:not(:last-child) {
    margin-right: """ + str(new_spacing) + """px
}
""")

class StackLayout(Layout):
    """
    Stack Layout class
    """
    def __init__(self, parent:Layout = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Stack Layout (same as headless Tab)

        Parameters
        ----------
        parent: Layout, default None
            parend of StackLayout
        id: str, default None
            id of StackLayout
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of StackLayout
        """
        super().__init__(parent, "div", [ "hufpy-widget-no-flex", "hufpy-stack-layout" ], class_list, id, attributes)

    @property
    def current_index(self):
        """
        current index(index of visible child)
        """
        visible_index = None
        for idx, child in enumerate(self.children):
            if child.visible:
                visible_index = idx
                break

        return 0 if visible_index is None else visible_index

    @current_index.setter
    def current_index(self, new_index:int):
        for child in self.children:
            child.visible = False

        self.children[new_index].visible = True

    def append_child(self, widget:Layout, apply_html:bool = True):
        widget.update_style_property("width", "100%")
        widget.update_style_property("height", "100%")

        super().append_child(widget, apply_html)

class Spacer(Widget):
    """
    Spacer (Expander)
    """
    def __init__(self, parent:Layout):
        """
        Spacer Widget (same as Expander)

        Parameters
        ----------
        parent: Layout, required
            parent of Spacer
        """
        super().__init__(parent, "div", [ "hufpy-widget-no-flex" ])
        self.stretch = True
