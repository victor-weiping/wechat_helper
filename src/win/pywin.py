# -*- coding: utf-8 -*-
#
#   interface functions to pyautowin
#
import pywinauto
from helper.my_logging import *

class PyWin:
    def connect_wechat(class_name='WeChatMainWndForPC'):
        logger.info('connecting to "WeChat"')
        try:
            app = pywinauto.application.Application(backend='uia').connect(class_name=class_name)
        except:
            logger.error('connecting to WeChat failed')
            return None
        return app['WeChat']

    def find_child_window(parent, title, type, index=0, warning=True):
        for i in range(3):
            win = parent.child_window(title=title, control_type=type, found_index=index)
            if win.exists():
                return win
            # 如果是新的Window, 可能需要等一点时间，其他类别不需要延时等
            if not (type == 'Window' or type == 'Pane'):
                break
        if warning:
            logger.warning('did not find "%s"[%s]', title, type)
        return None

    def find_child_item(parent, levels):
        pane = parent
        if pane == None:
            return None
        for i in levels:
            if i == -1:
                pane = pane.parent()
                continue
            children = pane.children()
            if len(children) <= i:
                return None
            pane = children[i]
        return pane

    def get_desktop():
        return pywinauto.Desktop(backend="uia")

    def get_language(win):
        # child_window(title="Language bar", control_type="ToolBar")
        #     | child_window(title="English (United States)", control_type="MenuItem")
        desktop = pywinauto.Desktop(backend="uia")
        for i in range(5):
            # set focus to the window, input method may change accordingly
            win.set_focus()
            pane = desktop.window(class_name='Shell_TrayWnd')
            # pane = desktop.window(title='', control_type='Pane', found_index=i)
            # Windows-7
            language = pane.window(title='Language bar', control_type='ToolBar')
            if language == None:
                # Windows-10
                language = pane.window(title='Tray Input Indicator', control_type='Pane')
            if language.exists():
                # language.print_control_identifiers(filename='language.txt')
                items = language.children()
                for item in items:
                    print(item.window_text())
                    if 'English' in item.window_text():
                        return 'English'
                return 'Other'
        return None

    def get_chatting_window(index=0):
        desktop = pywinauto.Desktop(backend="uia")
        win = desktop.window(class_name='ChatWnd', control_type='Window', found_index=index)
        if win.exists():
            return win;
        return None

    def find_top_window(win_name, warning=True):
        win = pywinauto.Desktop(backend='uia')[win_name]
        if win.exists():
            return win
        if warning:
            logger.warning('failed to open "%s"', win_name)
        return None

    def get_window_text(item):
        if item:
            return item.window_text()
        return item

    def get_children(element, ctype=None):
        return element.children(control_type=ctype)

    def get_image(item):
        return item.capture_as_image()

    def get_rect(item):
        return item.rectangle()

    def draw_outline(item):
        item.draw_outline()

    # optionally highlight the window rect
    def click_control(control, pos='center', button='left'):
        if control == None:
            return
        control.draw_outline()
        coords = control.rectangle()
        if pos == 'center':
            x = int((coords.right - coords.left) / 2)
            y = int((coords.bottom - coords.top) / 2)
        elif pos == 'top-left':
            x = 5
            y = 5
        else:
            x = (coords.right - coords.left) - 5
            y = (coords.bottom - coords.top) - 5
        pywinauto.mouse.click(button=button, coords=(coords.left+x, coords.top+y))

    def click_control_at(control, x, y, button='left'):
        control.draw_outline()
        coords = control.rectangle()
        pywinauto.mouse.click(button=button, coords=(coords.left+x, coords.top+y))

    def parse_keys(keys):
        # print('"'+keys+'"')
        # pywinauto has bug to enter unicode greater than FFFF
        text = ''
        for k in range(len(keys)):
            # print(ord(keys[k]))
            if keys[k] in '(){}+':
                text += '{'+keys[k]+'}'
            elif ord(keys[k]) < 65536:
                text += keys[k]
            elif len(keys)-k > k:
                text = ''
            else:
                break
        # logger.info('keys"'+text+'"')
        return text

    def type_keys(control, keys):
        control.type_keys(keys, with_spaces=True)

    def send_keys(keys):
        pywinauto.keyboard.send_keys(keys)

    def mouse_move(control):
        coords = control.rectangle()
        x = int((coords.right - coords.left) / 2)
        y = int((coords.bottom - coords.top) / 2)
        pywinauto.mouse.move(coords=(coords.left+x, coords.top+y))

    def mouse_scroll(control, dist):
        coords = control.rectangle()
        x = int((coords.right - coords.left) / 2)
        y = int((coords.bottom - coords.top) / 2)
        pywinauto.mouse.scroll(coords=(coords.left+x, coords.top+y), wheel_dist=dist)
