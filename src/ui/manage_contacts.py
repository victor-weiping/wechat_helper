# -*- coding: utf-8 -*-
#
from win.pywin import PyWin
from ui.person_info import PersonInfo
from helper.my_logging import *

class ManageContacts:
    def __init__(self, win):
        self.win = win

    def close(self):
        button = PyWin.find_child_window(self.win, 'Close', 'Button')
        PyWin.click_control(button)

    # callback(json_data)
    def list_contacts(self, callback):
        list = self.find_contact_list()
        self.set_focus_top_item(list)
        item0 = None
        count = 0
        while True:
            item = self.get_focus_item(list)
            if item == None:    # None: did not find selected item
                logger.warning('lost selected item.')
                break
            if item == item0:
                break
            if callback:
                callback(self.get_data(item))
            item0 = item
            count += 1
            list.type_keys('{DOWN}')
        return count

    def set_focus_top_item(self, list):
        # cancel all selections if there is
        selected = PyWin.find_child_window(self.win, "取消选择", "Button", warning=False)
        if selected != None:
            PyWin.click_control(selected)
        # select then de-select
        PyWin.click_control(list, 'top-left')
        PyWin.click_control(list, 'top-left')
        # control-home to top
        list.type_keys('^{HOME}')
        return self.get_focus_item(list)

    def get_focus_item(self, list):
        items = PyWin.get_children(list, 'ListItem')
        for item in items:
            if item.is_selected():
                return item
        return None

    def get_data(self, item):
        data = {}
        pic = self.get_item_pic(item)
        PyWin.click_control(pic)
        win = PyWin.find_child_window(self.win, 'WeChat', 'Pane')
        person_info = PersonInfo(win)
        data = person_info.get_person_info()
        person_info.close()
        return data

    def find_contact_list(self):
        # 当tags list打开后，会有两个同样的list，要找右边一个。rect.left > 200
        list = PyWin.find_child_window(self.win, '', 'List')
        pos = list.rectangle().left - self.win.rectangle().left
        if pos < 200:
            list = PyWin.find_child_window(self.win, '', 'List', 1)
        list.draw_outline()
        return list

    def get_item_pic(self, item):
        return PyWin.find_child_item(item, [0, 0, 1, 0])

    def get_item_text(self, item):
        control = PyWin.find_child_item(item, [0, 0, 1, 1])
        return PyWin.get_window_text(control)

    def get_item_alias(self, item):
        control = PyWin.find_child_item(item, [0, 0, 2, 0, 0])
        alias = PyWin.get_window_text(control)
        if alias == 'Add Remarks':
            alias = ''
        return alias

    def get_item_tag(self, item):
        control = PyWin.find_child_item(item, [0, 0, 3, 0, 0])
        tag = PyWin.get_window_text(control)
        if tag == 'Add Tag':
            tag = ''
        return tag.split('，')
