# -*- coding: utf-8 -*-
#
import time
from win.pywin import PyWin as pywin
from ui.chat_info import ChatInfo
from helper.my_logging import *

# 双击对话列表中的朋友，跳出的独立对话屏幕窗口
class Chatting:
    def __init__(self, win):
        self.win = win
        self.members = []

    def get_friend_name(self):
        return self.win.window_text()

    def get_members(self):
        button = pywin.find_child_window(self.win, 'Chat Info', 'Button')
        if not button.exists():
            logger.warning("did not find button")
            return None

        for i in range(3):
            pywin.click_control(button)
            time.sleep(0.5)
            win = pywin.find_child_window(self.win, "Chat Info", "Window", 0, False)
            if win:
                break
        if win.exists():
            chat_info = ChatInfo(win)
            chat_info.get_members(self.save_info)
            chat_info.close()
            return self.members
        return None

    def save_info(self, info):
        self.members.append(info)

    def close(self):
        close = pywin.find_child_window(self.win, 'Close', 'Button')
        pywin.click_control(close)
