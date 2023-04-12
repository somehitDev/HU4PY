# -*- coding: utf-8 -*-
import os, sys, webview, json
from ast import literal_eval
from typing import Dict, List, Any, Type
from .widgets._base import Layout, Widget
from . import __path__


class ApplicationAPI:
    app_window:webview.Window = None

    def __init__(self):
        self.widgets:Dict[str, Widget] = {}

    def __convert_object_to_js(self, object:Any) -> str:
        if isinstance(object, dict):
            return json.dumps(object)
        elif isinstance(object, bool):
            return "true" if object else "false"
        else:
            return "`" + str(object) + "`"
        
    def __revert_js_to_object(self, js_value:Any) -> Any:
        if isinstance(js_value, str):
            if js_value.startswith("{") and js_value.endswith("}"):
                return json.loads(js_value)
            elif js_value.startswith("[") and js_value.endswith("]"):
                return literal_eval(js_value)
            elif js_value in ( "true", "false" ):
                return js_value == "true"
            else:
                try:
                    return eval(js_value)
                except ( NameError, ValueError, SyntaxError ):
                    return js_value
        else:
            return js_value

    def create_widget(self, tag_name:str, widget_class_list:List[str], widget:Widget, attributes:dict, parent:Layout = None, auto_attach:bool = False):
        parent_id = "hufpy-app-container" if parent is None else parent.id

        res = self.app_window.evaluate_js(f"""
window.hufpy.createWidget("{tag_name}", "{" ".join(widget_class_list)}", "{widget.widget_type.lower()}", "{widget.id}", {self.__convert_object_to_js(attributes)}, "{parent_id}", {self.__convert_object_to_js(auto_attach)});
""")
        if res["state"] == "fail":
            raise RuntimeError(res["message"])

        self.widgets[widget.id] = widget
                                                                 
    def remove_widget(self, widget:Widget):
        self.app_window.evaluate_js(f'window.hufpy.removeWidget("{widget.id}");')
        self.widgets.pop(widget.id, None)


    # def get_widget_children(self, widget_id:str) -> List[str]:
    #     return self.app_window.evaluate_js(f'window.hufpy.getWidgetChildren("{widget_id}");')

    def get_widget_attribute(self, widget_id:str, attribute_name:str) -> Any:
        return self.__revert_js_to_object(self.app_window.evaluate_js(f'window.hufpy.getWidgetAttribute("{widget_id}", "{attribute_name}");'))
    
    def set_widget_attribute(self, widget_id:str, attribute_name:str, attribute_value:Any):
        self.app_window.evaluate_js(f'window.hufpy.setWidgetAttribute("{widget_id}", "{attribute_name}", {self.__convert_object_to_js(attribute_value)});')
    
    def remove_widget_attribute(self, widget_id:str, attribute_name:str):
        self.app_window.evaluate_js(f'window.hufpy.removeWidgetAttribute("{widget_id}", "{attribute_name}");')

    def widget_attribute_exists(self, widget_id:str, attribute_name:str) -> bool:
        return self.app_window.evaluate_js(f'window.hufpy.widgetAttributeExists("{widget_id}", "{attribute_name}");')

    def set_widget_visible(self, widget_id:str, parent_id:str, visible:bool, widget_idx:int = None):
        widget_idx = '"null"' if widget_idx is None else widget_idx
        self.app_window.evaluate_js(f'window.hufpy.setWidgetVisible("{widget_id}", "{parent_id}", {"true" if visible else "false"}, {widget_idx});')


    def bind_widget_event(self, widget_id:str, event_name:str, bind_name:str, call_args:List[str] = [], call_widget_id:str = None):
        call_widget_id = "null" if call_widget_id is None else f'"{call_widget_id}"'
        self.app_window.evaluate_js(f'window.hufpy.bindWidgetEvent("{widget_id}", "{event_name}", "{bind_name}", {call_args}, {call_widget_id});')

    def call_python_widget_event(self, widget_id:str, event_name:str, args:List[Any]):
        if widget_id in self.widgets.keys():
            getattr(self.widgets[widget_id], event_name)(*[ self.__revert_js_to_object(arg) for arg in args ])

    
    def add_global_css(self, style_id:str, style_content:str):
        self.app_window.evaluate_js(f'window.hufpy.addGlobalCss("{style_id}", `{style_content}`);')

    def delete_global_css(self, style_id:str):
        self.app_window.evaluate_js(f'window.hufpy.deleteGlobalCss("{style_id}");')

class Application:
    """
    hufpy Application manager
    """
    __app_api:ApplicationAPI = None

    @staticmethod
    def init(title:str = "hufpy", icon:str = None, width:int = 800, height:int = 600, x:int = None, y:int = None) -> webview.Window:
        """
        Initialize and create default webview window

        Parameters
        ----------
        title: str, default "hufpy"
            title of main window
        icon: str, default None
            icon of main window
            if windows, .ico
            if macos, .icns
            if linux or nuix, .png
        width: int, default 800
            width of main window
        height: int, default 600
            height of main window
        x: int, default None
            horizontal location(x) of main window
            if None, center
        y: int, default None
            vertical location(y) of main window
            if None, center

        Return
        ------
        window: webview.Window
            main window generated
        """
        webview.initialize("cef" if sys.platform == "win32" else "cocoa" if sys.platform == "darwin" else "qt")
        app_api = ApplicationAPI()
        setattr(Application, "__app_api", app_api)

        def on_window_loaded():
            win.load_css(os.path.join(__path__[0], "assets", "styles", f"{sys.platform}.css"))
            gui_win = win.gui.BrowserView.instances[win.uid]

            if sys.platform == "win32":
                import clr
                clr.AddReference("System.Drawing")
                from System.Drawing import Icon

                gui_win.Icon = Icon(icon if icon else os.path.join(__path__[0], "assets", "icons", "icon.ico"))
            elif sys.platform == "darwin":
                from AppKit import NSImage

                gui_win.app.setApplicationIconImage_(
                    NSImage.alloc().initByReferencingFile_(icon if icon else os.path.join(__path__[0], "assets", "icons", "icon.icns"))
                )
            else:
                from PySide6.QtCore import QIcon

                gui_win.setWindowIcon(QIcon(icon if icon else os.path.join(__path__[0], "assets", "icons", "icon.png")))

        win = webview.create_window(
            url = os.path.join(__path__[0], "assets", "index.html"),
            js_api = app_api,
            title = title,
            width = width, height = height,
            x = x, y = y
        )
        app_api.app_window = win
        win.events.loaded += on_window_loaded

        return win

    @staticmethod
    def run(main_layout_class:Type[Layout], debug:bool = False):
        """
        Run hufpy application

        Parameters
        ----------
        main_layout_class: Type[Layout], required
            class of main layout to display
        debug: bool, default False
            flag for debug(devtool)
        """
        def on_start():
            main_layout_class.api = getattr(Application, "__app_api")
            main_layout_class()

        webview.start(on_start, debug = debug)
