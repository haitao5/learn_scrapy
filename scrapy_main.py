#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#import argparse
# import re
from multiprocessing import Pool
import requests
import bs4
import time
#import json
# import io
import  csv

root_url = 'http://wufazhuce.com'

def get_url(num):
    # 拼接URL
    return root_url + '/one/' + str(num)

def get_urls(num):
    # 使用map(function, iterable, ...) 函数根据提供的函数对指定序列做映射
    urls = map(get_url, range(100,100+num))
    return urls

def get_data(url):
    dataList = {}
    dataList["url"] = url
    response = requests.get(url)    # 读取网页
    if response.status_code != 200:
        return {'noValue': 'noValue'}
    #print(response.text)
    # 解析    
    soup = bs4.BeautifulSoup(response.text,"html.parser")
    dataList["index"] = soup.title.string[4:7]
    for meta in soup.select('meta'):
        if meta.get('name') == 'description':
            dataList["content"] = meta.get('content')
    dataList["imgUrl"] = soup.find_all('img')[1]['src']
    return dataList


if __name__=='__main__':
    """
    使用 pool.map(function, iter)将迭代器中的数字作为参数依次传入函数中
    """

    pool = Pool(4)   # 创建线程池资源
    dataList = []
    urls = get_urls(10)  # 映射URL列表
    
    # 
    # 记录运行时间
    start = time.time()
    dataList = pool.map(get_data, urls)
    end = time.time()
    print ('use: %.2f s' % (end - start))

    # 保存到CVS文件中
    f = open('res.cvs', 'w', newline='')
    fWriter = csv.writer(f, delimiter='\t')
    fWriter.writerow(['URL', 'Index', 'Content', 'imURL'])
    for i in dataList:
        fWriter.writerow([i['url'], i['index'], i['content'], i['imgUrl']])
        print(i)
    f.close()
    
    """
    # 保存到json
    jsonData = json.dumps({'data':dataList})
    with open('data.json', 'w') as outfile:
        json.dump(jsonData, outfile)
    """
