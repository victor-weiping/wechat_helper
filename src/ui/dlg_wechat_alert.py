# -*- coding: utf-8 -*-
#
from win.pywin import PyWin
from helper.my_logging import *

class DlgWeChatAlert:
    def __init__(self, dlg):
        self.dlg = dlg

    def get_title(self):
        return PyWin.find_child_item(self.dlg, [1, 0, 0, 0])

    def get_message(self):
        return PyWin.find_child_item(self.dlg, [1, 0, 1, 1])

    def get_ok_button(self):
        return PyWin.find_child_item(self.dlg, [1, 0, 2, 0])

    def get_cancel_button(self):
        return PyWin.find_child_item(self.dlg, [1, 0, 2, 1])

    def click_ok(self):
        ok = self.get_ok_button()
        PyWin.click_control(ok)

    def click_cancel(self):
        ok = self.get_cancel_button()
        PyWin.click_control(ok)
