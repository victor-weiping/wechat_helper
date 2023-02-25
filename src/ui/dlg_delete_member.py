# -*- coding: utf-8 -*-
#
import time
from win.pywin import PyWin
from helper.my_logging import *
from ui.dlg_wechat_confirm import DlgWeChatConfirm

class DlgDeleteMember:
    def __init__(self, dlg):
        self.dlg = dlg

    # return number of deleted members
    def delete_member(self, members):
        # put name in 'Search Edit' field
        edit = PyWin.find_child_window(self.dlg, 'Search', 'Edit')
        if not edit.has_keyboard_focus():
            logger.warning('failed to put focus on edit')
            return False

        for item in members:
            name = item['name']
            PyWin.click_control(edit)
            PyWin.type_keys(edit, '^a{BACKSPACE}')
            PyWin.type_keys(edit, PyWin.parse_keys(name))
            candidates = self.get_candidates(name)
            if len(candidates) != 1:
                logger.warning('%s has %d candidates', name, len(candidates))
                continue
            # select unique item
            if self.verify_checked(candidates[0]) == False:
                logger.warning('%s duplicated?')
                continue
            else:
                logger.info('selected "%s"', name)

        n = len(self.get_selected_items())
        if n > 0:
            if self.click_delete():
                logger.info('removed %d selected members', n)
        else:
            self.click_cancel()
        return n

    def click_delete(self):
        # for testing
        self.click_cancel()
        return False

        delete = self.dlg.window(title='Delete', control_type='Button')
        PyWin.click_control(delete)

        # expect confirmation popup window
        win = PyWin.find_child_window(self.dlg, 'WeChat', 'Window', warning=False)
        if win != None:
            dlg_confirm = DlgWeChatConfirm(win)
            dlg_confirm.confirm_delete()

            # 等待popup window closed，否则会引发后续操作问题
            for i in range(10):
                time.sleep(0.2)
                if not win.exists():
                    break
            return True

        return False

    def click_cancel(self):
        button = self.dlg.window(title='Cancel', control_type='Button')
        PyWin.click_control(button)
        logger.info('clicked cancel button')

    def get_selected_items(self):
        pane = self.dlg.children(control_type='Pane')[1]
        pane = pane.children(control_type='Pane')[2]
        list = pane.children(control_type='List')[0]
        items = PyWin.get_children(list, 'ListItem')
        return items

    def get_candidates(self, name):
        candidates = []
        pane = self.dlg.children(control_type='Pane')[1]
        pane = pane.children(control_type='Pane')[0]
        list = pane.children(control_type='List')[0]
        items = PyWin.get_children(list, 'ListItem')
        for item in items:
            self.scroll_item_in(list, item)
            text = PyWin.find_child_item(item, [0,1,0]).window_text()
            if text == name:
                candidates.append(item)
        # found unique candidate, scroll in view
        if len(candidates) == 1:
             self.scroll_item_in(list, candidates[0])
        return candidates

    def verify_checked(self, item):
        # check 之前的数量
        before = len(self.get_selected_items())
        # check
        PyWin.click_control(item)
        after = len(self.get_selected_items())

        if after < before:
            logger.warning('duplicated item?')
            return False
        return True

    def scroll_item_in(self, list, item):
        # scroll item in view
        top = PyWin.get_rect(list).top
        for i in range(30):     # limited loops
            itop = PyWin.get_rect(item).top
            if itop >= top:
                break
            # print('down', top, itop)
            PyWin.mouse_scroll(list, 5) # 动作太大会滑过导致反复
            time.sleep(0.5) # 过快会滑过太多

        bottom = PyWin.get_rect(list).bottom
        for i in range(30):
            ibottom = PyWin.get_rect(item).bottom
            if ibottom <= bottom:
                break
            # print('up', bottom, ibottom)
            PyWin.mouse_scroll(list, -5)
            time.sleep(0.5)
