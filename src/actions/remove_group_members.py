# -*- coding: utf-8 -*-
#
from helper.my_logging import *
from helper.utils import Utils
from helper.file_io import FileIo
from ui.wechat import WeChat

class RemoveGroupMembers:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        filename = self.settings['folder']+self.settings['filename']
        logger.info('read %s', filename)
        data = FileIo.get_json(filename)

        args = {
            'group': {'name': self.settings['group']},
            'members': data['members']
            }

        wechat = WeChat()
        wechat.remove_group_members(args)
