# -*- coding: utf-8 -*-
#
import os, json, yaml

class FileIo:
    def get_yaml(filename):
        if os.path.exists(filename) == False:
            return None
        with open(filename, 'r', encoding='utf8') as file:
            obj = yaml.safe_load(file)
            return obj

    def get_json(filename):
        if os.path.exists(filename) == False:
            return None
        # logger.info('read json from "%s"', filename)
        with open(filename, 'r', encoding='utf8') as file:
            obj = json.load(file)
            return obj

    def put_json(obj, filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, 'w', encoding='utf8') as file:
            json.dump(obj, file, indent=2, ensure_ascii=False)

    def put_text(strs, filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, 'w', encoding='utf8') as file:
            for line in strs:
                file.write(line + '\n')
