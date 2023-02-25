# -*- coding: utf-8 -*-
#
from helper.my_logging import *
from win.pywin import PyWin
from ui.share import Share
from ui.dlg_add_member import DlgAddMember
from ui.dlg_delete_member import DlgDeleteMember
from ui.person_info import PersonInfo

class ChatInfo:
    def __init__(self, win):
        self.win = win

    # return number of invied members
    def add_members(self, args):
        # 打开添加朋友('+')对话窗口
        self.click_add()
        win = PyWin.find_child_window(self.win, 'AddMemberWnd', 'Window')
        dlg_add_member = DlgAddMember(win)

        # 邀请加入一定数量的朋友
        n = dlg_add_member.add_members(args)
        return n

    def click_add(self):
        list = PyWin.find_child_window(self.win, 'Members', 'List')
        items = PyWin.get_children(list, 'ListItem')
        for item in items:
            if item.window_text() == 'Add':
                PyWin.click_control(item)
                return
        logger.warning('did not find "Add" member button')
        return

    def close(self):
        # PyWin.type_keys(self.win, '{ESC}')
        PyWin.send_keys('{ESC}')

    def view_more(self):
        # in case of less member, there is no 'View More Members'
        button = 'Show All' # version 3.6.0.18
        view_more = PyWin.find_child_window(self.win, button, 'Button', warning=False)
        if view_more == None:
            button = 'View More Members'  # version 3.5.0.46
            view_more = PyWin.find_child_window(self.win, button, 'Button', warning=False)

        if view_more != None:
            PyWin.click_control(view_more)

    def get_members(self, callback):
        self.view_more()

        list = PyWin.find_child_window(self.win, 'Members', 'List')
        scroll_list = PyWin.find_child_item(list, [-1])
        items = PyWin.get_children(list, 'ListItem')
        logger.info('%d members in the list', len(items))

        for item in items:
            Share.scroll_item_in(scroll_list, item)
            item.draw_outline()
            # time.sleep(0.5)
            name = PyWin.get_window_text(item)
            if name == 'Add' or name == 'Delete' or name == 'Remove':
                continue

            # open info card window
            PyWin.click_control(item)
            pane = PyWin.find_child_window(self.win, 'WeChat', 'Pane')
            if pane == None:
                logger.warning('failed to open personal info for "%s"', name)
                return 0

            person_info = PersonInfo(pane)
            callback(person_info.get_person_info())
            person_info.close()
        return

    def remove_members(self, members):
        list = PyWin.find_child_window(self.win, 'Members', 'List')
        items = PyWin.get_children(list, 'ListItem')

        # 从 member 中找出 [-]Delete
        for item in items:
            name = item.window_text()
            if name == 'Delete' or name == 'Remove':
                break
        if not (name == 'Remove' or name == 'Delete'):
            logger.warning('did not find <Remove> button. items=%d', len(items))
            input('stop check...')
            return 0

        PyWin.click_control(item)
        dlg = PyWin.find_child_window(self.win, 'DeleteMemberWnd', 'Window')
        if dlg == None:
            logger.warning('did not see "Delete Member Window"')
            return 0
        dlg_delete = DlgDeleteMember(dlg)
        deleted = dlg_delete.delete_member(members)
        return deleted
