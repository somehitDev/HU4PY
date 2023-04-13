# -*- coding: utf-8 -*-
import uuid, hufpy, webview
from typing import List, Any, Literal, Union


def create_widget_id(widget_py_class_name:str) -> str:
    """
    function to generate widget id

    Return
    ------
    id of widget: str
    """
    return f"{widget_py_class_name.capitalize()}_{uuid.uuid4().hex[:10]}"


class WidgetClassManager:
    """
    class manager of widget
    """
    def __init__(self, class_list:List[str], widget_id:str, api:"hufpy.application.ApplicationAPI"):
        """
        Parameters
        ----------
        class_list: List[str], required
            list of class
        widget_id: str, required
            id of widget
        api: ApplicationAPI
            application api of hufpy system
        """
        self.__class_list = class_list
        self.__widget_id = widget_id
        self.__api = api

    def append(self, class_name:str):
        """
        append class to widget

        Parameters
        ----------
        class_name: str, required
            class name to append
        """
        if not class_name in self.__class_list:
            self.__class_list.append(class_name)
            # self.__api.app_window.evaluate_js(f'document.querySelector("#{self.__widget_id}").classList.add("{self.__class_list}");')
            self.__api.app_window.evaluate_js(f'window.hufpy.$widgets["{self.__widget_id}"].classList.add("{self.__class_list}");')

    def remove(self, class_name:str):
        """
        remove class from widget

        Parameters
        ----------
        class_name: str, required
            class name to remove
        """
        if class_name in self.__class_list:
            self.__class_list.remove(class_name)
            # self.__api.app_window.evaluate_js(f'document.querySelector("#{self.__widget_id}").classList.remove("{self.__class_list}");')
            self.__api.app_window.evaluate_js(f'window.hufpy.$widgets["{self.__widget_id}"].classList.remove("{self.__class_list}");')

