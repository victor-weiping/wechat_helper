# -*- coding: utf-8 -*-
#
#   written by Weiping Liu  2023-01
#
#   wechat_helper
#
# > python .\src\wechat_helper.py settings\{setting.yaml}
#
# 利用automation的方式模拟手工操作，实现预定的功能。
#
# 运行前需要先启动进入 WeChat,　启动后mouse/keyboard将用于模拟操作，不再可
# 以人工干预，否则会造成执行错误，使程序中断
#
# 程序依赖界面，如果有的界面由于版本更新改动，程序需要随着修改，
# 单个界面的测试可以执行　test.py
#
import sys, os
from helper.my_logging import *
from helper.file_io import FileIo
from ui.wechat import WeChat

from actions.list_contacts import ListContacts
from actions.list_saved_groups import ListSavedGroups
from actions.forward_msg import ForwardMsg
from actions.invite_join_group import InviteJoinGroup
from actions.find_blocked_members import FindBlockedMembers
from actions.list_group_members import ListGroupMembers
from actions.remove_group_members import RemoveGroupMembers
from actions.merge_group_members import MergeGroupMembers
from actions.dump_chat_msgs import DumpChatMsgs

def main(setting_file):
    # active actions
    action_map = {
        'list_contacts': do_list_contacts,
        'list_saved_groups': do_list_saved_groups,
        'forward_msg': do_forward_msg,
        'invite_join_group': do_invite_join_group,
        # 'find_blocked_members': do_find_blocked_members,
        'list_group_members': do_list_group_members,
        'remove_group_members': do_remove_group_members,
        'merge_group_members': do_merge_group_members,
        'dump_chat_msgs': do_dump_chat_msgs,
    }

    # 读入settings
    settings = FileIo.get_yaml(setting_file)

    # allow to include multiple actions in one setting
    for action in settings['actions']:
        if action['action'] in action_map:
            action_map[action['action']](action)
        else:
            logger.warning('unknown action "%s"', action)

def do_list_contacts(settings):
    ListContacts(settings).run()

def do_list_saved_groups(settings):
    ListSavedGroups(settings).run()

def do_forward_msg(settings):
    ForwardMsg(settings).run()

def do_invite_join_group(settings):
    InviteJoinGroup(settings).run()

def do_find_blocked_members(settings):
    FindBlockedMembers(settings).run()

def do_list_group_members(settings):
    ListGroupMembers(settings).run()

def do_remove_group_members(settings):
    RemoveGroupMembers(settings).run()

def do_merge_group_members(settings):
    MergeGroupMembers(settings).run()

def do_dump_chat_msgs(settings):
    DumpChatMsgs(settings).run()
    
#####################################################################
if __name__ == '__main__':
    # Usage: program {settings}
    if len(sys.argv) < 2:
        logger.warning('miss setting file')
        exit(-1)
    else:
        setting_file = os.path.abspath(sys.argv[1])
        logger = getMyLogger(__name__, setting_file)
        if os.path.exists(setting_file):
            main(setting_file)
