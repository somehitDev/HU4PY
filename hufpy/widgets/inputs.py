# -*- coding: utf-8 -*-
import sys
from types import MethodType
from typing import Any, Literal, List
from datetime import datetime
from ._base import Widget, Layout
from .layouts import RowLayout, Frame
from ._displays import Label


class _Input(Widget):
    """
    Base Input Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}, auto_attach:bool = False):
        """
        Base Input class

        Parameters
        ----------
        parent: Layout, required
            parent of Input
        id: str, default None
            id of Input
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of Input
        auto_attach: bool, default False
            flag to append widget to parent's children
        """
        super().__init__(parent, "input", [ "hufpy-widget-no-flex" ], class_list, id, attributes, auto_attach)
        self.__on_change = None

    @property
    def on_changed(self) -> MethodType:
        """
        changed event of Input

        event: MethodType
        """
        return self.__on_change
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

# inputs
class TextInput(_Input):
    """
    TextInput Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        TextInput Widget (same as <input type="text">)

        Parameters
        ----------
        parent: Layout, required
            parent of TextInput
        id: str, default None
            id of TextInput
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of TextInput
        """
        attributes["type"] = "text"
        super().__init__(parent, id, [ "hufpy-textinput" ] + class_list, attributes)

        self.bind_command("change", "on_changed", [ "value" ])
        self.__on_change = None

    @property
    def autocomplete(self) -> bool:
        """
        flag to autocomplete or not
        """
        return self.get_attribute("autocomplete")
    
    @autocomplete.setter
    def autocomplete(self, new_state:bool):
        self.set_attribute("autocomplete", new_state)

    @property
    def type(self) -> Literal["text", "password", "email", "tel", "url", "search"]:
        """
        type of TextInput

        Options
        -------
        text
            plain text type(default)
        password
            password type
        email
            email type
        tel
            tel(number) type
        url
            url type
        search
            search type
        """
        return self.get_attribute("type")
        
    @type.setter
    def type(self, new_type:Literal["text", "password", "email", "tel", "url", "search"]):
        self.get_attribute("type", new_type.lower())

    @property
    def placeholder(self) -> str:
        """
        placeholder of TextInput
        """
        return self.get_attribute("placeholder")
    
    @placeholder.setter
    def placeholder(self, new_placeholder:str):
        self.set_attribute("placeholder", new_placeholder)

    @property
    def value(self) -> Any:
        """
        value(text) of TextInput
        """
        return self.get_attribute("value")
    
    @value.setter
    def value(self, new_value:Any):
        self.set_attribute("value", str(new_value))

    @property
    def on_changed(self) -> MethodType:
        """
        changed event of TextInput

        event: MethodType[value:Any]
        """
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

    def __on_changed(self, value:Any):
        if self.__on_change:
            self.__on_change(value)

class NumberInput(_Input):
    """
    NumberInput Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        NumberInput Widget

        Parameters
        ----------
        parent: Layout, required
            parent of NumberInput
        id: str, default None
            id of NumberInput
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of NumberInput
        """
        attributes["type"] = "number"
        super().__init__(parent, id, [ "hufpy-number-input" ] + class_list, attributes)

        self.bind_command("change", "on_changed", [ "value" ])
        self.__on_change = None

        self.min = 0
        self.max = 100
        self.step = 1

    @property
    def min(self) -> int:
        """
        minimum range of NumberInput
        """
        return self.get_attribute("min")
    
    @min.setter
    def min(self, new_min:int):
        self.set_attribute("min", new_min)

    @property
    def max(self) -> int:
        """
        maximum range of NumberInput
        """
        return self.get_attribute("max")
    
    @max.setter
    def max(self, new_max:int):
        self.set_attribute("max", new_max)

    @property
    def step(self) -> int:
        """
        step of NumberInput
        """
        return self.get_attribute("step")
    
    @step.setter
    def step(self, new_step:int):
        self.set_attribute("step", new_step)

    @property
    def value(self) -> int:
        """
        value(number) of NumberInput
        """
        return self.get_attribute("value")
    
    @value.setter
    def value(self, new_value:int):
        self.set_attribute("value", new_value)

    @property
    def on_changed(self) -> MethodType:
        """
        changed event of NumberInput

        event: MethodType[value:int]
        """
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

    def __on_changed(self, value:int):
        if self.__on_change:
            self.__on_change(value)

class FileInput(_Input):
    """
    FileInput Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        FileInput Widget

        Parameters
        ----------
        parent: Layout, required
            parent of FileInput
        id: str, default None
            id of FileInput
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of FileInput
        """
        attributes["type"] = "file"
        super().__init__(parent, id, [ "hufpy-file-input" ] + class_list, attributes)

        self.bind_command("change", "on_selected")
        self.__on_select = None

    @property
    def accept(self) -> List[str]:
        """
        acceptable patterns of FileInput
        """
        return [
            item.strip()
            for item in self.get_attribute("accept").split(",")
        ]
    
    @accept.setter
    def accept(self, new_accept:List[str]):
        self.set_attribute("accept", ",".join(new_accept))

    @property
    def capture(self) -> Literal["user", "environment"]:
        """
        capture type of FileInput

        Options
        -------
        user
        environment
        """
        return self.get_attribute("capture")
    
    @capture.setter
    def capture(self, new_value:Literal["user", "environment"]):
        self.set_attribute("capture", new_value)

    @property
    def multiple(self) -> bool:
        """
        flag to select multiple or not
        """
        return self.get_attribute("multiple")
    
    @multiple.setter
    def multiple(self, new_state:bool):
        self.set_attribute("multiple", new_state)

    @property
    def value(self) -> str:
        """
        selected file of FileInput
        """
        return self.get_attribute("value")
    
    @property
    def files(self) -> List[str]:
        """
        selected files of FileInput
        """
        return self.get_attribute("files")
    
    @property
    def on_selected(self) -> MethodType:
        """
        selected event of FileInput

        event: MethodType[value:str | files:List[str]]
        """
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
        """
        DirectoryInput Widget class
        """
        def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
            """
            DirectoryInput Widget
            only works on windows

            Parameters
            ----------
            parent: Layout, required
                parent of DirectoryInput
            id: str, default None
                id of DirectoryInput
            attributes: dict, default {}
                attributes of DirectoryInput
            """
            attributes["webkitdirectory"] = True
            super().__init__(parent, id, [ "hufpy-directory-input" ] + class_list, attributes)
            self.class_list.remove("hufpy-file-input")

# checkbox
class CheckBox(RowLayout):
    """
    CheckBox Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        CheckBox Widget

        Parameters
        ----------
        parent: Layout, required
            parent of CheckBox
        id: str, default None
            id of CheckBox
        class_list: List[str], default []
            class list of Label
        attributes: dict, default {}
            attributes of CheckBox
        """
        super().__init__(parent, id, class_list, attributes)

        self.__chk = _Input(self, class_list = [ "hufpy-checkbox" ], attributes = { "type": "checkbox" }, auto_attach = True)
        self.__label = Label(self, class_list = [ "hufpy-checkbox-label" ], attributes = { "for": self.__chk.id })
        self.append_child(self.__label)

        self.__chk.bind_command("change", "on_changed", [ "checked" ])
        self.__chk.on_changed = self.__on_changed

    @property
    def text(self) -> str:
        """
        text of CheckBox
        """
        return self.__label.text
    
    @text.setter
    def text(self, new_text:str):
        self.__label.text = new_text

    @property
    def checked(self) -> bool:
        """
        checked state of CheckBox
        """
        return self.__chk.get_attribute("checked")
    
    @checked.setter
    def checked(self, state:bool):
        self.__chk.set_attribute("checked", state)

    @property
    def on_changed(self) -> MethodType:
        """
        changed event of CheckBox

        event: MethodType[checked:bool]
        """
        return self.__chk.on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__chk.on_changed = new_callback

    def __on_changed(self, state:bool):
        if self.__chk.on_changed:
            self.__chk.on_changed(state)

# radio
class Radio(RowLayout):
    """
    Radio Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Radio Widget

        Parameters
        ----------
        parent: Layout, requried
            parent of Radio
        id: str, default None
            id of Radio
        class_list: List[str], default []
            class list of Radio
        attributes: dict, default {}
            attributes of Radio
        """
        super().__init__(parent, id, class_list, attributes)

        self.__radio = _Input(self, class_list = [ "hufpy-radio" ], attributes = { "type": "radio", "name": f"{self.parent.id}_radio" }, auto_attach = True)
        self.__label = Label(self, class_list = [ "hufpy-radio-label" ], attributes = { "for": self.__radio.id })
        self.append_child(self.__label)

        self.__radio.bind_command("change", "on_changed", [ "value" ])

    @property
    def checked(self) -> bool:
        """
        checked state of Radio
        """
        return self.__radio.get_attribute("checked")
    
    @property
    def text(self) -> Any:
        """
        text of Radio
        """
        return self.__radio.get_attribute("value")
    
    @text.setter
    def text(self, new_value:Any):
        self.__radio.set_attribute("value", str(new_value))
        self.__label.text = str(new_value)

    @property
    def on_changed(self) -> MethodType:
        """
        changed event of Radio

        event: MethodType[text:str]
        """
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__radio.on_changed = new_callback

    def __on_changed(self, text:str):
        if self.__radio.on_changed:
            self.__radio.on_changed(text)

# pickers
class DatePicker(_Input):
    """
    DatePicker Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        DatePicker Widget

        Parameters
        ----------
        parent: Layout, required
            parent of DatePicker
        id: str, default None
            id of DatePicker
        class_list: List[str], default []
            class list of DatePicker
        attributes: dict, default {}
            attributes of DatePicker
        """
        super().__init__(parent, id, [ "hufpy-date-picker" ] + class_list, attributes)

        self.type = "date"
        self.bind_command("change", "on_changed", [ "value" ])
        self.__on_change = None

    @property
    def type(self) -> Literal["datetime", "date", "month", "time"]:
        """
        type of DatePicker

        Options
        -------
        datetime
            date + time picker
        date
            date only picker
        month
            year + month picker
        time
            time only picker
        """
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
        """
        value of DatePicker
        """
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
        """
        changed event of DatePicker

        event: MethodType[value:datetime]
        """
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback
    
    def __on_changed(self, value:datetime):
        if self.__on_change:
            self.__on_change(value)

class ColorPicker(RowLayout):
    """
    ColorPicker Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        ColorPicker Widget

        Parameters
        ----------
        parent: Layout, required
            parent of ColorPicker
        id: str, default None
            id of ColorPicker
        class_list: List[str], default []
            class list of ColorPicker
        attributes: dict, default {}
            attributes of ColorPicker
        """
        super().__init__(parent, id, class_list, attributes)

        self.__picker = _Input(self, class_list = [ "hufpy-color-picker" ], attributes = { "type": "color" }, auto_attach = True)
        self.__label = Label(self, class_list = [ "hufpy-color-picker-label" ], attributes = { "for": self.__picker.id })
        self.append_child(self.__label)

        self.__picker.bind_command("change", "on_changed", [ "value" ])

    @property
    def text(self) -> str:
        """
        text of ColorPicker
        """
        return self.__label.text
    
    @text.setter
    def text(self, new_text:str):
        self.__label.text = new_text

    @property
    def value(self) -> str:
        """
        color of ColorPicker
        """
        return self.__picker.get_attribute("value")
    
    @value.setter
    def value(self, new_color:str):
        self.__picker.set_attribute("value", new_color)

    @property
    def on_changed(self) -> MethodType:
        """
        changed event of ColorPicker

        event: MethodType[color:str]
        """
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__picker.on_changed = new_callback

    def __on_changed(self, color:str):
        if self.__picker.on_changed:
            self.__picker.on_changed(color)

# range
class Range(Frame):
    """
    Range Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Range Widget

        Parameters
        ----------
        parent: Layout, required
            parent of Range
        id: str, default None
            id of Range
        class_list: List[str], default []
            class list of Range
        attributes: dict, default {}
            attributes of Range
        """
        super().__init__(parent, id, class_list, attributes)

        self.__range = _Input(self, class_list = [ "hufpy-range" ], attributes = { "type": "range" }, auto_attach = True)
        self.__label = Label(self, class_list = [ "hufpy-range-label" ], attributes = { "for": self.__range.id })
        self.append_child(self.__label)

        self.__range.bind_command("change", "on_changed", [ "value" ])
        self.orient = "horizontal"
        self.min = 0
        self.max = 100
        self.step = 1

    @property
    def text(self) -> str:
        """
        text of Range
        """
        return self.__label.text
    
    @text.setter
    def text(self, new_text:str):
        self.__label.text = new_text

    @property
    def orient(self) -> Literal["horizontal", "vertical"]:
        """
        orient of Range

        Options
        -------
        horizontal
            make Range as horizontal
        vertical
            make Range as vertical
        """
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
        """
        minimum range of Range
        """
        return self.__range.get_attribute("min")
    
    @min.setter
    def min(self, new_min:int):
        self.__range.set_attribute("min", new_min)

    @property
    def max(self) -> int:
        """
        maximum range of Range
        """
        return self.__range.get_attribute("max")
    
    @max.setter
    def max(self, new_max:int):
        self.__range.set_attribute("max", new_max)

    @property
    def step(self) -> int:
        """
        step of Range
        """
        return self.__range.get_attribute("step")
    
    @step.setter
    def step(self, new_step:int):
        self.__range.set_attribute("step", new_step)

    @property
    def value(self) -> int:
        """
        number of Range
        """
        return self.__range.get_attribute("value")
    
    @value.setter
    def value(self, new_value:int):
        self.__range.set_attribute("value", new_value)

    @property
    def on_changed(self) -> MethodType:
        """
        changed event of Range

        event: MethodType[value:int]
        """
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__range.on_changed = new_callback

    def __on_changed(self, value:int):
        if self.__range.on_changed:
            self.__range.on_changed(value)

# combobox
class ComboBox(Layout):
    """
    ComboBox Widget class
    """
    def __init__(self, parent:Layout, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        CheckBox Widget

        Parameters
        ----------
        parent: Layout, required
            parent of ComboBox
        id: str, default None
            id of ComboBox
        class_list: List[str], default []
            class list of ComboBox
        attributes: dict, default {}
            attributes of ComboBox
        """
        super().__init__(parent, "select", [ "hufpy-widget-no-flex", "hufpy-combobox" ], class_list, id, attributes)

        self.__children:List[ComboBoxItem] = []
        self.bind_command("change", "on_index_changed")
        self.bind_command("change", "on_text_changed")
        self.__on_index_change, self.__on_text_change = None, None

    @staticmethod
    def from_list(parent:Layout, items:List[str]) -> "ComboBox":
        """
        create ComboBox from list of items

        Parameters
        ----------
        parent: Layout, required
            parent of generated ComboBox
        items: List[str], required
            source for ComboBox

        Return
        ------
        combobox: ComboBox
            generated ComboBox
        """
        cb = ComboBox(parent)
        for item in items:
            child = ComboBoxItem(cb)
            child.text = item

        return cb

    @property
    def children(self) -> List["ComboBoxItem"]:
        """
        children of ComboBox

        Return
        ------
        children: List[ComboBoxItem]
        """
        return self.__children

    @property
    def current_index(self) -> int:
        """
        index of selected item of ComboBox
        """
        for idx, child in enumerate(self.children):
            if child.value == self.get_attribute("value"):
                return idx

    @current_index.setter
    def current_index(self, new_index:int):
        for idx, child in enumerate(self.children):
            child.selected = False
        
        self.children[new_index].selected = True

    @property
    def current_text(self) -> str:
        """
        text of selected item of ComboBox
        """
        return self.get_attribute("value")

    @current_text.setter
    def current_text(self, new_text:str):
        for child in self.children:
            child.selected == child.text == new_text

    @property
    def on_index_changed(self) -> MethodType:
        """
        index changed event of ComboBox

        event: MethodType[index:int]
        """
        return self.__on_index_changed

    @on_index_changed.setter
    def on_index_changed(self, new_callback:MethodType):
        self.__on_index_change = new_callback

    def __on_index_changed(self):
        if self.__on_index_change:
            self.__on_index_change(self.current_index)

    @property
    def on_text_changed(self) -> MethodType:
        """
        text changed event of ComboBox

        event: MethodType[text:str]
        """
        return self.__on_text_changed
    
    @on_text_changed.setter
    def on_text_changed(self, new_callback:MethodType):
        self.__on_text_change = new_callback

    def __on_text_changed(self):
        if self.__on_text_change:
            self.__on_text_change(self.current_text)

class ComboBoxItem(Widget):
    """
    ComboBox Item Widget class
    """
    def __init__(self, parent:ComboBox):
        """
        ComboBoxItem Widget

        Parameters
        ----------
        parent: ComboBox, required
            parent ComboBox of ComboBoxItem
        """
        super().__init__(parent, "option", [ "hufpy-combobox-item" ], auto_attach = True)

    @property
    def text(self) -> Any:
        """
        text of ComboBoxItem
        """
        return self.get_attribute("value")
    
    @text.setter
    def text(self, new_value:Any):
        self.set_attribute("value", new_value)
        self.set_attribute("text", new_value)

    @property
    def selected(self) -> bool:
        """
        selected state of ComboBoxItem
        """
        return self.get_attribute("selected")
    
    @selected.setter
    def selected(self, new_state:bool):
        self.set_attribute("selected", new_state)