class Widget:
    """
    Base Widget class of hufpy system
    """
    api:"hufpy.application.ApplicationAPI" = None
    widget_type:str = "widget"

    def __init__(self, parent:"Layout", tag_name:str, widget_class_list:List[str] = [], additional_class_list:List[str] = [], widget_id:str = None, widget_attributes:dict = {}, auto_attach:bool = False):
        """
        Create Widget and connect to webview api system

        Parameters
        ----------
        parent: Layout, required
            parent of widget
        tag_name: str, required
            html tag to create
        widget_class_list: List[str], default []
            class list of html object
        additional_class_list: List[str], default []
            additional class list of html object
        widget_id: str, default None
            id of widget
            if None, generate id from create_widget_id function
        widget_attributes: dict, default {}
            attributes of widget
        auto_attach: bool, default False
            flag to append widget to parent's children
        """
        self.__parent = parent
        self.api = parent.api if parent else self.__class__.api if self.__class__.api else None
        self.__id = widget_id if widget_id else create_widget_id(self.__class__.__name__)
        self.__class_list = list(set(widget_class_list + additional_class_list))

        if parent:
            parent.children.append(self)

        if self.api:
            self.api.create_widget(tag_name, widget_class_list, self, widget_attributes, parent, auto_attach)
            if parent and auto_attach:
                parent.append_child(self, True)

    def __str__(self) -> str:
        return f'<{self.__class__.__name__} id="{self.id}">'

    @property
    def id(self) -> str:
        """
        id of widget
        """
        return self.__id
    
    @id.setter
    def id(self, new_id:str):
        self.__id = new_id
        self.set_attribute("id", new_id)

    @property
    def class_list(self) -> WidgetClassManager:
        """
        class manager of widget
        """
        return WidgetClassManager(self.__class_list, self.id, self.api)
    
    @property
    def parent(self) -> "Layout":
        """
        parent of widget
        """
        return self.__parent
    
    @parent.setter
    def parent(self, new_parent:"Layout"):
        if self.parent:
            self.parent.remove_child(self)

        new_parent.append_child(self)
        self.__parent = new_parent


    @property
    def style(self) -> dict:
        """
        style of widget
        """
        return self.api.get_widget_attribute(self.id, "style")
    
    @style.setter
    def style(self, new_style:dict):
        self.api.set_widget_attribute(self.id, "style", new_style)

    @property
    def width(self) -> int:
        """
        width of widget
        """
        return int(self.style.pop("width", self.get_attribute("width"))[:-2])

    @width.setter
    def width(self, new_width:int):
        self.update_style_property("width", f"{new_width}px")

    @property
    def height(self) -> int:
        """
        height of widget
        """
        return int(self.style.pop("height", self.get_attribute("height"))[:-2])
    
    @height.setter
    def height(self, new_height:int):
        self.update_style_property("height", f"{new_height}px")

    @property
    def foreground(self) -> str:
        """
        foreground(font color) of widget
        """
        return self.style.pop("color", "black")
    
    @foreground.setter
    def foreground(self, new_foreground:str):
        self.update_style_property("color", new_foreground)

    @property
    def background(self) -> str:
        """
        background color of widget
        """
        return self.style.pop("background-color", "white")
    
    @background.setter
    def background(self, new_background:str):
        self.update_style_property("background-color", new_background)


    @property
    def stretch(self) -> bool:
        """
        flag to stretch widget
        if True, widget expands
        """
        return self.has_style_property("flex")

    @stretch.setter
    def stretch(self, state:bool):
        if state:
            self.update_style_property("flex", "1")
        else:
            self.remove_style_property("flex")

    @property
    def horizontal_align(self) -> Literal["default", "left", "center", "right"]:
        """
        horizontal alignment of widget content

        Options
        -------
        default
            default state, same as left
        left
            set content align to left
        center
            set content align to center
        right
            set content align to right
        """
        if self.has_style_property("justify-content"):
            raw_align = self.style["justify-content"]
            if raw_align == "start":
                return "left"
            elif raw_align == "end":
                return "right"
            else:
                return raw_align
        else:
            return "default"

    @horizontal_align.setter
    def horizontal_align(self, align:Literal["default", "left", "center", "right"]):
        align = align.lower()

        if align == "left":
            self.update_style_property("justify-content", "start")
        elif align == "center":
            self.update_style_property("justify-content", "center")
        elif align == "right":
            self.update_style_property("justify-content", "end")
        else:
            self.remove_style_property("justify-content")

    @property
    def vertical_align(self) -> Literal["default", "top", "center", "bottom"]:
        """
        vertical alignment of widget content

        Options
        -------
        default
            default state, same as top
        top
            set content align to top
        center
            set content align to center
        bottom
            set content align to bottom
        """
        if self.has_style_property("align-items"):
            raw_align = self.style["align-items"]
            if raw_align == "start":
                return "top"
            elif raw_align == "end":
                return "bottom"
            else:
                return raw_align
        else:
            return "default"

    @vertical_align.setter
    def vertical_align(self, align:Literal["default", "top", "center", "bottom"]):
        align = align.lower()

        if align == "left":
            self.update_style_property("align-items", "start")
        elif align == "center":
            self.update_style_property("align-items", "center")
        elif align == "right":
            self.update_style_property("align-items", "end")
        else:
            self.remove_style_property("align-items")


    @property
    def disabled(self) -> bool:
        """
        disabled state of widget
        """
        return self.has_attribute("disabled")
    
    @disabled.setter
    def disabled(self, state:bool):
        if state:
            self.set_attribute("disabled", "")
        else:
            self.remove_attribute("disabled")

    @property
    def visible(self) -> bool:
        """
        flag to visible of widget
        """
        return self.get_attribute("data-visible")
    
    @visible.setter
    def visible(self, state:bool):
        self.set_attribute("data-visible", "true" if state else "false")
        try:
            widget_idx = self.parent.children.index(self)
        except ValueError:
            widget_idx = len(self.parent.children) + 1

        self.api.set_widget_visible(self.id, self.parent.id, state, widget_idx)


    def update_style_property(self, name:str, value:str):
        """
        update style property of widget

        Parameters
        ----------
        name: str, required
            name of property to update
        value: str, required
            value to update
        """
        new_style = self.style
        new_style.update({ name: value })
        self.style = new_style

    def remove_style_property(self, name:str):
        """
        remove style property of widget

        Parameters
        ----------
        name: str, required
            name of property to remove
        """
        new_style = self.style
        new_style.pop(name, None)
        self.style = new_style

    def has_style_property(self, name:str) -> bool:
        """
        check style property exists

        Parameters
        ----------
        name: str, required
            name of property to check

        Return
        ------
        state: bool
            state of property exists
        """
        return name in self.style.keys()
    
    def get_attribute(self, name:str) -> Any:
        """
        get attribute of widget

        Parameters
        ----------
        name: str, required
            attribute name to get

        Return
        ------
        value: Any
            value of given attribute name
        """
        return self.api.get_widget_attribute(self.id, name)

    def set_attribute(self, name:str, value:Any):
        """
        set attribute of widget

        Parameters
        ----------
        name: str, required
            attribute name to set
        value: Any, required
            attribute value to set
        """
        self.api.set_widget_attribute(self.id, name, value)

    def remove_attribute(self, name:str):
        """
        remove attribute from widget

        Parameters
        ----------
        name: str, required
            attribute name to remove
        """
        self.api.remove_widget_attribute(self.id, name)

    def has_attribute(self, name:str):
        """
        check attribute exists

        Parameters
        ----------
        name: str, required
            attribute name to exists
        """
        return self.api.widget_attribute_exists(self.id, name)
    
    def delete(self):
        """
        delete widget from hufpy system
        """
        self.api.remove_widget(self)
        self.parent.children.remove(self)

    def bind_command(self, event_name:str, bind_name:str, call_args:List[str] = [], call_widget_id:str = None):
        """
        bind command(event) to widget

        Parameters
        ----------
        event_name: str, required
            event name to bind
        bind_name: str, required
            function name of widget to bind
        call_args: List[str], default []
            arguments for widget's function
        call_widget_id: str, default None
            widget id for call function if need
            if caller and reciever widgets are different, need to set
        """
        self.api.bind_widget_event(self.id, event_name, bind_name, call_args, call_widget_id)

