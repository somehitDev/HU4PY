# -*- coding: utf-8 -*-
import pandas as pd
from ast import literal_eval
from typing import List, Dict, Any, Literal
from types import MethodType
from ._base import Widget, Layout


class TableHeader(Layout):
    def __init__(self, parent:"Table", id:str = None, attributes:dict = {}):
        super().__init__(parent, "thead", [ "hufpy-widget-no-flex", "hufpy-table-header" ], id, attributes, True)

    @property
    def children(self) ->  List["TableColumn"]:
        return super().children

class TableBody(Layout):
    def __init__(self, parent:"Table", id:str = None, attributes:dict = {}):
        super().__init__(parent, "tbody", [ "hufpy-widget-no-flex", "hufpy-table-body" ], id, attributes, True)

    @property
    def children(self) -> List["TableRow"]:
        return super().children

class Table(Layout):
    def __parse_value(self, source:str) -> Any:
        try:
            value = float(source)
            if value == int(value):
                return int(value)
            else:
                return value
        except:
            pass

        try:
            return int(source)
        except:
            pass

        try:
            return literal_eval(source)
        except:
            pass

        try:
            return eval(source)
        except:
            pass

        return source

    def __init__(self, parent:Layout = None, id:str = None, attributes:dict = {}):
        super().__init__(parent, "table", [ "hufpy-widget-no-flex", "hufpy-table" ], id, attributes)

        self.__header = TableHeader(self, self.id + "_header")
        self.__body = TableBody(self, self.id + "_body")

        self.__on_click, self.__on_change = None, None

    @property
    def header(self) -> TableHeader:
        return self.__header
    
    @property
    def body(self) -> TableBody:
        return self.__body
    
    @property
    def on_clicked(self) -> MethodType:
        return self.__on_clicked
    
    @on_clicked.setter
    def on_clicked(self, new_callback:MethodType):
        self.__on_click = new_callback

    def __on_clicked(self, target_item:Widget):
        if self.__on_click:
            ridx, cidx = 0, 0
            for row_idx, row in enumerate(self.body.children):
                for child_idx, child in enumerate(row.children):
                    if child == target_item:
                        ridx, cidx = row_idx, child_idx

            self.__on_click(ridx, cidx)

    @property
    def on_changed(self) -> MethodType:
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

    def __on_changed(self, target_item:Widget, value:str):
        if self.__on_change:
            ridx, cidx = 0, 0
            for row_idx, row in enumerate(self.body.children):
                for child_idx, child in enumerate(row.children):
                    if child == target_item:
                        ridx, cidx = row_idx, child_idx

            self.__on_change(ridx, cidx, value)
    
    @staticmethod
    def from_pandas(parent:Layout, source:pd.DataFrame) -> "Table":
        table = Table(parent)
        if not source.empty:
            for column in source.columns:
                tcol = TableColumn(table)
                tcol.title = column
                # table.header.append_child(tcol)

            for row in source.values:
                trow = TableRow(table)
                for value in row:
                    titem = TableItem(trow)
                    titem.text = str(value)
                    trow.append_child(titem)

                # table.body.append_child(trow)

        return table
    
    def to_pandas(self) -> pd.DataFrame:
        datas = []
        for row in self.body.children:
            data_row = []
            for child in row.children:
                if isinstance(child, TableItem):
                    data_row.append(self.__parse_value(child.text))
                else:
                    try:
                        data_row.append(self.__parse_value(child.text))
                    except:
                        data_row.append(self.__parse_value(child.value))

            datas.append(data_row)

        return pd.DataFrame(datas, columns = [ column.title for column in self.header.children ])

    @staticmethod
    def from_datas(parent:Layout, source:List[Dict[str, Any]]):
        table = Table(parent)
        if len(source) > 0:
            for column in source[0].keys():
                tcol = TableColumn(table)
                tcol.title = column
                # table.header.append_child(tcol)

            for row in source:
                trow = TableRow(table)
                for value in row.values():
                    titem = TableItem(trow)
                    titem.text = str(value)
                    trow.append_child(titem)

                # table.body.append_child(trow)

        return table
    
    def to_datas(self) -> List[Dict[str, Any]]:
        datas = []
        for row in self.body.children:
            data_row = {}
            for column, child in zip(self.header.children, row.children):
                if isinstance(child, TableItem):
                    data_row[column.title] = self.__parse_value(child.text)
                else:
                    try:
                        data_row[column.title] = self.__parse_value(child.text)
                    except:
                        data_row[column.title] = self.__parse_value(child.value)

            datas.append(data_row)

        return datas

class TableColumn(Layout):
    def __init__(self, parent:Table = None, id:str = None, attributes:dict = {}):
        super().__init__(parent.header, "th", [ "hufpy-widget-no-flex", "hufpy-table-column" ], id, attributes)
        parent.header.append_child(self)

    @property
    def title(self) -> str:
        return self.get_attribute("text")
    
    @title.setter
    def title(self, new_title:str):
        self.set_attribute("text", new_title)

    @property
    def horizontal_align(self) -> Literal["default", "left", "center", "right"]:
        return self.style.pop("text-align", "default")

    @horizontal_align.setter
    def horizontal_align(self, new_align:Literal["default", "left", "center", "right"]):
        if new_align == "default":
            self.remove_style_property("text-align")
        else:
            self.update_style_property("text-align", new_align)

    @property
    def vertical_align(self):
        raise DeprecationWarning("")

class TableRow(Layout):
    def __init__(self, parent:Table = None, id:str = None, attributes:dict = {}):
        super().__init__(parent.body, "tr", [ "hufpy-widget-no-flex", "hufpy-table-row" ], id, attributes, True)

        self.__table = parent

    @property
    def children(self) -> List["TableItem"]:
        return super().children
    
    def append_child(self, widget:Widget, apply_html:bool = True):
        widget.bind_command("click", "on_clicked", [ "self" ], self.__table.id)
        widget.bind_command("change", "on_changed", [ "self", "value" ], self.__table.id)

        super().append_child(widget, apply_html)

class TableItem(Widget):
    def __init__(self, parent:TableRow):
        super().__init__(parent, "td", [ "hufpy-widget-no-flex", "hufpy-table-item" ])

    @property
    def text(self) -> str:
        return self.get_attribute("text")
    
    @text.setter
    def text(self, new_text:str):
        self.set_attribute("text", new_text)

    @property
    def horizontal_align(self) -> Literal["default", "left", "center", "right"]:
        return self.style.pop("text-align", "default")

    @horizontal_align.setter
    def horizontal_align(self, new_align:Literal["default", "left", "center", "right"]):
        if new_align == "default":
            self.remove_style_property("text-align")
        else:
            self.update_style_property("text-align", new_align)

    @property
    def vertical_align(self):
        raise DeprecationWarning("")
