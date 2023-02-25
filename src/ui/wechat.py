# -*- coding: utf-8 -*-
#
import time
from helper.my_logging import *
from win.pywin import PyWin
from ui.contacts import Contacts
from ui.chats import Chats
from ui.settings import Settings

logger = getMyLogger(__name__)

class WeChat:
    def __init__(self):
        self.wechat = PyWin.connect_wechat()
        if self.wechat == None:
            logger.error('did not find WeChat !')
            quit()

        # raise wechat window on top
        self.wechat.set_focus()

        # logger.info('WeChat version: "%s"', self.get_version())

        # switch ime to english, do not have to do selection at input
        self.ime_english()

    # 点击菜单,换到Chats界面
    def click_chats(self):
        button = PyWin.find_child_window(self.wechat, 'Chats', 'Button')
        PyWin.click_control(button)

    # 点击菜单: Contacts，换到Contacts界面
    def click_contacts(self):
        button = PyWin.find_child_window(self.wechat, 'Contacts', 'Button')
        PyWin.click_control(button)

    # 点击菜单: More|Settings，换到Settinigs界面
    def click_more(self):
        button = PyWin.find_child_window(self.wechat, 'More', 'Button')
        PyWin.click_control(button)

    # Settings menu
    def click_settings(self):
        button = PyWin.find_child_window(self.wechat, 'Settings', 'Button')
        PyWin.click_control(button)

    def ime_english(self):
        lang = PyWin.get_language(self.wechat)
        if lang != 'English':
            time.sleep(0.2)
            logger.info('change language to English')
            self.wechat.type_keys('%+') # Alt-Shift
            time.sleep(0.2)
            lang = PyWin.get_language(self.wechat)

    def get_version(self):
        # 点击菜单: More|Settings，换到Settinigs界面
        self.click_more()
        self.click_settings()

        win = PyWin.find_top_window('Settings')
        settings = Settings(win)
        version = settings.get_version()
        settings.close()
        return version

    def list_contacts(self, callback=None):
        # 点击菜单: Contacts，确保换到Contacts界面
        for i in range(3):
            self.click_contacts()
            time.sleep(0.2)
            win = PyWin.find_child_window(self.wechat, 'Contacts', 'List')
            if win:
                contacts = Contacts(self.wechat)
                return contacts.list_contacts(callback)

    def list_saved_groups(self, callback):
        # 点击菜单: Contacts，换到Contacts界面
        self.click_contacts()

        # 从contacts收集名单
        contacts = Contacts(self.wechat)
        return contacts.list_saved_groups(callback)

    def forward_msg(self, args):
        # 点击菜单,换到Chats界面
        self.click_chats()
        chats = Chats(self.wechat)
        return chats.forward_msg(args)

    def invite_join_group(self, args):
        # 点击菜单,换到Chats界面
        self.click_chats()

        chats = Chats(self.wechat)
        chats.invite_join_group(args)

    def list_group_members(self, args, callback):
        # 点击菜单,换到Chats界面
        self.click_chats()

        chats = Chats(self.wechat)
        chats.list_group_members(args, callback)

    def remove_group_members(self, args):
        # 点击菜单,换到Chats界面
        self.click_chats()

        chats = Chats(self.wechat)
        chats.remove_group_members(args)

    def dump_chat_msgs(self, args):
        # 点击菜单,换到Chats界面
        self.click_chats()

        chats = Chats(self.wechat)
        chats.dump_chat_msgs(args)
