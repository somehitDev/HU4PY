# -*- coding: utf-8 -*-
import pandas as pd
from ast import literal_eval
from typing import List, Dict, Any, Literal
from types import MethodType
from ._base import Widget, Layout


class TableHeader(Layout):
    """
    Table Header Layout class
    """
    def __init__(self, parent:"Table", id:str = None, attributes:dict = {}):
        """
        TableHeader (same as thead)

        Parameters
        ----------
        parent: Table, required
            parent Table of TableHeader
        id: str, default None
            id of TableHeader
        class_list: List[str], default []
            class list of TableHeader
        attributes: dict, default {}
            attributes of TableHeader
        """
        super().__init__(parent, "thead", [ "hufpy-widget-no-flex", "hufpy-table-header" ], [], id, attributes, True)

    @property
    def children(self) ->  List["TableColumn"]:
        """
        children of TableHeader

        Return
        ------
        children: List[TableColumn]
        """
        return super().children

class TableBody(Layout):
    """
    Table Body Layout class
    """
    def __init__(self, parent:"Table", id:str = None, attributes:dict = {}):
        """
        TableBody (same as tbody)

        Parameters
        ----------
        parent: Table, required
            parent Table of TableBody
        id: str, default None
            id of TableBody
        attributes: dict, default {}
            attributes of TableBody
        """
        super().__init__(parent, "tbody", [ "hufpy-widget-no-flex", "hufpy-table-body" ], [], id, attributes, True)

    @property
    def children(self) -> List["TableRow"]:
        """
        children of TableBody

        Return
        ------
        children: List[TableRow]
        """
        return super().children

class Table(Layout):
    """
    Table Layout class
    """
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

    def __init__(self, parent:Layout = None, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        Table

        Parameters
        ----------
        parent: Layout, default None
            parent of Table
        id: str, default None
            id of Table
        class_list: List[str], default []
            class list of Table
        attributes: dict, default {}
            attributes of Table
        """
        super().__init__(parent, "table", [ "hufpy-widget-no-flex", "hufpy-table" ], class_list, id, attributes)

        self.__header = TableHeader(self, self.id + "_header")
        self.__body = TableBody(self, self.id + "_body")

        self.__on_click, self.__on_change = None, None

    @property
    def header(self) -> TableHeader:
        """
        TableHeader of Table

        Return
        ------
        header: TableHeader
        """
        return self.__header
    
    @property
    def body(self) -> TableBody:
        """
        TableBody of Table

        Return
        ------
        body: TableBody
        """
        return self.__body
    
    @property
    def on_clicked(self) -> MethodType:
        """
        clicked event of Table

        event: MethodType[ridx:int, cidx:int]
        """
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
        """
        changed event of Table

        event: MethodType[ridx:int, cidx:int, value:Any]
        """
        return self.__on_changed
    
    @on_changed.setter
    def on_changed(self, new_callback:MethodType):
        self.__on_change = new_callback

    def __on_changed(self, target_item:Widget, value:Any):
        if self.__on_change:
            ridx, cidx = 0, 0
            for row_idx, row in enumerate(self.body.children):
                for child_idx, child in enumerate(row.children):
                    if child == target_item:
                        ridx, cidx = row_idx, child_idx

            self.__on_change(ridx, cidx, value)
    
    @staticmethod
    def from_pandas(parent:Layout, source:pd.DataFrame) -> "Table":
        """
        create Table from pandas.DataFrame

        Parameters
        ----------
        parent: Layout, required
            parent of generated Table
        source: pandas.DataFrame, required
            source for Table

        Return
        ------
        table: Table
            generated Table from source
        """
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
        """
        convert pandas.DataFrame from Table

        Return
        ------
        dataframe: pandas.DataFrame
            converted DataFrame from Table
        """
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
        """
        create Table from list of dictionaries

        Parameters
        ----------
        parent: Layout, required
            parent of generated Table
        source: List[Dict[str, Any]], required
            source for Table

        Return
        ------
        table: Table
            generated Table from source
        """
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
        """
        convert list of dictionaries from Table

        Return
        ------
        datas: List[Dict[str, Any]]
            converted data from Table
        """
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

class TableColumn(Widget):
    """
    Table Column Widget class
    """
    def __init__(self, parent:Table, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        TableColumn (same as th)

        Parameters
        ----------
        parent: Table, required
            parent Table of TableColumn
        id: str, default None
            id of TableColumn
        class_list: List[str], default []
            class list of TableColumn
        attributes: dict, default {}
            attributes of TableColumn
        """
        super().__init__(parent.header, "th", [ "hufpy-widget-no-flex", "hufpy-table-column" ], class_list, id, attributes)
        parent.header.append_child(self)

    @property
    def title(self) -> str:
        """
        title of TableColumn
        """
        return self.get_attribute("text")
    
    @title.setter
    def title(self, new_title:str):
        self.set_attribute("text", new_title)

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
    """
    Table Row Layout class
    """
    def __init__(self, parent:Table, id:str = None, class_list:List[str] = [], attributes:dict = {}):
        """
        TableRow (same as tr)

        Parameters
        ----------
        parent: Table, requried
            parent Table of TableRow
        id: str, default None
            id of TableRow
        class_list: List[str], default []
            class list of TableRow
        attributes: dict, default {}
            attributes of TableRow
        """
        super().__init__(parent.body, "tr", [ "hufpy-widget-no-flex", "hufpy-table-row" ], class_list, id, attributes, True)

        self.__table = parent

    @property
    def children(self) -> List["TableItem"]:
        """
        children of TableRow

        Return
        ------
        children: List[TableItem]
        """
        return super().children
    
    def append_child(self, widget:Widget, apply_html:bool = True):
        """
        append widget to layout

        Parameters
        ----------
        widget: Widget or Layout, required
            widget to append
        apply_html: bool, default True
            flag to attach element to Layout
        """
        widget.bind_command("click", "on_clicked", [ "self" ], self.__table.id)
        widget.bind_command("change", "on_changed", [ "self", "value" ], self.__table.id)

        super().append_child(widget, apply_html)

class TableItem(Widget):
    """
    Table Item Widget class
    """
    def __init__(self, parent:TableRow):
        """
        TableItem (same as td)

        Parameters
        ----------
        parent: TableRow
            parent TableRow of TableItem
        """
        super().__init__(parent, "td", [ "hufpy-widget-no-flex", "hufpy-table-item" ])

    @property
    def text(self) -> str:
        """
        text of TableItem
        """
        return self.get_attribute("text")
    
    @text.setter
    def text(self, new_text:str):
        self.set_attribute("text", new_text)

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
