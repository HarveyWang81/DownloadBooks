#!/bin/env python3
# coding:utf-8

"""
# Author:   Harvey.Wang
# Data:     3/27/2020 9:01 AM
# File:     DownloadBooks.py
# Software: DownloadBooks
# Email:    kenwanglin@gmail.com
# Desc:     
"""

import requests
from lxml.html import etree
from urllib import parse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer,Image,Table,TableStyle,Frame,ListFlowable, ListItem
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.colors import CMYKColor
from reportlab.lib.units import mm
import os
from libs import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

log = logger.Logger('logs/DownloadBooks.out.log', level='info')

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "http://www.ruiwen.com/jiaocai/shuxue/bubianban/yinianjishangce/shangce11.html",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

values = {
    'request_type': 'GET'
}

main_url = 'http://www.ruiwen.com'


def getResponse(url, headers={}, values={}, datas={}):
    if str.upper(values['request_type']) in {'GET', ''}:
        r = requests.get(url=url, headers=headers)
    elif str.upper(values['request_type']) == 'POST':
        r = requests.post(url=url, headers=headers, data=datas)

    return r


def generate_catalog(html, catalog_xpath):
    list_catalog = []
    datas = etree.HTML(html.content).xpath(catalog_xpath)
    for data in datas:
        log.logger.debug('url={0} title={1}'.format(data.attrib['href'], data.attrib['title']))
        list_catalog.append({'url': data.attrib['href'], 'title': data.attrib['title']})
    return list_catalog


def download_image(url, img_xpath, dir_path):
    file_list = []
    i = 0

    while True:
        r = getResponse(url=url, headers=headers, values=values)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            break

    img_datas = etree.HTML(r.content).xpath(img_xpath)
    img_url, img_name = os.path.split(img_datas[0].attrib['src'])

    while True:
        i = i + 1

        download_img_url = 'http:{0}/{1}.jpg'.format(img_url, i)
        log.logger.info('Downloading file {0}'.format(download_img_url))

        image = requests.get(headers=headers, url=download_img_url)

        if image.status_code >= 400:
            break

        file_name = '{0}/{1}'.format(dir_path, os.path.basename(download_img_url))

        with open(file_name, 'wb') as f:
            f.write(image.content)

        file_list.append(file_name)


    return file_list

def generate_pdf(book_name, file_list):
    book_name = os.path.join(BASE_DIR, 'Books', book_name)

    book = []

    for file_name in file_list:
        log.logger.debug(file_name)
        img = Image(file_name)
        img.drawHeight = 260 * mm  # 设置读取后图片的高
        img.drawWidth = 200 * mm  # 设置读取后图片的宽
        book.append(img)

    doc = SimpleDocTemplate(book_name + '.pdf', pagesize = [210 * mm, 297 * mm], topMargin=15 * mm, bottomMargin=15 * mm)
    doc.build(book)
    log.logger.info('Download is done {0}'.format(book_name + '.pdf'))


def main():
    url = 'http://www.ruiwen.com/jiaocai/yuwen/bubianban/yinianjixiace/xiace1.html'
    # catalog_xpath = '/html/body/div[2]/div[2]/div/ul/li/a'
    page_xpath = '//*[@class="pic"]/a'
    img_xpath = '//*[@class="pic"]/a/img'

    book_name = '部编版一年级语文下册'

    file_list = []

    dir_path = os.path.join(BASE_DIR, 'temp', book_name)

    while True:
        r = getResponse(url=url, headers=headers, values=values)
        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            break

    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    file_list = download_image(url, img_xpath, dir_path)
    log.logger.debug(file_list)

    generate_pdf(book_name, file_list)


if __name__ == '__main__':
    main()
