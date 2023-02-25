# -*- coding: utf-8 -*-
#
import time
from win.pywin import PyWin
from ui.manage_contacts import ManageContacts
from helper.my_logging import *

logger = getMyLogger(__name__)

class Contacts:
    def __init__(self, wechat):
        self.wechat = wechat
        self.chats = None

    # --- list contacts
    def list_contacts(self, callback):
        item = self.get_manage_contacts()
        if item == None:
            return

        # 点击，跳出 Manage Contacts窗口
        for i in range(3):
            PyWin.click_control(item)
            time.sleep(0.2)
            win = PyWin.find_top_window('Manage Contacts')
            if win:
                manage_contacts = ManageContacts(win)
                n = manage_contacts.list_contacts(callback)
                manage_contacts.close()
                return n

    def get_contacts_list(self):
        return PyWin.find_child_window(self.wechat, 'Contacts', 'List')

    # --- list saved groups
    def list_saved_groups(self, callback):
        list = self.get_contacts_list()
        # set focus to the list to receive keyboard input
        PyWin.click_control(list)
        list.type_keys('^{HOME}')

        # go throught list to find section of 'Saved Groups'
        saved_groups = False
        while True:
            items = PyWin.get_children(list, 'ListItem')
            index = self.get_focus_index(items)
            text = PyWin.get_window_text(items[index-1])
            if index > 0 and text == '':
                # get category name
                category = PyWin.find_child_item(items[index-1], [0, 0])
                name = PyWin.get_window_text(category)
                if name == 'Saved Groups':
                    saved_groups = True
                    logger.info('category: "%s"', name)
                elif saved_groups:
                    # has passed 'saved group' section
                    break

            if saved_groups:
                item = items[index]
                pic = PyWin.find_child_item(item, [0, 0])
                pic = PyWin.get_image(pic)
                name = PyWin.get_window_text(item)
                callback({'name':name, 'pic':pic})
            list.type_keys('{DOWN}')
        return

    def get_focus_index(self, items):
        for i in range(len(items)):
            if items[i].is_selected():
                return i
        return None

    # 从Contact List中找到 "Manage Contacts"
    def get_manage_contacts(self):
        list = self.get_contacts_list()
        PyWin.click_control(list)
        list.type_keys('^{HOME}')

        # Ctrl+Home不能到顶，需要滚屏
        PyWin.mouse_scroll(list, 10)     # scroll content down
        item = PyWin.find_child_window(self.wechat, 'Manage Contacts', 'Button')
        if item == None:
            logger.warning('did not find "Manage Contacts"')
            return None
        return item
