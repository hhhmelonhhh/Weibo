# -*- coding: utf-8 -*-
"""
@author: 恰melon
@ref: https://blog.csdn.net/jiangerchi/article/details/78837910

"""

# --------------------------------------------------------
# 爬取单条微博评论
# 非原创，借鉴博客 https://blog.csdn.net/jiangerchi/article/details/78837910
# 新浪有反扒手段，多准备几个小号，避免封号，必要时可采用代理ip
# --------------------------------------------------------
 
from fake_useragent import UserAgent
import re
import requests
import pandas
import time
import random

headers = {'User-Agent': UserAgent().random}
cookies = {'Cookie':'Your Cookies'} #登录m.weibo.cn，开发者工具获取cookies

def get_one_page(url):
    html = requests.get(url, headers = headers, cookies = cookies)
    html_return = html.json()['data']['html']
    return html_return
 
def parse_one_page(html_return):
    pattern = re.compile(r'com.(\d+)"><img width=".+?" height=".+?" alt="(.+?)" src=".+?" usercard=".+?" ucardconf=".+?"></a>.*?</a>：(.+?)</div>.+?<span node-type="like_status" class=""><em class="W_ficon ficon_praised S_txt2">ñ</em><em>(.+?)</em></span>.+?<div class="WB_from S_txt2">(.+?)</div>',re.S)
    data = re.findall(pattern, html_return)
    return data
 
def write_to_file(data,num):
    savepath = 'YourDir/id{}.csv'
    data_to_write = pandas.DataFrame(data)
    data_to_write.to_csv(savepath.format(num), mode = 'a+', header = False, index = False)
 
def get(url,num):
    html_return = get_one_page(url)                                           
    data = parse_one_page(html_return)
    write_to_file(data, num)
    return data

if __name__ == '__main__':
    base_url = 'https://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&filter=all&page={}'
    num = input() # weiboID   e.g. '4280588624064425'
    
    count = 0
    html1 = requests.get(base_url.format(num, 1), headers = headers, cookies = cookies)
    cnts = html1.json()['data']['count'] 
    print(('Weibo', num.strip('\n'), ':', cnts))
    
    for i in range(1, html1.json()['data']['page']['totalpage'] + 1):
        url = base_url.format(num, i)
        try:
            data = get(url, num)
            count += len(data)
            print('Page{} has been downloaded.'.format(i))
        except:
            print(('Pass page {}.'.format(i)))
            pass
        time.sleep(random.uniform(2, 6))
    print(count)