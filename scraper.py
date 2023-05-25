import httpx
import asyncio
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
from randomheader import RandomHeader
from fp.fp import FreeProxy
from env import *

class Scraper:
    def __init__(self, keyword, asin):
        self.currentTime = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.randomHeader = RandomHeader().header()
        self.keyword = keyword
        self.pageNo = 1
        self.asin = asin
        self.url = self.getUrl()
        self.previousPageTotal = 0
        self.asinList = []
        self.itemLookUp = dict()
        self.proxy_url = "http://51.178.47.12:80"
        self.proxies = {"http://": self.proxy_url, "https://": self.proxy_url}

    def getUrl(self):
        item = self.keyword.replace(' ','+')
        return BASE_URL.format(itemName=item, pageNo=self.pageNo)
    
    def getRank(self, asinList, itemLookUp):
        rank = asinList.index(self.asin) + 1 + self.previousPageTotal
        return {"time":self.currentTime, "asin":self.asin, "rank": rank, "item name": itemLookUp[self.asin], "keyword": self.keyword}
    
    async def htmlPage(self):
        limits = httpx.Limits(max_connections=MAX_CONNECTION)
        async with httpx.AsyncClient(limits=limits, timeout=httpx.Timeout(TIME_OUT), headers= self.randomHeader) as session:
            result = await session.get(self.url)
            return result
        
    async def run(self):
        isFound = False
        while not isFound:
            self.pageNo = self.pageNo + 1
            if self.pageNo > MAX_PAGE:
                isFound = True
                return 'could not able to find'

            res = await self.htmlPage()
            soup = bs(res, 'html.parser')
            result = soup.find_all('div',{"data-asin":True})

            for item in result:
                if item['data-asin']:
                    self.asinList.append(item['data-asin'])
                    name = item.find('span',{'class':"a-size-base-plus a-color-base a-text-normal"})
                    if name:
                        self.itemLookUp[item['data-asin']] = name.contents
                    else:
                        self.itemLookUp[item['data-asin']] = 'not loaded'
            if self.asin in self.asinList:
                isFound = True
                break
            self.previousPageTotal = len(self.asinList)
            print(f'searched {self.previousPageTotal} item did not found in page {self.pageNo}')
            self.asinList = []
            self.itemLookUp = dict()
        return self.getRank(self.asinList, self.itemLookUp)
        # res = await self.htmlPage()
        # soup = bs(res, 'html.parser')
        # result = soup.find_all('div',{"data-asin":True})
        # asinList = []
        # itemLookUp = dict()
        # for item in result:
        #     if item['data-asin']:
        #         asinList.append(item['data-asin'])
        #         name = item.find('span',{'class':"a-size-base-plus a-color-base a-text-normal"})
        #         if name:
        #             itemLookUp[item['data-asin']] = name.contents
        #         else:
        #             itemLookUp[item['data-asin']] = 'not loaded'
        # return self.getRank(asinList, itemLookUp)
        

