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

def get_urls(start, num):
    # 使用map(function, iterable, ...) 函数根据提供的函数对指定序列做映射
    urls = map(get_url, range(start, start+num))
    return urls

def get_data(url):
    dataList = {}
    dataList["url"] = url
    response = requests.get(url)    # 读取网页
    if response.status_code != 200:
        return {'noValue': 'noValue'}
    #print(response.text)
    # 解析    
    soup = bs4.BeautifulSoup(response.text,"html.parser")   # .encode("UTF-8", "ignore")
    dataList["index"] = str(soup.title.string[4:8])
    for meta in soup.select('meta'):
        if meta.get('name') == 'description':
            dataList["content"] = str(meta.get('content'))
    dataList["imgUrl"] = str(soup.find_all('img')[1]['src'])
    
    date = soup.select('div[class="one-pubdate"]')[0].get_text()
    dataList["date"] = str(date.replace('\n', ' ').strip())
    return dataList


if __name__=='__main__':
    """
        使用 pool.map(function, iter)将迭代器中的数字作为参数依次传入函数中
    """

    pool = Pool(4)   # 创建线程池资源
    dataList = []
    urls = get_urls(1050, 1000)  # 映射URL列表
    
    # 
    # 记录运行时间
    start = time.time()
    dataList = pool.map(get_data, urls)
    end = time.time()
    print ('use: %.2f s' % (end - start))

    # 保存到CVS文件中
    f = open('res.cvs', 'w', newline='')
    fWriter = csv.writer(f, delimiter='\t')
    fWriter.writerow(['Index', 'Date','Content', 'URL', 'imURL'])
    for i in dataList:
        try:
            print('Current:'+ str(i))
            fWriter.writerow([i['index'], i['date'], i['content'], i['url'], i['imgUrl']])
        except Exception as e:
            print("Unexpected Error: {}".format(e))
            print('Current:'+ str(i))

    f.close()
    
    """
    # 保存到json
    jsonData = json.dumps({'data':dataList})
    with open('data.json', 'w') as outfile:
        json.dump(jsonData, outfile)
    """
