# -*- coding: utf-8 -*-
from hufpy import Application
from hufpy.widgets import (
    Tab, TabItem
)

from views.WidgetShowcase import WidgetShowcase
from views.TableShowcase import TableShowcase


Application.init(width = 1000, height = 800)

class MainView(Tab):
    def __init__(self):
        super().__init__()

        tab1 = TabItem(self)
        tab1.title = "widget showcase"
        tab1.content = WidgetShowcase(tab1)

        tab2 = TabItem(self)
        tab2.title = "table showcase"
        tab2.content = TableShowcase(tab2)

Application.run(MainView, debug = True)
