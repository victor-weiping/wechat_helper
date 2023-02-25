# -*- coding: utf-8 -*-
#
import os
from ui.wechat import WeChat
from helper.file_io import FileIo
from helper.utils import Utils
from helper.my_logging import *

class ListSavedGroups:
    def __init__(self, settings):
        self.settings = settings
        self.data_folder = None
        self.subfolder = None
        self.filename = None
        self.members = []
        self.index = 0

    def save_data(self, data):
        info = {}
        for key in data:
            if key == 'pic':
                self.index += 1
                imgfile = self.subfolder + str(self.index) + '.png'
                data['pic'].save(self.data_folder + imgfile, format='png')
                info['pic'] = imgfile
            else:
                info[key] = data[key]
        self.members.append(info)

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        self.data_folder = self.settings['data_folder']
        self.filename = self.settings['filename']

        basename = os.path.splitext(os.path.basename(self.filename))[0]
        self.subfolder = basename + '_img\\'
        os.makedirs(self.data_folder + self.subfolder, exist_ok=True)
        Utils.del_all_files(self.data_folder + self.subfolder)

        wechat = WeChat()
        wechat.list_saved_groups(self.save_data)

        filename = self.data_folder + self.filename

        data = {
            "group_name": 'Saved Groups',
            "time": Utils.get_time_now(),
            "size": len(self.members),
            "members": self.members
        }
        FileIo.put_json(data, filename)
        logger.info('%d groups saved to "%s"', len(self.members), filename)
