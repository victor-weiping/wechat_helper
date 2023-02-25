# -*- coding: utf-8 -*-
#
from ui.wechat import WeChat
from helper.file_io import FileIo
from helper.utils import Utils
from helper.my_logging import *

class ForwardMsg:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        filename = self.settings['data_folder'] + self.settings['filename']
        data = FileIo.get_json(filename)

        exclude = []
        if 'exclude' in self.settings:
            exclude = self.settings['exclude']


        wechat = WeChat()
        args = {
            'user': None,               # 从哪个用户转发:本人
            'folder': self.settings['data_folder'],           # 头像图片文件所在的目录
            'members': data['members'], # 转发朋友名单
            'exclude': exclude,         # 不包括所列的tags
            'type': self.settings['type'],  # member 类别
        }
        wechat.forward_msg(args)
