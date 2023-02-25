# -*- coding: utf-8 -*-
#
from win.pywin import PyWin
from ui.share import Share
from ui.dlg_wechat_alert import DlgWeChatAlert
from helper.utils import Utils
from helper.my_logging import *

class DlgAddMember:
    def __init__(self, dlg):
        self.dlg = dlg
        self.checked_1_img = Utils.load_pic('.\\src\\ui\\img\\checked-1.png')
        self.unchecked_0_img = Utils.load_pic('.\\src\\ui\\img\\unchecked-0.png')
        self.unchecked_1_img = Utils.load_pic('.\\src\\ui\\img\\unchecked-1.png')

    def get_search_edit(self):
        return PyWin.find_child_window(self.dlg, 'Search', 'Edit')

    def get_contacts_list(self):
        return PyWin.find_child_window(self.dlg, 'Select contacts to add', 'List')

    def get_selected_contacts(self):
        return PyWin.find_child_window(self.dlg, '', 'List')

    def get_ok_button(self):
        return PyWin.find_child_window(self.dlg, 'Done', 'Button')

    def get_cancel_button(self):
        return PyWin.find_child_window(self.dlg, 'Cancel', 'Button')

    def get_item_pic(self, item):
        node = PyWin.find_child_item(item, [0, 1])
        return PyWin.get_image(node)

    def get_checkbox_img(self, item):
        node = PyWin.find_child_item(item, [0, 0, 0])
        return PyWin.get_image(node)

    def get_number_selected(self):
        list = self.get_selected_contacts()
        return len(PyWin.get_children(list))

    def add_members(self, members):
        search = self.get_search_edit()
        list = self.get_contacts_list()

        for member in members:
            text = ''
            if ('id' in member) and (not member['id'].startswith('wxid_')):
                text = member['id']
            elif 'name' in member:
                text = member['name']

            # 输入查找的名字
            PyWin.type_keys(search, '^A{BACKSPACE}')
            PyWin.type_keys(search, PyWin.parse_keys(text))

            candidates = Share.get_candidates(list, member, type=None)

            if len(candidates) == 0:
                logger.warning('did not find member %s', member['name'])
                continue
            if len(candidates) > 1 and 'pic' in member:
                candidates = Share.select_by_pic(list, candidates, member, self.get_item_pic)
            if len(candidates) == 1:
                imgs = {
                    'unchecked_0_img': self.unchecked_0_img,
                    'unchecked_1_img': self.unchecked_1_img,
                    'checked_1_img': self.checked_1_img,
                    'get_checkbox_img': self.get_checkbox_img,
                }
                Share.verify_checked(list, candidates[0], imgs)

        n = self.get_number_selected()
        logger.info('invited %d members', n)
        if n > 0:
            self.click_ok()
        else:
            self.click_cancel()
        self.handle_alert()
        return n

    def click_ok(self):
        button = self.get_ok_button()
        PyWin.click_control(button)

    def click_cancel(self):
        button = self.get_cancel_button()
        PyWin.click_control(button)

    def handle_alert(self):
        # check if there is popup alert popup window
        win = PyWin.find_child_window(self.dlg, 'WeChat', 'Window')
        if win == None:
            return

        alert = DlgWeChatAlert(win)
        msg = PyWin.get_window_text(alert.get_message())
        if 'Invite now?' in msg:
            alert.click_ok()
        else:
            logger.warning('alert: "' + msg + '"')
            alert.click_cancel()
