#!/usr/bin/env python
# coding: utf-8

# In[1]:


#整合+蘋果
from selenium import webdriver #打開網頁瀏覽器 需driver
from selenium.webdriver.chrome.options import Options
import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import time
import pandas as pd

#自由電子報
def get_ltn(search):
    print("搜尋自由電子報")
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    links = []
    titles = []
    times = []

    for page in range(1,201):
        url  = f'https://search.ltn.com.tw/list?keyword={search}&page={page}'
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text)
        re = soup.find_all('div', class_="cont")
        if re == []:
            print(f"Page {page} no result")
            break
        for i in re:
            url = i.find('a')['href']
            #print(url)
            links.append(url)
            title = i.find('a').text
            titles.append(title)
            #print(title)
            time = i.find('span').text
            times.append(time)
        #print(time)
        print(f"Page {page} done")
    print("----------------------------------------------------")
    print("自由電子報 Done")
    #print(titles)
    return titles,times,links
#東森新聞
def get_ebc(search):
    print("搜尋東森新聞")
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    links = []
    titles = []
    times = []

    for page in range(1,201):
        url  = f'https://news.ebc.net.tw/Search/Result?type=keyword&value={search}&page={page}'
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text)
        re = soup.find_all('div', class_="style1 white-box")
        if re == []:
            print(f"Page {page} no result")
            break
        for i in re:
            url = i.find('a')['href']
            url = f"https://news.ebc.net.tw/{url}"
            #print(url)
            links.append(url)
            title = i.find("div",class_="title").text
            #print(title)
            titles.append(title)
            time = i.find('span',class_="small-gray-text").text
            #print(time)
            times.append(time)
        
        print(f"Page {page} done")
    print("----------------------------------------------------")
    print("東森新聞 Done")
    print("----------------------------------------------------")
    #print(titles)
    return titles,times,links

#中時新聞網
def get_cht(search):
    print("搜尋中時新聞網")
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
    links = []
    titles = []
    times = []

    for page in range(1,201):
        url  = f'https://www.chinatimes.com/search/{search}?page={page}&chdtv'
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.text)

        if soup.find_all('h3') == []:
            print(f"Page {page} no result")
            break
        for i in soup.find_all('h3'):
            url = i.find('a')['href']
            title = i.find('a').text
            #time = soup.find('span',class_='date').text
            #print(url)
            #print(title)
            #print(time)
            links.append(url)
            titles.append(title)
        for i in soup.find_all('div',class_='meta-info'):
            time = i.find('span',class_='date').text
            #print(time)
            times.append(time)
        
        print(f"Page {page} done")
    print("----------------------------------------------------")
    print("中時新聞網 Done")
    print("----------------------------------------------------")
    #print(titles)
    return titles,times,links

#蘋果
def get_apple(search):
    print("搜尋蘋果新聞")
    chrome_options =Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options,executable_path="./chromedriver.exe") #有時\會被偵測為轉行等等符號，這時在前面加r代表不經過轉換
    driver.get(f'https://tw.appledaily.com/search/{search}/')
    

    last_height = driver.execute_script("return document.body.scrollHeight")

    go=True

    while go:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(int(2))
        html_source = driver.page_source
#     soup = BeautifulSoup(html_source, "lxml")
#     re = soup.find_all('span',class_='desktop-blurb  truncate truncate--3')
        new_height = driver.execute_script("return document.body.scrollHeight")

    #已經到頁面底部
        if new_height == last_height:
            print("已經到頁面最底部，程序停止")
            break

        last_height = new_height
    
    links = []
    titles = []
    times = []
    soup = BeautifulSoup(html_source, "lxml")
    select = soup.find('article',class_='grid__col apd-grid__col--lg-8 apd-grid__col--md-4 apd-grid__col--sm-4 article-container')
    re = select.find_all('span',class_='desktop-blurb truncate truncate--3')
    for i in re:
        title = i.text
        #print(title)
        titles.append(title)
    re2 = select.find_all('a',class_=' story-card ')
    for i2 in re2:
        url =  f"https://tw.appledaily.com/{i2['href']}"
        #print(url)
        links.append(url)
    re3 = select.find_all('div',class_='timestamp')
    for i3 in re3:
        time_ = i3.text[6:]
        #print(time)
        times.append(time_)
    driver.close()
    print("----------------------------------------------------")
    print("蘋果新聞 Done")
    print("----------------------------------------------------")
    return titles,times,links
    

name = input("請輸入搜尋關鍵字: ")
a1,b1,c1 = get_ltn(name)
a2,b2,c2 = get_ebc(name)
a3,b3,c3 = get_cht(name)
a4,b4,c4 = get_apple(name)
print("ALL Done")
print("將結果儲存至excel...")
df1 = pd. DataFrame({'Titles':a1, 'Date':b1, 'Links':c1}) 
df2 = pd. DataFrame({'Titles':a2, 'Date':b2, 'Links':c2}) 
df3 = pd. DataFrame({'Titles':a3, 'Date':b3, 'Links':c3}) 
df4 = pd. DataFrame({'Titles':a4, 'Date':b4, 'Links':c4}) 
dfs = {'自由電子報':df1, '東森新聞':df2, '中時新聞網':df3 , '蘋果新聞': df4}
writer = pd.ExcelWriter(f'./{name}.xlsx', engine='xlsxwriter')
for sheet_name in dfs.keys():
    dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False) 
writer.save()
print(f"完成，搜尋結果儲存於{name}.xlsx中")


