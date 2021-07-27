#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from bs4 import BeautifulSoup as bs
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent

html_list = ['messages.html', 'messages2.html']
STR = [':', 'July', 'MA', 'Matvey', 'Akimov']

LIST_PHOTO = []
LIST_TEXT = []
DATA = ''


def read_html(filemane):
    with open(filemane, 'rb') as f:
        data = f.read()
    return data


def get_product_data(html):
    soup = bs(html, 'html.parser')

    list_a = soup.find('div').find_all('a')
    list_div = soup.find_all('div')

    for div in list_div:
        text = div.get_text(strip=True)
        if ':' in text or 'July' in text or 'Matvey' in text or 'MA' in text or not text:
            continue
        if text in LIST_TEXT:
            LIST_TEXT.append(text + '_P')
        else:
            LIST_TEXT.append(text)

    for a in list_a:
        photo = a.get('href')
        if 'tel' in photo or 'messages' in photo:
            continue
        LIST_PHOTO.append(photo)


def save(data):
    for article, img in data.items():
        """ Save article in txt """
        f = open('tmp/art.txt', 'a')
        f.write(article + '\n')
        f.close()

        """ Save img """
        path = os.path.join(BASE_DIR, 'html/img/')
        path_photo = os.path.join(BASE_DIR, 'html', img)
        img = Image.open(path_photo)
        if '/' in article:
            article = article.replace('/', '')
        img.save(path + article + '.jpg')


def parse():
    i = 0
    total_data = len(html_list)
    for h in html_list:
        i += 1
        print('')
        print('>> %s/%s' % (i, total_data), h)
        path = os.path.join(BASE_DIR, 'html', h)
        html = read_html(path)
        get_product_data(html)

    DATA = dict(zip(LIST_TEXT, LIST_PHOTO))
    save(DATA)


parse()
