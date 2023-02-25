# -*- coding: utf-8 -*-
#
import time
from helper.my_logging import *
from helper.utils import Utils
from helper.file_io import FileIo

'''
    群成员合并
'''
class MergeGroupMembers:
    def __init__(self, settings):
        self.settings = settings
        self.members = []

    def run(self):
        logger.info('settings: %s', Utils.format_json(self.settings))

        folder = self.settings['folder']
        save_to = self.settings['save_to']

        include = self.settings['include_groups']
        count_include = 0
        for name in include:
            logger.info('include:'+name)
            data = FileIo.get_json(folder+name)
            n = self.insert_members(data['members'])
            count_include += n
            logger.info('%d/%d members', n, len(data['members']))

        exclude = self.settings['exclude_groups']
        count_exclude = 0
        for name in exclude:
            logger.info('exclude:'+name)
            data = FileIo.get_json(folder+name)
            n = self.remove_members(data['members'])
            count_exclude += n
            logger.info('%d/%d members', n, len(data['members']))

        data = {
           "group_name": save_to,
           "time": Utils.get_time_now(),
           "size": len(self.members),
           "include": include,
           "exclude": exclude,
           "members": self.members
        }
        FileIo.put_json(data, folder+save_to)
        logger.info('merged %d membres', len(self.members))

    def exist_member(self, member):
        if 'id' not in member:
            return None
        for m in self.members:
            if m['name'] == member['name'] and m['id'] == member['id']:
                return m
        return None

    def insert_members(self, members):
        if len(self.members) == 0:
            self.members = members.copy()
            return len(members)

        count =0
        for m in members:
            if not self.exist_member(m):
                self.members.append(m)
                count += 1
        return count

    def remove_members(self, members):
        new_members = members.copy()
        count = 0
        for m in members:
            element = self.exist_member(m)
            if element != None:
                self.members.remove(element)
                count += 1
        return count
