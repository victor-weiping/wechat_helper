# -*- coding: utf-8 -*-
#
from win.pywin import PyWin
from ui.share import Share
from helper.utils import Utils
from helper.my_logging import *

class DlgForwardTo:
    def __init__(self, dlg):
        self.dlg = dlg
        self.checked_1_img = Utils.load_pic('.\\src\\ui\\img\\checked-1.png')
        self.unchecked_0_img = Utils.load_pic('.\\src\\ui\\img\\unchecked-0.png')
        self.unchecked_1_img = Utils.load_pic('.\\src\\ui\\img\\unchecked-1.png')


    def get_search_edit(self):
        return PyWin.find_child_window(self.dlg, 'Search', 'Edit')

    def get_multiple(self):
        return PyWin.find_child_window(self.dlg, 'Multiple', 'Button')

    def get_new_chat(self):
        return PyWin.find_child_window(self.dlg, 'New Chat', 'Button')

    def get_contacts_list(self):
        # 输入检索内容后
        list = PyWin.find_child_window(self.dlg, 'Select contacts to add', 'List')
        if list == None:
            # 初始态
            list = PyWin.find_child_window(self.dlg, '', 'List')
        return list

    def get_number_selected(self):
        list = PyWin.find_child_window(self.dlg, 'Selected Contacts', 'List')
        return len(PyWin.get_children(list))

    def get_cancel_button(self):
        # there are 2 'cancel' buttons, one at left, one at right side, pick right one
        button = PyWin.find_child_window(self.dlg, 'Cancel', 'Button')
        if button.rectangle().left < (self.dlg.rectangle().right + self.dlg.rectangle().left)/2:
            button = PyWin.find_child_window(self.dlg, 'Cancel', 'Button', 1)
        return button

    def get_send_button(self):
        # 'send-to' and 'ccancel' have the same parent
        button = self.get_cancel_button()
        send = PyWin.find_child_item(button, [-1, 0, 0])
        if 'Send' not in PyWin.get_window_text(send):
            print('not send button')
        return send

    # checkbox circle pic
    def get_checkbox_img(self, item):
        checkbt = PyWin.find_child_item(item, [0, 0])
        return PyWin.get_image(checkbt)

    # photo pic
    def get_item_pic(self, item):
        button = PyWin.find_child_item(item, [0, 1])
        return PyWin.get_image(button)

    # return number of sent members
    def send_to_members(self, members, type):
        # forward to multiple contacts
        PyWin.click_control(self.get_multiple())

        for member in members:
            self.select_member(member, type)

        n = self.get_number_selected()
        # print('ready to send contacts:', n)
        # input('read to send. wait...' + str(n))
        if n > 0:
            self.click_send()
        else:
            self.click_cancel()
        return n    # number of sent

    def select_member(self, member, type):
        search_edit = self.get_search_edit()
        text = ''
        # search by 'id'
        if ('id' in member) and (not member['id'].startswith('wxid_')):
            text = member['id']
        # search by 'name'
        elif 'name' in member:
            text = member['name']
        keys = PyWin.parse_keys(text)
        # print('keys: "'+keys+'"')
        if keys == "":
            logger.warning('unsupported name/id: "%s"', text)
            return False

        PyWin.click_control(search_edit)
        PyWin.type_keys(search_edit, '^A{BACKSPACE}')
        PyWin.type_keys(search_edit, keys)

        list = self.get_contacts_list()
        if list == None:
            logger.warning('did not find member: %s', text)
            return False

        candidates = Share.get_candidates(list, member, type)
        if len(candidates) == 0:
            logger.warning('did not find member: "%s"', member['name'])
            return False
        if len(candidates) > 1:
            candidates = Share.select_by_pic(list, candidates, member, self.get_item_pic)
        if len(candidates) == 1:
            imgs = {
                'unchecked_0_img': self.unchecked_0_img,
                'unchecked_1_img': self.unchecked_1_img,
                'checked_1_img': self.checked_1_img,
                'get_checkbox_img': self.get_checkbox_img,
            }
            Share.verify_checked(list, candidates[0], imgs)
            return True

        logger.warning('did not find member: "%s"', member['id'])
        return False

    def click_send(self):
        # input('read to send !!')
        button = self.get_send_button()
        PyWin.click_control(button)

    def click_cancel(self):
        button = self.get_cancel_button()
        PyWin.click_control(button)
