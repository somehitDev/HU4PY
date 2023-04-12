# -*- coding: utf-8 -*-
from ._base import Widget, Layout



class Frame(Layout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, "div", [ "hufpy-widget-no-flex", "hufpy-frame" ], id, attributes)

class FieldSet(Layout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, "fieldset", [ "hufpy-widget-no-flex", "hufpy-fieldset" ], id, attributes)

        self.__legend = Widget(self, "legend", [ "hufpy-widget-no-flex", "hufpy-fieldset-legend" ], auto_attach = True)

    @property
    def title(self) -> str:
        return self.__legend.get_attribute("text")
    
    @title.setter
    def title(self, new_title:str):
        self.__legend.set_attribute("text", new_title)

class ColumnLayout(Layout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        attributes["data-spacing"] = "0"
        super().__init__(parent, "div", [ "hufpy-widget", "huf-column-layout" ], id, attributes)

        self.__global_css_id = f"style_{self.id}"

#         self.api.app_window.load_css(f"""
# #""" + self.id + """ > *:not(:last-child) {
#     margin-bottom: """ + str(spacing) + """px
# }
# """)

    @property
    def spacing(self) -> int:
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
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        attributes["data-spacing"] = "0"
        super().__init__(parent, "div", [ "hufpy-widget", "huf-row-layout" ], id, attributes)

        self.__global_css_id = f"style_{self.id}"

#         self.api.app_window.load_css(f"""
# #""" + self.id + """ > *:not(:last-child) {
#     margin-right: """ + str(spacing) + """px
# }
# """)

    @property
    def spacing(self) -> int:
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
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, "div", [ "hufpy-widget-no-flex", "hufpy-stack-layout" ], id, attributes)

    @property
    def current_index(self):
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

class Spacer(Widget):
    def __init__(self, parent:Layout = None):
        super().__init__(parent, "div", [ "hufpy-widget-no-flex" ])
        self.stretch = True
