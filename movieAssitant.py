# -*- coding: utf-8 -*-
# @Time    : 2018/7/21 12:30
# @Author  : Torre
# @Email   : klyweiwei@163.com
# 此脚本可以帮助你快速搜索到下载最多(按下载次数下载排行)的电影ed2k, 通过迅雷\电驴等工具下载
# 数据源扩增中, 此项目仅提供两个安全绿色搜索源 https://www.ciliba.me/ ,https://www.zhongzijun.com/
# 如果网址域名被改, 需增加异常以增强程序的强健性
from bs4 import BeautifulSoup as bs
import requests
import os
import re


def getSoup(url):
    response = requests.get(url)
    response.raise_for_status()
    res = response.text
    soup = bs(res, 'html.parser')
    return res, soup


# 入参:电影名字,排名前n(n<=5), 注意：两个网站输出的下载链接个数为2n
def movieAssistant(movie, n):
    url1 = 'https://www.zhongzijun.com/list_click/'+movie+'/1'
    url2 = 'https://www.ciliba.me/s/'+movie+'_hits_1.html'
    # 数据的初始化
    # with open('urls.json', 'r', encoding='utf-8') as f:
    #     urls = json.load(f)
    # print(urls, type(urls))
    ed2ks = []
    res1, soup1 = getSoup(url1)
    links = soup1.select('td.ls-magnet a')
    for link in links[0:n]:
        # print(link.get('href'))
        # # 获取资源大小
        # pattern = re.compile(r'[-+]?[0-9]*\.?[0-9]+')
        # capacity = pattern.findall(str(res1))
        # print(capacity)
        # 获取下载链接
        ed2k = link.get('href')+'\n'
        print(ed2k)
        ed2ks.append(ed2k)
        ed2kWrite(movie, ed2k)
    # print(ed2ks)

    res2, soup2 = getSoup(url2)
    links = soup2.select('h3 a')
    # print(type(links))
    for link in links[0:n]:
        # print(link.get("href"))
        res22, soup22 = getSoup(link.get("href"))
        # 获取资源大小+热度
        pattern = re.compile(r' 种子大小：(.+?)</p>')
        capacity = pattern.findall(str(res22))
        # print(capacity)
        # 获取下载地址
        ed2k = soup22.select('p input')
        # print(ed2k)
        # 数据整合
        print(ed2k[0].get('value')+' '+capacity[0])
        ed2kWrite(movie, ed2k[0].get('value')+' '+capacity[0]+'\n')


# 文件的写入
def ed2kWrite(movie, ed2k):
    # 判断文件是否存在
    # filepath = os.getcwd()+'\\download\\'+ movie+'.txt'
    filepath = os.getcwd()+ movie+'.txt'
    if os.path.exists(filepath):
        # os.remove(filepath)
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(ed2k)
    else:
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(ed2k)


# 测试方法
if __name__ == '__main__':
    movieAssistant('我不是药神', 5)
