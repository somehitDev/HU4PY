# -*- coding: utf-8 -*-
import sys
from types import MethodType
from typing import Any, Literal, List
from datetime import datetime
from ._base import Widget, Layout
from .layouts import RowLayout, Frame
from ._displays import Label


class _Input(Widget):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}, auto_attach:bool = False):
        super().__init__(parent, "input", [ "hufpy-widget-no-flex" ], id, attributes, auto_attach)
        self.__on_change = None

    @property
    def on_changed(self) -> MethodType:
        return self.__on_change
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

# inputs
class TextInput(_Input):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        attributes["type"] = "text"
        super().__init__(parent, id, attributes)

        self.bind_command("change", "on_changed", [ "value" ])
        self.__on_change = None

    @property
    def autocomplete(self) -> bool:
        return self.get_attribute("autocomplete")
    
    @autocomplete.setter
    def autocomplete(self, new_state:bool):
        self.set_attribute("autocomplete", new_state)

    @property
    def type(self) -> Literal["text", "password", "email", "tel", "url", "search"]:
        return self.get_attribute("type")
        
    @type.setter
    def type(self, new_type:Literal["text", "password", "email", "tel", "url", "search"]):
        self.get_attribute("type", new_type.lower())

    @property
    def placeholder(self) -> str:
        return self.get_attribute("placeholder")
    
    @placeholder.setter
    def placeholder(self, new_placeholder:str):
        self.set_attribute("placeholder", new_placeholder)

    @property
    def value(self) -> Any:
        return self.get_attribute("value")
    
    @value.setter
    def value(self, new_value:Any):
        self.set_attribute("value", str(new_value))

    @property
    def on_changed(self) -> MethodType:
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

    def __on_changed(self, text:str):
        if self.__on_change:
            self.__on_change(text)

class NumberInput(_Input):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        attributes["type"] = "number"
        super().__init__(parent, id, attributes)

        self.bind_command("change", "on_changed", [ "value" ])
        self.__on_change = None

        self.min = 0
        self.max = 100
        self.step = 1

    @property
    def min(self) -> int:
        return self.get_attribute("min")
    
    @min.setter
    def min(self, new_min:int):
        self.set_attribute("min", new_min)

    @property
    def max(self) -> int:
        return self.get_attribute("max")
    
    @max.setter
    def max(self, new_max:int):
        self.set_attribute("max", new_max)

    @property
    def step(self) -> int:
        return self.get_attribute("step")
    
    @step.setter
    def step(self, new_step:int):
        self.set_attribute("step", new_step)

    @property
    def value(self) -> int:
        return self.get_attribute("value")
    
    @value.setter
    def value(self, new_value:int):
        self.set_attribute("value", new_value)

    @property
    def on_changed(self) -> MethodType:
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

    def __on_changed(self, value:int):
        if self.__on_change:
            self.__on_change(value)

class FileInput(_Input):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        attributes["type"] = "file"
        super().__init__(parent, id, attributes)

        self.bind_command("change", "on_selected")
        self.__on_select = None

    @property
    def accept(self) -> List[str]:
        return [
            item.strip()
            for item in self.get_attribute("accept").split(",")
        ]
    
    @accept.setter
    def accept(self, new_accept:List[str]):
        self.set_attribute("accept", ",".join(new_accept))

    @property
    def capture(self) -> Literal["user", "environment"]:
        return self.get_attribute("capture")
    
    @capture.setter
    def capture(self, new_value:Literal["user", "environment"]):
        self.set_attribute("capture", new_value)

    @property
    def multiple(self) -> bool:
        return self.get_attribute("multiple")
    
    @multiple.setter
    def multiple(self, new_state:bool):
        self.set_attribute("multiple", new_state)

    @property
    def value(self) -> str:
        return self.get_attribute("value")
    
    @property
    def files(self) -> List[str]:
        return self.get_attribute("files")
    
    @property
    def on_selected(self) -> MethodType:
        return self.__on_selected
    
    @on_selected.setter
    def on_selected(self, new_callback:MethodType):
        self.__on_select = new_callback
    
    def __on_selected(self):
        if self.__on_select:
            if self.multiple:
                self.__on_select(self.files)
            else:
                self.__on_select(self.value)

if sys.platform == "win32":
    class DirectoryInput(FileInput):
        def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
            attributes["webkitdirectory"] = True
            super().__init__(parent, id, attributes)