class Layout(Widget):
    """
    Layout Widget class
    """
    widget_type:str = "layout"

    def __init__(self, parent:Union["Layout", webview.Window], tag_name:str, widget_class_list:List[str] = [], additional_class_list:List[str] = [], widget_id:str = None, widget_attributes:dict = {}, auto_attach:bool = False):
        """
        Create Layout and connect to webview api system

        Parameters
        ----------
        parent: Layout or webview.Window, required
            parent of widget
        tag_name: str, required
            html tag to create
        widget_class_list: List[str], default []
            class list of html object
        additional_class_list: List[str], default []
            additional class list of html object
        widget_id: str, default None
            id of widget
            if None, generate id from create_widget_id function
        widget_attributes: dict, default {}
            attributes of widget
        auto_attach: bool, default False
            flag to append widget to parent's children
        """
        super().__init__(parent, tag_name, widget_class_list, additional_class_list, widget_id, widget_attributes, True if auto_attach or isinstance(parent, webview.Window) else False)

        self.__children:List[Widget] = []

    @property
    def children(self) -> List[Widget]:
        """
        child widgets of layout
        """
        return self.__children
    
    def append_child(self, widget:Union[Widget, "Layout"], apply_html:bool = True):
        """
        append widget to layout

        Parameters
        ----------
        widget: Widget or Layout, required
            widget to append
        apply_html: bool, default True
            flag to attach element to Layout
        """
        if widget.parent:
            widget.parent.remove_child(widget)

        self.children.append(widget)

        if apply_html:
            self.api.app_window.evaluate_js(f'window.hufpy.$attachWidget("{widget.id}", "{self.id}", "{self.widget_type}");')

    def insert_child(self, widget:Union[Widget, "Layout"], index:int):
        """
        insert widget in specific index

        Parameters
        ----------
        widget: Widget of Layout, required
            widget to insert
        index: int, required
            specific index to insert
        """
        widget.parent.remove_child(widget)
        self.api.app_window.evaluate_js(f'window.hufpy.$attachWidget("{widget.id}", "{self.id}", "{self.widget_type}" {index});')
        self.children.insert(index, widget)

    def remove_child(self, child:Union[Widget, "Layout"]):
        """
        remove child widget from Layout

        Parameters
        ----------
        child: Widget or Layout
            child to remove
        """
        self.api.app_window.evaluate_js(f'window.hufpy.$detatchWidget("{child.id}", "{self.id}");')
        if child in self.children:
            self.children.remove(child)
    
    def clear(self):
        """
        clear all children
        """
        for child in self.__children:
            self.remove_child(child)
