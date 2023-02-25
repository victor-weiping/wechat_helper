# -*- coding: utf-8 -*-
#
import time, sys
import pprint
from win.pywin import PyWin as pywin
from ui.wechat import WeChat
from ui.chats import Chats
from ui.contacts import Contacts
from ui.settings import Settings
from ui.manage_contacts import ManageContacts
from ui.person_info import PersonInfo
from ui.chatting import Chatting
from ui.dlg_forward_to import DlgForwardTo
from ui.dlg_add_member import DlgAddMember

# UI 功能测试：
#   1 启动执行本程序，选择要测试的功能序号
#   2 手动进入要测试的屏幕
#   3 追踪查看测试过程并检查结果

wechat = WeChat()
win = None

def test_WeChat(title):
    print("Show selection of menu items: Chats, Contacts, More")
    wechat.ime_english()
    # print('id.txt ...')
    # wechat.wechat.print_control_identifiers(filename='id.txt')
    for i in range(2):
        wechat.click_chats()
        time.sleep(1)
    #     wechat.click_contacts()
    #     time.sleep(1)
    #     wechat.click_more()
    #     time.sleep(1)

def test_Chats(title):
    print('id.txt ...')
    wechat.wechat.print_control_identifiers(filename='id.txt')
    print(title)
    chats = Chats(wechat.wechat)

    if True:
        field = chats.get_search_edit()
        field.draw_outline()
        field = chats.get_contacts_list()
        field.draw_outline()
        field = chats.get_chat_info_button()
        field.draw_outline()
        field = chats.get_chatting_title()
        print("title: '" + field + "'")
        field = chats.get_msg_list()
        field.draw_outline()
        field = chats.get_input_edit()
        field.draw_outline()
        field = chats.get_send_button()
        field.draw_outline()

        # show up only in search
        input('input in search edit, enter to continue...')
        chats.get_clear_button().draw_outline()
        chats.get_results_list().draw_outline()

    chats.chat_to_self()

def test_Contacts(title):
    print("Highlight 'Manage Contacts'")
    while win == None:
        print("waiting for ", title)
        win = pywin.find_child_window(wechat.wechat, 'Contacts', 'List')
        time.sleep(1)
    print('id.txt ...')
    win.print_control_identifiers(filename='id.txt')
    print(title)
    contacts = Contacts(wechat.wechat)
    for i in range(2):
        contacts.get_manage_contacts().draw_outline()
        time.sleep(1)
        # time.sleep(1)

def test_Settings(title):
    print("Find and show version number")
    while win == None:
        print("waiting for ", title)
        win = pywin.find_top_window("Settings", False)
        time.sleep(1)
    win.print_control_identifiers(filename='id.txt')
    settings = Settings(win)
    v = settings.get_version()
    settings.close()
    print(v)

def test_ManageContacts(title):
    print("Show name of the first contact")
    while win == None:
        print("waiting for ", title)
        win = pywin.find_top_window("Manage Contacts", False)
        time.sleep(1)
    # print('id.txt ...')
    # win.print_control_identifiers(filename='id.txt')
    print(title)
    manage_contacts = ManageContacts(win)
    list = manage_contacts.find_contact_list()
    item = manage_contacts.set_focus_top_item(list)
    name = manage_contacts.get_item_text(item)
    print(name)
    # manage_contacts.close()

def test_Chatting(title):
    win = None
    while win == None:
        print("waiting for ", title)
        win = pywin.get_friend_dialog_window()
        time.sleep(1)
    # print('id.txt ...')
    # win.print_control_identifiers(filename='id.txt')
    print(title)
    while win:
        win.set_focus()
        chatting = Chatting(win)
        print(chatting.get_friend_name())
        print(chatting.get_members())
        chatting.close()
        win = pywin.get_friend_dialog_window()

def test_PersonInfo(title):
    win = None
    while win == None:
        print("waiting for ", title)
        win = pywin.find_child_window(wechat.wechat, 'WeChat', 'Pane')
        time.sleep(1)
    print('id.txt ...')
    win.print_control_identifiers(filename='id.txt')
    print(title)
    person_info = PersonInfo(win)
    pprint.pprint(person_info.get_person_info())
    print('--------')
    print('name:', person_info.get_name())
    print('id:', person_info.get_id())
    print('alias:', person_info.get_alias())
    print('group alias:', person_info.get_group_alias())
    person_info.get_pic().show()

def test_CaptureWeChat(title):
    print("waiting for ", title)
    print("Get ready in 3 seconds")
    time.sleep(3)
    print('id.txt ...')
    wechat.wechat.print_control_identifiers(filename='id.txt')
    print(title)

def test_SelectMsgs(title):
    chats = Chats(wechat.wechat)
    print(chats.select_last_section_msgs())

def test_ForwardTo(title):
    print("Forward To")
    win = None
    while win == None:
        print("waiting for ", title)
        win = pywin.find_child_window(wechat.wechat, 'WeChat', 'Window')
        time.sleep(1)
    print('id.txt ...')
    win.print_control_identifiers(filename='id.txt')
    print(title)
    dlg_forward_to = DlgForwardTo(win)
    dlg_forward_to.get_search_edit().draw_outline()
    dlg_forward_to.get_new_chat().draw_outline()
    dlg_forward_to.get_multiple().draw_outline()
    dlg_forward_to.get_contacts_list().draw_outline()
    dlg_forward_to.get_selected_contacts().draw_outline()

def test_AddMember(title):
    win = None
    while win == None:
        print("waiting for ", title)
        win = pywin.find_child_window(wechat.wechat, 'AddMemberWnd', 'Window')
        time.sleep(1)
    print('id.txt ...')
    # win.print_control_identifiers(filename='id.txt')
    print(title)
    dlg_add_member = DlgAddMember(win)
    dlg_add_member.get_search_edit().draw_outline()
    dlg_add_member.get_contacts_list().draw_outline()
    dlg_add_member.get_selected_contacts().draw_outline()
    dlg_add_member.get_ok_button().draw_outline()
    dlg_add_member.get_cancel_button().draw_outline()

map = [
    {"title": "WeChat", "code": test_WeChat},           # 主屏幕
    {"title": "Chats", "code": test_Chats},
    {"title": "Contacts", "code": test_Contacts},
    {"title": "Settings", "code": test_Settings},        # 系统设置
    {"title": "Manage Contacts", "code": test_ManageContacts},  # 朋友名单列表
    {"title": "Person Info", "code": test_PersonInfo},
    {"title": "Chatting", "code": test_Chatting},         # 独立对话框:
    {"title": "Capture WeChat", "code": test_CaptureWeChat},
    {"title": "Select last section of msgs", "code": test_SelectMsgs},
    {"title": "Dialog Forward To", "code": test_ForwardTo},
    {"title": "Dialog Add Member", "code": test_AddMember},
    ]

def main(cmd):
    for i in range(len(map)):
        print(i+1, map[i]["title"])
    if cmd:
        i = int(cmd)
    else:
        i = input()

    map[int(i)-1]["code"](map[int(i)-1]["title"])
    return

if __name__ == '__main__':
    # select ether from cmd line or printed menu
    cmd = None
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
    main(cmd)