# checkbox
class CheckBox(RowLayout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, id, attributes)

        self.__chk = _Input(self, attributes = { "type": "checkbox" }, auto_attach = True)
        self.__label = Label(self, attributes = { "for": self.__chk.id })
        self.append_child(self.__label)

        self.__chk.bind_command("change", "on_changed", [ "checked" ])
        self.__chk.on_changed = self.__on_changed

    @property
    def text(self) -> str:
        return self.__label.text
    
    @text.setter
    def text(self, new_text:str):
        self.__label.text = new_text

    @property
    def checked(self) -> bool:
        return self.__chk.get_attribute("checked")
    
    @checked.setter
    def checked(self, state:bool):
        self.__chk.set_attribute("checked", state)

    @property
    def on_changed(self) -> MethodType:
        return self.__chk.on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__chk.on_changed = new_callback

    def __on_changed(self, state:bool):
        if self.__chk.on_changed:
            self.__chk.on_changed(state)

# radio
class Radio(RowLayout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, id, attributes)

        self.__radio = _Input(self, attributes = { "type": "radio", "name": f"{self.parent.id}_radio" }, auto_attach = True)
        self.__label = Label(self, attributes = { "for": self.__radio.id })
        self.append_child(self.__label)

        self.__radio.bind_command("change", "on_changed", [ "value" ])

    @property
    def checked(self) -> bool:
        return self.__radio.get_attribute("checked")
    
    @property
    def value(self) -> Any:
        return self.__radio.get_attribute("value")
    
    @value.setter
    def value(self, new_value:Any):
        self.__radio.set_attribute("value", str(new_value))
        self.__label.text = str(new_value)

    @property
    def on_changed(self) -> MethodType:
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__radio.on_changed = new_callback

    def __on_changed(self, value:Any):
        if self.__radio.on_changed:
            self.__radio.on_changed(value)

# pickers
class DatePicker(_Input):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, id, attributes)

        self.type = "date"
        self.bind_command("change", "on_changed", [ "value" ])
        self.__on_change = None

    @property
    def type(self) -> Literal["datetime", "date", "month", "time"]:
        raw_type = self.get_attribute("type")
        if raw_type == "datetime-local":
            return "datetime"
        else:
            return raw_type
        
    @type.setter
    def type(self, new_type:Literal["datetime", "date", "month", "time"]):
        self.set_attribute("type", "datetime-local" if new_type == "datetime" else new_type)
        if self.get_attribute("value") == "":
            self.value = datetime.now()

    @property
    def value(self) -> datetime:
        if self.type == "datetime":
            return datetime.strptime(self.get_attribute("value"), "%Y-%m-%dT%H:%M:%S")
        elif self.type == "date":
            return datetime.strptime(self.get_attribute("value"), "%Y-%m-%d")
        elif self.type == "month":
            return datetime.strptime(self.get_attribute("value"), "%Y-%m")
        else:
            return datetime.strptime(self.get_attribute("value"), "%H:%M:%S")
        
    @value.setter
    def value(self, new_value:datetime):
        if self.type == "datetime":
            self.set_attribute("value", new_value.strftime("%Y-%m-%dT%H:%M:%S"))
        elif self.type == "date":
            self.set_attribute("value", new_value.strftime("%Y-%m-%d"))
        elif self.type == "month":
            self.set_attribute("value", new_value.strftime("%Y-%m"))
        else:
            self.set_attribute("value", new_value.strftime("%H:%M:%S"))

    @property
    def on_changed(self) -> MethodType:
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback
    
    def __on_changed(self, value:datetime):
        if self.__on_change:
            self.__on_change(value)

class ColorPicker(RowLayout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, id, attributes)

        self.__picker = _Input(self, attributes = { "type": "color" }, auto_attach = True)
        self.__label = Label(self, attributes = { "for": self.__picker.id })
        self.append_child(self.__label)

        self.__picker.bind_command("change", "on_changed", [ "value" ])

    @property
    def text(self) -> str:
        return self.__label.text
    
    @text.setter
    def text(self, new_text:str):
        self.__label.text = new_text

    @property
    def value(self) -> str:
        return self.__picker.get_attribute("value")
    
    @value.setter
    def value(self, new_color:str):
        self.__picker.set_attribute("value", new_color)

    @property
    def on_changed(self) -> MethodType:
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__picker.on_changed = new_callback

    def __on_changed(self, color:str):
        if self.__picker.on_changed:
            self.__picker.on_changed(color)

