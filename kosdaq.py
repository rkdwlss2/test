from selenium import webdriver
from itertools import count
import time
from bs4 import BeautifulSoup
import pandas as pd
result = []
url2 = 'https://finance.naver.com/sise/sise_index_day.nhn?code=KOSDAQ'
driver = webdriver.Chrome('chromedriver.exe')
time.sleep(4)
driver.get(url2)  
pagenum=1
trlist=[]
while True:
        stop=0
        for i in [3,4,5,10,11,12]:
            temp=[]
            for j in [1,2,3,6,4]:
                dat1=driver.find_element_by_xpath("//*[@class='type_1']/tbody/tr[%s]/td[%s]"%(str(i),str(j)))
                dat=dat1.text
                cla=dat1.get_attribute('class')
                if (j==1)&(dat[:4]=="2019"):
                    stop=1
                    break
                if cla[-4:-2]=="nv":
                    temp.append('-'+dat)
                elif cla[-4:-2]=="ed":
                    temp.append('+'+dat)
                else:
                    temp.append(dat)
            if stop!=1:
                trlist.append(temp)
        pagenum+=1
        if stop==1:
            trlist=pd.DataFrame(trlist,columns=["date","체결가","전일비","거래대금","등락률"])
            trlist=trlist.sort_values(by='date',ascending=True) 
            trlist.to_csv('kosdaq.csv',encoding='utf-8-sig')
            break
        driver.get(url2+"&page="+str(pagenum))