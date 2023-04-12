# -*- coding: utf-8 -*-
import os, sys, pandas as pd
from datetime import datetime
from hufpy import Application, __path__
from hufpy.widgets.layouts import ColumnLayout, RowLayout, FieldSet
from hufpy.widgets import (
    Label, Image, Button, ToggleButton,
    Tab, TabItem,
    Table, TableColumn, TableRow, TableItem
)
from hufpy.widgets.inputs import (
    TextInput, NumberInput, FileInput,
    CheckBox, Radio,
    DatePicker, ColorPicker,
    Range,
    ComboBox
)
if sys.platform == "win32":
    from hufpy.widgets.inputs import DirectoryInput


Application.init(width = 1000, height = 800)

class WidgetShowcase(ColumnLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.spacing = 5

        fs_input = FieldSet(self)
        fs_input.title = "inputs"
        self.append_child(fs_input)

        row_input = RowLayout(fs_input)
        row_input.spacing = 5
        fs_input.append_child(row_input)

        ti = TextInput(row_input)
        ti.placeholder = "placeholder"
        ti.on_changed = self.on_text_changed
        row_input.append_child(ti)

        ni = NumberInput(row_input)
        ni.value = 50
        ni.on_changed = self.on_number_changed
        row_input.append_child(ni)

        fi = FileInput(row_input)
        fi.on_selected = self.on_file_selected
        row_input.append_child(fi)

        if sys.platform == "win32":
            di = DirectoryInput(row_input)
            di.on_selected = self.on_directory_selected
            row_input.append_child(di)


        fs_chk_rdo = FieldSet(self)
        fs_chk_rdo.title = "checkbox / radio"
        self.append_child(fs_chk_rdo)

        col_chk_rdo = ColumnLayout(fs_chk_rdo)
        col_chk_rdo.spacing = 5
        fs_chk_rdo.append_child(col_chk_rdo)

        chk = CheckBox(col_chk_rdo)
        chk.text = "checkbox"
        chk.checked = True
        chk.on_changed = self.on_chk_changed
        col_chk_rdo.append_child(chk)

        radio_row = RowLayout(col_chk_rdo)
        radio_row.spacing = 5
        col_chk_rdo.append_child(radio_row)

        radio1 = Radio(radio_row)
        radio1.value = "1234"
        radio1.on_changed = self.on_radio_changed
        radio_row.append_child(radio1)

        radio2 = Radio(radio_row)
        radio2.value = "5678"
        radio2.on_changed = self.on_radio_changed
        radio_row.append_child(radio2)


        fs_picker = FieldSet(self)
        fs_picker.title = "pickers"
        self.append_child(fs_picker)

        col_date = ColumnLayout(fs_picker)
        col_date.spacing = 5
        fs_picker.append_child(col_date)

        date_row = RowLayout(col_date)
        date_row.spacing = 5
        col_date.append_child(date_row)

        dp_dt = DatePicker(date_row)
        dp_dt.type = "datetime"
        dp_dt.on_changed = self.on_dpdatetime_changed
        date_row.append_child(dp_dt)

        dp_d = DatePicker(date_row)
        dp_d.type = "date"
        dp_d.on_changed = self.on_dpdate_changed
        date_row.append_child(dp_d)

        dp_m = DatePicker(date_row)
        dp_m.type = "month"
        dp_m.on_changed = self.on_dpmonth_changed
        date_row.append_child(dp_m)

        dp_t = DatePicker(date_row)
        dp_t.type = "time"
        dp_t.on_changed = self.on_dptime_changed
        date_row.append_child(dp_t)

        cp = ColorPicker(col_date)
        cp.text = "test color"
        cp.value = "red"
        cp.on_changed = self.on_color_changed
        col_date.append_child(cp)


        fs_range = FieldSet(self)
        fs_range.title = "ranges"
        self.append_child(fs_range)

        row_range = RowLayout(fs_range)
        row_range.spacing = 5
        fs_range.append_child(row_range)

        h_range = Range(row_range)
        h_range.text = "test range"
        h_range.value = 10
        h_range.on_changed = self.on_hrange_changed
        row_range.append_child(h_range)

        v_range = Range(row_range)
        v_range.orient = "vertical"
        v_range.text = "vertical range"
        v_range.value = 20
        v_range.on_changed = self.on_vrange_changed
        row_range.append_child(v_range)


        cb = ComboBox.from_list(self, [ "option 1", "option 2" ])
        cb.current_text = "option2"
        cb.on_index_changed = self.on_cb_index_changed
        cb.on_text_changed = self.on_cb_text_changed
        self.append_child(cb)


        fs_display = FieldSet(self)
        fs_display.title = "displays"
        self.append_child(fs_display)

        row_display = RowLayout(fs_display)
        row_display.spacing = 5
        fs_display.append_child(row_display)

        label = Label(row_display)
        label.text = "12341234"
        row_display.append_child(label)

        img = Image(row_display)
        img.width = 100
        img.height = 100
        img.source = os.path.join(__path__[0], "assets", "icons", "icon.png")
        row_display.append_child(img)


        fs_button = FieldSet(self)
        fs_button.title = "buttons"
        self.append_child(fs_button)

        row_button = RowLayout(fs_button)
        row_button.spacing = 5
        fs_button.append_child(row_button)

        btn = Button(row_button)
        btn.text = "button"
        btn.on_clicked = self.on_btn_clicked
        row_button.append_child(btn)

        toggle_btn = ToggleButton(row_button)
        toggle_btn.text = "toggle button"
        toggle_btn.on_toggled = self.on_btn_toggled
        row_button.append_child(toggle_btn)


    def on_text_changed(self, text:str):
        print("text input: ", text)

    def on_number_changed(self, value:int):
        print("number input: ", value)

    def on_file_selected(self, file:str):
        print("file input: ", file)

    def on_directory_selected(self, directory:str):
        print("directory input: ", directory)

    def on_chk_changed(self, state:bool):
        print("checkbox: ", state)

    def on_radio_changed(self, value:str):
        print("radio: ", value)

    def on_dpdatetime_changed(self, date:datetime):
        print("datetime picker: ", date)

    def on_dpdate_changed(self, date:datetime):
        print("date picker: ", date)

    def on_dpmonth_changed(self, date:datetime):
        print("month picker: ", date)

    def on_dptime_changed(self, date:datetime):
        print("time picker: ", date)

    def on_color_changed(self, color:str):
        print("color: ", color)

    def on_hrange_changed(self, value:int):
        print("horizontal range: ", value)

    def on_vrange_changed(self, value:int):
        print("vertical range: ", value)

    def on_cb_index_changed(self, index:int):
        print("combobox index: ", index)

    def on_cb_text_changed(self, text:str):
        print("combobox text: ", text)

    def on_btn_clicked(self):
        print("button clicked!")

    def on_btn_toggled(self, state:bool):
        print("toggle button: ", state)

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


class MyTab(Tab):
    def __init__(self):
        super().__init__()

        tab1 = TabItem(self)
        tab1.title = "widget showcase"
        tab1.content = WidgetShowcase(tab1)

        tab2 = TabItem(self)
        tab2.title = "table showcase"
        tab2.content = TableShowcase(tab2)

Application.run(MyTab, debug = True)