# range
class Range(Frame):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, id, attributes)

        self.__range = _Input(self, attributes = { "type": "range" }, auto_attach = True)
        self.__label = Label(self, attributes = { "for": self.__range.id })
        self.append_child(self.__label)

        self.__range.bind_command("change", "on_changed", [ "value" ])
        self.orient = "horizontal"
        self.min = 0
        self.max = 100
        self.step = 1

    @property
    def text(self) -> str:
        return self.__label.text
    
    @text.setter
    def text(self, new_text:str):
        self.__label.text = new_text

    @property
    def orient(self) -> Literal["horizontal", "vertical"]:
        return self.__range.get_attribute("orient")
    
    @orient.setter
    def orient(self, new_orient:Literal["horizontal", "vertical"]):
        if not sys.platform == "linux" and new_orient == "vertical":
            new_orient = "horizontal"
            print("vertical range is available on linux system")

        self.__range.set_attribute("orient", new_orient.lower())
        if new_orient == "horizontal":
            self.class_list.remove("hufpy-column-layout")
            self.class_list.append("hufpy-row-layout")
        else:
            self.class_list.remove("hufpy-row-layout")
            self.class_list.append("hufpy-column-layout")

    @property
    def min(self) -> int:
        return self.__range.get_attribute("min")
    
    @min.setter
    def min(self, new_min:int):
        self.__range.set_attribute("min", new_min)

    @property
    def max(self) -> int:
        return self.__range.get_attribute("max")
    
    @max.setter
    def max(self, new_max:int):
        self.__range.set_attribute("max", new_max)

    @property
    def step(self) -> int:
        return self.__range.get_attribute("step")
    
    @step.setter
    def step(self, new_step:int):
        self.__range.set_attribute("step", new_step)

    @property
    def value(self) -> int:
        return self.__range.get_attribute("value")
    
    @value.setter
    def value(self, new_value:int):
        self.__range.set_attribute("value", new_value)

    @property
    def on_changed(self) -> MethodType:
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__range.on_changed = new_callback

    def __on_changed(self, color:str):
        if self.__range.on_changed:
            self.__range.on_changed(color)

# combobox
class ComboBox(Layout):
    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, "select", [ "hufpy-widget-no-flex" ], id, attributes)

        self.__children:List[ComboBoxItem] = []
        self.bind_command("change", "on_index_changed")
        self.bind_command("change", "on_text_changed")
        self.__on_index_change, self.__on_text_change = None, None

    @staticmethod
    def from_list(parent:Layout, items:List[str]) -> "ComboBox":
        cb = ComboBox(parent)
        for item in items:
            child = ComboBoxItem(cb)
            child.value = item

        return cb

    @property
    def children(self) -> List["ComboBoxItem"]:
        return self.__children

    @property
    def current_index(self) -> int:
        for idx, child in enumerate(self.children):
            if child.value == self.get_attribute("value"):
                return idx

    @current_index.setter
    def current_index(self, new_index:int):
        for idx, child in enumerate(self.children):
            child.selected = idx == new_index

    @property
    def current_text(self) -> str:
        return self.get_attribute("value")

    @current_text.setter
    def current_text(self, new_text:str):
        for child in self.children:
            child.selected == child.value == new_text

    @property
    def on_index_changed(self) -> MethodType:
        return self.__on_index_changed

    @on_index_changed.setter
    def on_index_changed(self, new_callback:MethodType):
        self.__on_index_change = new_callback

    def __on_index_changed(self):
        if self.__on_index_change:
            self.__on_index_change(self.current_index)

    @property
    def on_text_changed(self) -> MethodType:
        return self.__on_text_changed
    
    @on_text_changed.setter
    def on_text_changed(self, new_callback:MethodType):
        self.__on_text_change = new_callback

    def __on_text_changed(self):
        if self.__on_text_change:
            self.__on_text_change(self.current_text)

class ComboBoxItem(Widget):
    def __init__(self, parent:ComboBox):
        super().__init__(parent, "option", auto_attach = True)

    @property
    def value(self) -> Any:
        return self.get_attribute("value")
    
    @value.setter
    def value(self, new_value:Any):
        self.set_attribute("value", new_value)
        self.set_attribute("text", new_value)

    @property
    def selected(self) -> bool:
        return self.get_attribute("selected")
    
    @selected.setter
    def selected(self, new_state:bool):
        self.set_attribute("selected", new_state)
