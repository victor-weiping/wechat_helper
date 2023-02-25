# -*- coding: utf-8 -*-
#
from ui.wechat import WeChat
from helper.utils import Utils
from helper.my_logging import *

class InviteJoinGroup:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        wechat = WeChat()
        args = {
            'group': {'name':self.settings['group']},
        }
        wechat.invite_join_group(args)
