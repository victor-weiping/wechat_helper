# -*- coding: utf-8 -*-
#
import os
from ui.wechat import WeChat
from helper.file_io import FileIo
from helper.utils import Utils
from helper.my_logging import *

class DumpChatMsgs:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        folder = self.settings['folder']
        args = {
            "folder": folder
            }

        wechat = WeChat()
        wechat.dump_chat_msgs(args)

        filename = folder + args['name']+'.json'
        FileIo.put_json(args['msgs'], filename)
        logger.info('msgs saved to "%s"', filename)
