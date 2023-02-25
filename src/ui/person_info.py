# -*- coding: utf-8 -*-
#
from win.pywin import PyWin
from helper.my_logging import *

class PersonInfo:
    def __init__(self, win):
        self.win = win

    # find information based on tree structure, this does work faster than find_child_window
    # however this is highly wechat version dependent !!
    def get_person_info(self):
        info = {}
        node = PyWin.find_child_item(self.win, [1, 0, 0, 0, 0, 0])
        info['pic'] = PyWin.get_image(node)

        name = PyWin.get_window_text(PyWin.find_child_item(node, [-1, 1, 0, 0, 0]))
        info['name'] = name

        # group 1 for 'more', 'WeChat ID', 'Region'
        group1 = PyWin.find_child_item(node, [-1, 1, 1, 0])
        items = PyWin.get_children(group1)
        for item in items:
            name = PyWin.get_window_text(PyWin.find_child_item(item, [0]))
            value = PyWin.get_window_text(PyWin.find_child_item(item, [1]))
            if 'Group Alias' in name:
                info['group_alias'] = value
            elif 'WeChat ID' in name:
                info['id'] = value
            elif 'Alias' in name:
                info['alias'] = value
        group2 = PyWin.find_child_item(node, [-1, -1, 1])
        items = PyWin.get_children(group2)
        for item in items:
            if len(PyWin.get_children(item)) >= 2:
                name = PyWin.get_window_text(PyWin.find_child_item(item, [0]))
                value = PyWin.find_child_item(item, [1])
                while PyWin.get_window_text(value) == '':
                    value = PyWin.find_child_item(value, [0])
                value = PyWin.get_window_text(value)
                if name == 'Alias' and value != 'Tap to add note':
                    info['alias'] = value
                elif name == 'Tags':
                    info['tags'] = value
        return info

    def get_name(self):
        control = PyWin.find_child_window(self.win, None, 'Edit')
        return PyWin.get_window_text(control)

    def get_pic(self):
        control = PyWin.find_child_window(self.win, None, 'Button')
        return PyWin.get_image(control)

    def get_id(self):
        name = PyWin.find_child_window(self.win, 'WeChat ID:', 'Text', warning=False)
        value = PyWin.find_child_item(name, [-1, 1])
        return PyWin.get_window_text(value)

    def get_group_alias(self):
        name = PyWin.find_child_window(self.win, 'Group Alias: ', 'Text', warning=False)
        value = PyWin.find_child_item(name, [-1, 1])
        return PyWin.get_window_text(value)

    def get_alias(self):
        name = PyWin.find_child_window(self.win, 'Alias', 'Text', warning=False)
        value = PyWin.find_child_item(name, [-1, 1])
        return PyWin.get_window_text(value)

    # return True if successfull
    def chat_to(self):
        button = PyWin.find_child_window(self.win, "Messages", "Button")
        if button != None:
            PyWin.click_control(button)
            return True
        logger.warning('did not find "Messages" button')
        return False

    def close(self):
        # print('close')
        self.win.type_keys('{ESC}')
