# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import os
import sys
import time
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
from PIL import Image, ImageDraw, ImageFont

pattern = re.compile(r'([^<>/\\\|:""\*\?]+)\.\w+$')
#水印位置 需要减去四个像素
test_marker_margin = 4
textMark = "power @ leaveastory.com; spider@caterpillar"
# 获取图片
def getImg(site_url: str,flag):
    # 访问网站
    url = requests.get(site_url)
    # 获取网站数据
    html = url.text
    # print(html)
    # 创建对象，解析网页，lmxl
    soup = BeautifulSoup(html, "html.parser")
    # 获取所有img标签
    imgTags = soup.find_all("img")
    print(len(imgTags))
    # 解析img标签 
    parser_img_tags(imgTags,flag)

# 解析img标签，获取图片链接
def parser_img_tags(imgTags,flag):
    for imgTag in imgTags:
        if flag:
            # 单张图片
            save_image(imgTag.get("data-vpf-src"))
        else:
            # 不同尺寸大小的图片
            imgs_set_str = imgTag.get("data-vpf-srcset")
            for imgs_url_and_size_str in imgs_set_str.split(","):
                save_image(imgs_url_and_size_str)
 
def add_water_marker( imgPath):
    image = Image.open(imgPath)
    # 实例化图片对象
    img = Image.open(imgPath)
    
    # 获取图片的宽、高,以便计算图片的相对位置
    w, h = img.size  
    
    #查看图片高度
    # print("图片高度：",h)
    # print("图片宽度：",w)
    # 设置字体、字体大小
    font = ImageFont.truetype('C:/Users/Administrator/SourceHanSansCN-Regular.ttf',22)
    draw = ImageDraw.Draw(img)
    font_x,font_y =font.getsize(textMark)
    #draw.text的四个参数设置:文字位置(横坐标，纵坐标)/内容/颜色/字体
    draw.text((w - font_x - test_marker_margin,h - font_y - test_marker_margin), text=textMark, fill=(0, 0, 0,0), font=font)
    img.save(imgPath)

# 保存图片、加水印      
def save_image(imgs_url_and_size_str):
    # https://leaveastory.com/wp-content/uploads/2018/03/359-500x500.png 500w
    img_url = imgs_url_and_size_str.split(" ")[0]
    img_name = pattern.findall(img_url)
    if(img_name):
        img_full_name = "./leave_a_story/image/%s.png" % img_name[0]
        urllib.request.urlretrieve(img_url,img_full_name)
        time.sleep(3)
        add_water_marker(img_full_name)
        time.sleep(3)
if __name__ == "__main__":
    i = 0
    flag = 1
    # 仅下载前9页
    for i  in  range(1,10):
        getImg("https://leaveastory.com/?vp_page=%s" % str(i),flag)