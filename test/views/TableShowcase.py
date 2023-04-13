# -*- coding: utf-8 -*-
import pandas as pd
from hufpy.widgets.layouts import ColumnLayout, FieldSet
from hufpy.widgets import (
    Table, TableColumn, TableRow, TableItem
)


class TableShowcase(ColumnLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.spacing = 5

        fs_manual = FieldSet(self)
        fs_manual.title = "manual"
        self.append_child(fs_manual)

        tb_m = Table(fs_manual)
        tb_m.on_clicked = self.on_item_clicked
        # tb_m.on_changed = self.on_item_changed
        fs_manual.append_child(tb_m)

        for idx in range(4):
            TableColumn(tb_m).title = f"column {idx + 1}"

        for ridx in range(4):
            tr_m = TableRow(tb_m)
            for cidx in range(4):
                titem = TableItem(tr_m)
                titem.text = f"item {ridx + 1}x{cidx + 1}"
                # titem = TextInput(tr_m)
                # titem.value = f"item {ridx + 1}x{cidx + 1}"
                tr_m.append_child(titem)


        fs_data = FieldSet(self)
        fs_data.title = "from datas"
        self.append_child(fs_data)

        table_datas = [ { "col1": 1.3, "col2": "data1" }, { "col1": 2, "col2": "data2" } ]
        tb_d = Table.from_datas(fs_data, table_datas)
        # print(tb_d.to_datas())
        fs_data.append_child(tb_d)


        fs_pandas = FieldSet(self)
        fs_pandas.title = "from pandas"
        self.append_child(fs_pandas)

        tb_p = Table.from_pandas(fs_pandas, pd.DataFrame.from_dict(table_datas))
        # print(tb_d.to_pandas())
        fs_pandas.append_child(tb_p)

    def on_item_clicked(self, ridx:int, cidx:int):
        print(f"ridx: {ridx} / cidx: {cidx}")

    def on_item_changed(self, ridx:int, cidx:int, value:str):
        print(f"ridx: {ridx} / cidx: {cidx} / value: {value}")
