# -*- coding: utf-8 -*-
#
import time, os
from helper.my_logging import *
from ui.wechat import WeChat
from helper.utils import Utils
from helper.file_io import FileIo

class FindBlockedMembers:
    def __init__(self, settings):
        self.settings = settings
        self.blocked = []

    def callback(self, member):
        self.blocked.append(member)

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        folder = self.settings['folder']

        filename = folder + self.settings['members']
        data = FileIo.get_json(filename)

        wechat = WeChat()
        args = {
            'folder': folder,           # 头像图片文件所在的目录
            'members': data['members'], # 转发朋友名单
            'type': 'Contacts',          # member 类别
            'index': 0
        }
        wechat.find_blocked_members(args, self.callback)

        # save blocked member listing
        filename = self.settings['folder'] + self.settings['blocked']

        data = {
            "group_name": 'Blocked',
            "time": Utils.get_time_now(),
            "size": len(self.blocked),
            "members": self.blocked
        }
        FileIo.put_json(data, filename)
        logger.info('%d blocked saved to "%s"', len(self.blocked), filename)
