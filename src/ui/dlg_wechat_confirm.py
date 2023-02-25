# -*- coding: utf-8 -*-
#
from win.pywin import PyWin
from helper.my_logging import *

# 从群组移出某人，在点击 Delete 之后会有一个 Confirmation popup window
class DlgWeChatConfirm:
    def __init__(self, dlg):
        self.dlg = dlg

    def confirm_delete(self):
        text = 'Confirm deletion'
        item = PyWin.find_child_item(self.dlg, [1,0,1,1])
        title = item.window_text()
        logger.info(title)
        if title.startswith(text):
            delete = PyWin.find_child_window(self.dlg, 'Delete', 'Button')
            PyWin.click_control(delete)
            return True
        else:
            logger.warning('not expected "%s" window', text)
            cancel = PyWin.find_child_window(self.dlg, 'Cancel', 'Button')
            PyWin.click_control(cancel)
            return False
