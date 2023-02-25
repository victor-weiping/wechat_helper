# -*- coding: utf-8 -*-
#
import os
from ui.wechat import WeChat
from helper.file_io import FileIo
from helper.utils import Utils
from helper.my_logging import *

class ListContacts:
    def __init__(self, settings):
        self.settings = settings
        self.folder = None
        self.subfolder = None
        self.filename = None
        self.members = []

    def save_contact(self, data):
        info = {}
        # 未知因素会有聊天群混到朋友名单里来，需要剔除
        if ('id' in data) and (data['id'].endswith('@chatroom')):
            logger.warning('ignored wrong member "%s"', data['name'])
            return

        # 图片需要存成文件，保留文件名，其他项目不变
        for key in data:
            if key == 'pic':
                imgfile = self.subfolder + data['id'] + '.png'
                Utils.save_pic_png(data['pic'], self.folder + imgfile)
                info['pic'] = imgfile
            else:
                info[key] = data[key]
        logger.info('name: "%s"', info['name'])
        self.members.append(info)

    def run(self):
        logger.info('settings:\n%s', Utils.format_json(self.settings))

        self.folder = self.settings['folder']
        self.filename = self.settings['filename']

        # create folder for img files
        basename = os.path.splitext(os.path.basename(self.filename))[0]
        self.subfolder = basename + '_img\\'
        logger.info('check folder: "%s"', self.folder + self.subfolder)
        os.makedirs(self.folder + self.subfolder, exist_ok=True)
        Utils.del_all_files(self.folder + self.subfolder)

        # connect to wechat and get list of contacts, using callback to save data
        wechat = WeChat()
        wechat.list_contacts(self.save_contact)

        # output contacts
        data = {
            "group_name": 'Contacts',
            "time": Utils.get_time_now(),
            "size": len(self.members),
            "members": self.members
        }
        filename = self.folder + self.filename
        FileIo.put_json(data, filename)
        logger.info('%d contacts saved to "%s"', len(self.members), filename)
