# -*- coding: utf-8 -*-
#
import time
from win.pywin import PyWin
from helper.utils import Utils
from helper.my_logging import *

class Share:
    # type: "Contacts" - select in 'Contacts' section
    #       "Group" - select in 'Group' section
    #       None - select in whole list
    def get_candidates(list, member, type):
        candidates = []
        count = False
        if type == None:
            count = True    # count all in list
        items = PyWin.get_children(list)
        # print(len(items))
        for item in items:
            Share.scroll_item_in(list, item)
            # item.draw_outline()
            name = PyWin.get_window_text(item)
            # print('name: "'+name+'"')

            if (name == '') and type:
                section = item.children_texts()
                # print('section:', section)
                if section[0] == type:
                    count = True
                elif count:
                    break
            elif count:
                # <em>highlighted text</em>
                name = name.replace('</em>', '')
                name = name.replace('<em>', '')

                # after clicked 'Show All', need to redo this function call
                if name.startswith('Show All'):
                    PyWin.click_control(item)
                    logger.warning('list has changed')
                    return None
                # search by id, retun th unique member
                # if ('id' in member) and (not member['id'].startswith('wxid_')):
                if (name == member['name']) or ('alias' in member and name == member['alias']):
                    candidates.append(item)
        return candidates


    def select_by_pic(list, candidates, member, get_item_pic):
        if not 'pic' in member:
            return candidates
        # compare pic image
        select = {
            'item': None,
            'pic': None,
            'distance': -1
        }
        for item in candidates:
            Share.scroll_item_in(list, item)
            pic = get_item_pic(item)
            distance = Utils.compare_pics(pic, member['pic'])
            # pic.show()
            # member['pic'].show()
            # print(distance)
            # input('cmopare pics....')

            # 仅保留较小的distance（更相似的）
            if select['distance'] == -1 or select['distance'] > distance:
                print('distance:', distance)
                select['distance'] = distance
                select['item'] = item
                select['pic'] = pic
        select['pic'].show()
        member['pic'].show()
        input('check ...')
        logger.info('picture distance: %d', select['distance'])
        # only keep the similar one
        if select['distance'] < 50:
            return [select['item']]
        logger.warning('did no find similar picture for %s', member['name'])
        return candidates

    def verify_checked(list, item, imgs):
        # time.sleep(1)
        item.draw_outline()
        Share.scroll_item_in(list, item)
        bt0 = imgs['get_checkbox_img'](item)
        d_unchecked_0 = Utils.compare_pics(imgs['unchecked_0_img'], bt0)
        d_unchecked_1 = Utils.compare_pics(imgs['unchecked_1_img'], bt0)
        d_checked_1 = Utils.compare_pics(imgs['checked_1_img'], bt0)
        # print('distances:', d_unchecked_0, d_unchecked_1, d_checked_1)
        if ((d_unchecked_0 < 10) or (d_unchecked_1 < 10)) and (d_checked_1 > 200):
            PyWin.click_control(item)
        else:
            logger.warning('checkbox image may not right, distances: %d, %d, %d', d_unchecked_0, d_unchecked_1, d_checked_1)
        bt1 = imgs['get_checkbox_img'](item)
        distance = Utils.compare_pics(imgs['checked_1_img'], bt1)
        logger.info('checked distance %d, "%s"', distance, PyWin.get_window_text(item))
        return distance

    def scroll_item_in(list, item):
        # scroll item in view
        top = PyWin.get_rect(list).top
        for i in range(100):     # limited loops
            itop = PyWin.get_rect(item).top
            if itop >= top:
                break
            # print('down', top, itop)
            PyWin.mouse_scroll(list, 5) # 动作太大会滑过导致反复
            time.sleep(0.1)

        bottom = PyWin.get_rect(list).bottom
        for i in range(100):
            ibottom = PyWin.get_rect(item).bottom
            if ibottom <= bottom:
                break
            # print('up', bottom, ibottom)
            PyWin.mouse_scroll(list, -5)
            time.sleep(0.1)
