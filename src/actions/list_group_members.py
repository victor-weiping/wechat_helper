# -*- coding: utf-8 -*-
#
import time, os
from helper.my_logging import *
from helper.utils import Utils
from helper.file_io import FileIo
from ui.wechat import WeChat

class ListGroupMembers:
    def __init__(self, settings):
        self.settings = settings
        self.folder = None
        self.subfolder = None
        self.members = []

    def save_data(self, data):
        info = {}
        # 图片文件名用在群里的序号 001-500
        img_name = str(len(self.members)+1).zfill(3)
        for key in data:
            if key == 'pic':
                imgfile = self.subfolder + img_name + '.png'
                data['pic'].save(self.folder + imgfile, format='png')
                info['pic'] = imgfile
            elif (data[key] != None) and (data[key] != ''):
                info[key] = data[key]
        self.members.append(info)
        # if len(self.members) % 50 == 0:
        logger.info('member %d "%s"', len(self.members), info['name'])

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        self.folder = self.settings['folder']
        groups = self.settings['groups']
        for group in groups:
            meta_file = group['meta']
            self.members = []
            basename = os.path.splitext(os.path.basename(meta_file))[0]
            self.subfolder = basename + '_img\\'
            os.makedirs(self.folder + self.subfolder, exist_ok=True)
            Utils.del_all_files(self.folder + self.subfolder)

            wechat = WeChat()
            args = {
                'group': {'name': group['name']}
            }
            wechat.list_group_members(args, self.save_data)

            data = {
                "group_name": group['name'],
                "time": Utils.get_time_now(),
                "size": len(self.members),
                "members": self.members
            }
            filename = self.folder + meta_file
            FileIo.put_json(data, filename)
            logger.info('%d contacts saved to "%s"', len(self.members), filename)
