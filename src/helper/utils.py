# -*- coding: utf-8 -*-
#
import datetime
import json, os, glob
from PIL import Image
from PIL import ImageChops
import imagehash
from helper.my_logging import *

class Utils:
    # stime time string to be converted:
    #   '6:30 PM'
    #   '1-7-22 10:28 PM'
    #   '6-20-21 6:30 PM'
    #   'Yesterday 6:30 PM'
    #   'Monday 6:30 PM'
    # output format
    #   '2021-06-20 18:30'
    def format_time_tag(stime, warning=True):
        now = datetime.datetime.now()
        t = ''
        if stime == '':
            return None

        w = stime.split()
        ws = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Yesterday']
        if w[0] in ws:
            if w[0] == ws[7]:
                days = 1
            else:
                d0 = now.weekday()
                d1 = ws.index(w[0])
                days = d0 - d1
                if days < 0:
                    days += 7
            t = now - datetime.timedelta(days=days)
            t = t.strftime('%m-%d-%y') + stime[len(w[0]):]
        elif len(stime) <= 8:
            t = now.strftime('%m-%d-%y ') + stime
        else:
            t = stime
        try:
            tt = datetime.datetime.strptime(t, '%m-%d-%y %I:%M %p')
        except ValueError:
            if warning:
                logger.warning('wrong date-time string "%s"', stime)
            return None
        return tt.strftime('%Y-%m-%d %H:%M')

    def get_time_now():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    def get_time_fname():
        return datetime.datetime.now().strftime('%Y-%m-%d_%H%M')

    def format_json(jobj):
        return json.dumps(jobj, indent=2, ensure_ascii=False)

    def del_all_files(folder):
        list = os.listdir(folder)
        logger.info('delete all files in %s', folder)
        for filename in list:
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.warning('failed to delete %s. reason: %s' % (file_path, e))

    def parse_keys(text):
        parsed = ''
        for c in text:
            if c == ' ':
                parsed += '{SPACE}'
            elif c in '(){}~+^%':
                parsed += '{' + c + '}'
            elif c == '\n':
                parsed += '^{ENTER}'
            else:
                parsed += c
        # logger.info('<%s><%s>', text, parsed)
        return parsed

    def get_img_key(img):
        key = imagehash.average_hash(img)
        return str(key)

    def save_pic_png(pic, filename):
        pic.save(filename, format='png')

    def load_pic(filename):
        if os.path.exists(filename) == False:
            logger.warning('image file does not exists "%s"', filename)
            return None
        return Image.open(filename)

    def is_same_img(img1, img2):
        diff = ImageChops.difference(img1, img2)
        if diff.getbbox():
            return False
        return True

    def crop_img(img, x, y):
        width, height = img.size
        cropped = img.crop((x, y, width, height))
        return cropped

    def compare_pics(pic1, pic2, hash_size=24):
        hash1 = imagehash.average_hash(pic1, hash_size)
        hash2 = imagehash.average_hash(pic2, hash_size)
        distance = hash1 - hash2
        return distance

    def get_listfiles(file_spec):
        return glob.glob(file_spec)

if __name__ == '__main__':
    #   '1-7-22 10:28 PM
    print(Utils.format_time_tag('1-7-22 10:28 PM'))
    # print(Utils.format_time_tag('7:40 PM'))
    # print(Utils.format_time_tag('Yesterday 7:40 PM'))
    # print(Utils.format_time_tag('Sunday 7:40 PM'))
    # print(Utils.format_time_tag('Monday 7:40 PM'))
    # print(Utils.format_time_tag('Tuesday 7:40 PM'))
    # print(Utils.format_time_tag('Wednesday 7:40 PM'))
    # print(Utils.format_time_tag('Thursday 7:40 PM'))
    # print(Utils.format_time_tag('Friday 7:40 PM'))
    # print(Utils.format_time_tag('Saturday 7:40 PM'))
