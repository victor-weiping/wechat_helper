# -*- coding: utf-8 -*-
#
from win.pywin import PyWin

class Settings:
    def __init__(self, win):
        self.win = win

    def get_version(self):
        about = PyWin.find_child_window(self.win, 'About', 'TabItem')
        PyWin.click_control(about)

        update = PyWin.find_child_window(self.win, 'Update', 'Button')
        version = PyWin.find_child_item(update.parent(), [0,0])
        return PyWin.get_window_text(version)

    def close(self):
        close = PyWin.find_child_window(self.win, 'Close', 'Button')
        PyWin.click_control(close)
