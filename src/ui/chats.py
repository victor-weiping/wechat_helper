# -*- coding: utf-8 -*-
#
import time
from helper.utils import Utils
from win.pywin import PyWin
from ui.share import Share
from ui.person_info import PersonInfo
from ui.dlg_forward_to import DlgForwardTo
from ui.chat_info import ChatInfo
from ui.chatting import Chatting
from helper.file_io import FileIo
from helper.my_logging import *

class Chats:
    def __init__(self, wechat):
        self.win = wechat

    def get_search_edit(self):
        search = PyWin.find_child_window(self.win, 'Search', 'Edit')
        return search

    def get_clear_button(self):
        clear = PyWin.find_child_window(self.win, 'Clear', 'Button')
        return clear

    def get_contacts_list(self):
        list = PyWin.find_child_window(self.win, '会话', 'List')
        return list

    def get_results_list(self):
        list = PyWin.find_child_window(self.win, 'Search Results', 'List')
        return list

    def get_chat_info_button(self):
        button = PyWin.find_child_window(self.win, 'Chat Info', 'Button')
        return button

    def get_chat_info_window(self):
        for i in range(3):
            win = PyWin.find_child_window(self.win, 'Chat Info', 'Window')
            if win != None:
                return win
            # 当WeChat窗口靠右边，Chat Info移入内部，使用不同的名称
            win = PyWin.find_child_window(self.win, 'SessionChatRoomDetailWnd', 'Window')
            if win != None:
                return win
        logger.warning('failed open "Chat Info" window')
        return None

    def get_chatting_title(self):
        # the same parent with 'Chat Info' button
        button = self.get_chat_info_button()
        title = PyWin.find_child_item(button, [-1, -1, -1, 1, 0, 0, 0, 0])
        return PyWin.get_window_text(title)

    def get_msg_list(self):
        list = PyWin.find_child_window(self.win, '消息', 'List')
        return list

    def get_input_edit(self):
        edit = PyWin.find_child_window(self.win, 'Enter', 'Edit')
        return edit

    def get_send_button(self):
        edit = PyWin.find_child_window(self.win, 'sendBtn', 'Button')
        return edit

    # group/contact photo
    def get_item_pic(self, item):
        return PyWin.find_child_item(item, [0, 0])

    # return True if successfull
    def chat_to_self(self):
        # find user icon
        chats = PyWin.find_child_window(self.win, 'Chats', 'Button')
        user = PyWin.find_child_item(chats, [-1, 0])

        # click the user icon, popup user info window
        PyWin.click_control(user)
        pane = PyWin.find_child_window(self.win, 'WeChat', 'Pane')
        if pane == None:
            logger.warning('did not find "WeChat" pane')
            return False
        # pane.print_control_identifiers(filename='pane.txt')
        person_info = PersonInfo(pane)
        return person_info.chat_to()

    # return True if successfull
    def chat_to(self, member, type):
        if member == None:
            return self.chat_to_self()

        search = self.get_search_edit()
        PyWin.click_control(search)

        text = ''
        # search by 'id'
        if ('id' in member) and (not member['id'].startswith('wxid_')):
            text = member['id']
        # search by 'name'
        elif 'name' in member:
            text = member['name']

        PyWin.type_keys(search, '^A{BACKSPACE}')
        PyWin.type_keys(search, PyWin.parse_keys(text))

        # 更新结果需要花点时间
        time.sleep(1)
        list = self.get_results_list()
        candidates = Share.get_candidates(list, member, type)
        if len(candidates) == 0:
            logger.warning('did not find member: "%s"', member['name'])
            return False
        if len(candidates) > 1 and 'pic' in member:
            candidates = Share.select_by_pic(list, candidates, member, self.get_item_pic)
        if len(candidates) == 1:
            logger.info('chat to "%s"', member['name'])
            self.click_item(list, candidates[0])
            return True
        return False

    def click_item(self, list, item):
        Share.scroll_item_in(list, item)
        PyWin.click_control(item)

    # 返回 n= 转发的members数量
    # args = {
    #     'user': None,               # 从哪个用户转发:本人
    #     'folder': self.settings['data_folder'],           # 头像图片文件所在的目录
    #     'members': data['members'], # 转发朋友名单
    #     'exclude': exclude,         # 不包括所列的tags
    #     'type': self.settings['type'],  # member 类别
    # }
    def forward_msg(self, args):
        max_items = 9   # max number of contacts in a group for sending
        index = 0
        excludes = 0
        members = []
        while index < len(args['members']):
            member = args['members'][index]
            index += 1
            if self.exclude_tag(member, args['exclude']):
                excludes += 1
                continue
            if 'pic' in member:
                member['pic'] = Utils.load_pic(args['folder']+member['pic'])
            members.append(member)

            # forward a group of members
            if len(members) == max_items:
                self.do_forward_msg(args['user'], members, args['type'])
                members = []

        if len(members) > 0:
            self.do_forward_msg(args['user'], members, args['type'])
        logger.info('processed %d, excluded %d', index, excludes)

    def exclude_tag(self, member, exclude):
        if not 'tags' in member:
            return False
        tags = member['tags']
        # print(member['id'], tags)
        for e in exclude:
            if e in tags:
                logger.warning('exclude: %s [%s]', member['id'], e)
                return True
        return False

    def do_forward_msg(self, from_user, members, type):
        # switch to account where forward msg from
        self.chat_to_self()

        # select last section of msgs
        if self.select_last_section_msgs() <= 0:
            logger.warning('no selection, failed to forward')
            return 0

        # press forward, get popup window to select member and send
        PyWin.click_control(self.find_forward_control())
        for i in range(3):
            time.sleep(0.2)
            dlg = PyWin.find_child_window(self.win, 'WeChat', 'Window')
            if dlg:
                break
        if dlg == None:
            logger.warning('forward popup window does not show up')
            return 0
        dlg_forward_to = DlgForwardTo(dlg)
        n = dlg_forward_to.send_to_members(members, type)

        # close dlg if exists
        if dlg.exists():
            logger.warning('force close dlg-send-to')
            dlg_forward_to.click_cancel()
        # if One-on-One Forward text exists, close the forward window
        node = self.find_forward_control()
        if node != None:
            close = PyWin.find_child_item(node, [-1, -1, -1, 1])
            PyWin.click_control(close)
        # logger.info('forward: %d member(s)', n)
        return n

    # return number of selected msgs
    def select_last_section_msgs(self):
        list = PyWin.find_child_window(self.win, '消息', 'List')
        if list == None:
            logger.warning('did not find message list')
            return 0
        # 从下往上选择Messages
        items = PyWin.get_children(list, 'ListItem')
        items.reverse()     # reverse in place

        # scroll to bottom
        PyWin.click_control(list, 'top-left')
        PyWin.type_keys(list, '^{HOME}^{END}')

        msgs = 0
        while msgs < len(items):
            item = items[msgs]
            # check if the item is a valid date/time string
            t = Utils.format_time_tag(item.window_text(), warning=False)
            if t != None:   # found date/time
                break
            self.select_msg_item(list, item)
            msgs += 1
        # logger.info('selected %d msgs', msgs)
        return msgs

    def scroll_msg_in(self, list, item):
        list_rect = PyWin.get_rect(list)
        item_rect = PyWin.get_rect(item)
        # while item.top is 50 pix more than list-bottom window
        while item_rect.top > list_rect.bottom - 50:
            PyWin.mouse_scroll(list, -2) # scroll content up
            # print(list_rect, item_rect)
            # print('up')
            time.sleep(0.1)    # not sure if need this delay
            item_rect = PyWin.get_rect(item)
        # scroll content down into view
        while PyWin.get_rect(item).top < list_rect.top:
            # scroll过快会漏掉选择,用最小Window,测试数值不超过2
            PyWin.mouse_scroll(list, 2) # scroll content down
            # print('down')
            time.sleep(0.1)    # not sure if need this delay

    def scroll_msg_top(self, list):
        PyWin.click_control(list, 'top-left')
        PyWin.type_keys(list, '^{HOME}')

    def find_forward_control(self):
        # forward type:
        ftype = 'One-by-One Forward'
        # ftype = 'Combine and Forward'
        forward = PyWin.find_child_window(self.win, ftype, 'Text', warning=False)
        if forward:
            return PyWin.find_child_item(forward, [-1, 0])
        return None

    def select_msg_item(self, list, item):
        self.scroll_msg_in(list, item)
        forward = self.find_forward_control()
        if forward != None:
            PyWin.click_control(item, 'top-left')
        else:
            # item [text, link, photo,]
            #   pane
            #       pane    (fill)
            #       pane    (body)
            #       button  (sender)
            body = PyWin.find_child_item(item, [0, 1])
            PyWin.click_control(body, button='right')
            select = PyWin.find_child_window(self.win, 'Select...', 'MenuItem')
            PyWin.click_control(select)
        return True

    # 换到指定的群组，打开扩展窗口
    # group = {'name':'xx'}
    def open_chat_info(self, group):
        # 切换到指定的群，确认对话的群名是正确的
        if self.chat_to(group, 'Group Chats') == False:
            return 0
        # 点击title打开右边的扩展窗口
        button = self.get_chat_info_button()
        PyWin.click_control(button)
        win = self.get_chat_info_window()
        return win

    #################################################################
    def invite_join_group(self, args):
        while True:
            members = []
            for i in range(9):
                # check if there is any popup chatting window
                dlg = PyWin.get_chatting_window()
                if dlg == None:
                    break
                dlg.set_focus()
                chatting = Chatting(dlg)
                # there is only one contact in members
                members += chatting.get_members()
                chatting.close()

            if len(members) == 0:
                break

            for m in members:
                logger.info('member: "' + m['name'] + '"[' + m['id'] + ']')

            # now we open the group and invite the contact
            self.win.set_focus()
            win = self.open_chat_info(args['group'])
            if win == None:
                return

            chat_info = ChatInfo(win)
            n = chat_info.add_members(members)
            chat_info.close()
        return

    #################################################################
    def find_blocked_members(self, args, callback):
        blocked = 0
        index = 0
        members = len(args['members'])
        percent = 10
        for index in range(members):
            if index > int(members*percent/100):
                # report processed percentage
                logger.info('processed %d%%', percent)
                percent += 10
            member = args['members'][index]
            msg = self.check_member_blocked(member, args['type'], args['folder'])
            if msg == None:
                continue
            # logger.warning('blocked: "%s" [%s]', member['name'], member['id'])
            callback(member)
            blocked += 1
        logger.info('total blocked %d', blocked)
        return blocked

    # 检查特定成员对话的最后一段消息，如果包含给定的字符串'text'=[...]，返回本条消息内容
    # 如果没有包含，返回None
    def check_member_blocked(self, member, type, folder):
        # member['pic'] needs to be loaded
        if self.chat_to(member, type) == False:
            return None

        blocked_text = [
            '开启了朋友验证',
            '消息已发出，但被对方拒收了',
            '对方帐号异常'
            ]

        # logger.info('check reject "%s" [%s]', member['name'], member['id'])
        section = self.get_msg_section()
        if len(section['msgs']) == 0:
            return None

        # 只检查最后一行内容 in section['msgs']:
        msg = section['msgs'][0]
        for t in blocked_text:
            if t in msg:
                return msg
        return None

    # 获取按照时间段划分的一组对话信息，倒数第Ｎ组
    def get_msg_section(self, n=0):
        list = PyWin.find_child_window(self.win, '消息', 'List')
        items = PyWin.get_children(list, 'ListItem')
        # 倒排序
        items.reverse()

        msgs = []
        msg_time = None
        section = 0
        for item in items:
            text = PyWin.get_window_text(item)
            # check if the item is a valid date/time string
            msg_time = Utils.format_time_tag(text, warning=False)
            if msg_time != None:   # found date/time
                if section == n:
                    break
                else:
                    msgs = []
                    msg_time = None
                    section += 1
            else:
                msgs.append(text)

        return {
            'msgs': msgs,
            'time': msg_time
        }

    #################################################################
    # args = {
    #     'group': {'name': group['name']}
    # }
    def list_group_members(self, args, callback):
        # 换到指定的群组，打开扩展窗口
        win = self.open_chat_info(args['group'])
        if win == None:
            return 0

        #
        chat_info = ChatInfo(win)
        n = chat_info.get_members(callback)
        if win.exists():
            chat_info.close()
        return n

    #################################################################
    def remove_group_members(self, args):
        # 换到指定的群组，打开扩展窗口
        win = self.open_chat_info(args['group'])
        if win == None:
            return 0

        chat_info = ChatInfo(win)

        # 分组删除
        index = 0
        group_size = 3
        while index < len(args['members']):
            members = args['members'][index:index+group_size]
            chat_info.remove_members(members)
            index += group_size
        chat_info.close()
        return

    #################################################################
    def dump_chat_msgs(self, args):
        name = self.get_chatting_title()
        if not name:
            return None

        logger.info('dump msg for "' + name + '"...')
        msgs = FileIo.get_json(args['folder'] + name + '.json')
        if msgs == None:
            msgs = []

        last_time = None
        index = self.get_last_time_index(msgs)
        if index != None:
            last_time = msgs[index]['content']
            msgs = msgs[:index]
            logger.info('last time: %s', last_time)
            print('cut at: ', msgs[len(msgs)-1])

        list = PyWin.find_child_window(self.win, '消息', 'List')

        # scroll page up until find the last time stamp, or to top
        self.scroll_list_to_time(list, last_time)

        items = PyWin.get_children(list, 'ListItem')

        for item in items:
            msg = self.parse_item(item)
            if msg == None:
                logger.warning('unkown msg: %s', str(item))
                continue
            if index != None:
                if not (msg['sender'] == 'time' and msg['content'] == last_time):
                    continue
                index = None

            print('append:', msg)
            msgs.append(msg)
        args['msgs'] = msgs
        args['name'] = name

    def get_last_time_index(self, msgs):
        if msgs == None or len(msgs) == 0:
            return None
        for i in range(len(msgs), 0, -1):
            if msgs[i-1]['sender'] == 'time':
                return i-1
        return None

    def scroll_list_to_time(self, list, last_time):
        print('last time:', last_time)
        while last_time == None:
            time.sleep(0.5)
            self.scroll_msg_top(list)
            items = PyWin.get_children(list, 'ListItem')
            if PyWin.get_window_text(items[0]) != 'View more messages':
                print('at top')
                return
            PyWin.click_control(items[0])

        tag_time = Utils.get_time_now()
        while last_time < tag_time:
            time.sleep(0.5)
            print('get list items')
            items = PyWin.get_children(list, 'ListItem')
            for item in items:
                text = PyWin.get_window_text(item)
                tag_time = Utils.format_time_tag(text, False)
                if tag_time == None:
                    continue
                if tag_time <= last_time:
                    break
                print('scroll to top...')
                self.scroll_msg_top(list)
                if PyWin.get_window_text(items[0]) == 'View more messages':
                    print('click more...')
                    PyWin.click_control(items[0])
                    break
        logger.info('got time tag: %s', tag_time)
        return

    # parse item, return msg = {} or None if error
    def parse_item(self, item):
        msg = {}
        title = PyWin.get_window_text(item)
        t = Utils.format_time_tag(title, warning=False)
        if t != None:   # found date/time
            msg = {'sender':'time', 'content':t}
            return msg

        # item 只有一个 child: pane
        panes = PyWin.get_children(item)
        if len(panes) != 1:
            logger.warning('wrong number of children: %d', len(panes))
            return None

        # pane 有左、中、右三个Children
        children = PyWin.get_children(panes[0])
        if len(children) != 3:
            logger.warning('todo .. number of children: %d', len(panes))
            return None

        types = self.get_node_type(children[0])
        types += '-'+self.get_node_type(children[1])
        types += '-'+self.get_node_type(children[2])
        # print(types)
        if types == 'Pane-Button-Pane':
            msg = {'sender':'sys-0', 'content':title}
            return msg
        elif types == 'Button-Pane-Pane':
            msg = {'sender':children[0].window_text(), 'content':title}
            return msg
        elif types == 'Pane-Pane-Button':
            msg = {'sender':children[2].window_text(), 'content':title}
            return msg
        elif types == 'Pane-Edit-Pane':
            msg = {'sender':'sys-1', 'content':title}
            return msg
        elif types == 'Pane-Pane-Pane':
            msg = {'sender':'sys-2', 'content':children[2].window_text()}
            return msg
        else:
            logger.warning('todo types: '+types)
            return None

    def get_node_type(self, node):
        words = str(node).split()
        return words[len(words)-1]
