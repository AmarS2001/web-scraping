url = 'https://www.amazon.co.jp/s?k=cap&ref=nb_sb_noss'

import httpx
import asyncio
from bs4 import BeautifulSoup as bs
import json
from datetime import datetime
from randomheader import RandomHeader
from fp.fp import FreeProxy

rh = RandomHeader().header()
# proxy = FreeProxy().get()
# print(proxy)



# proxies = {
#    'http://': proxy,
#    'https://': proxy,
# }

async def run():
    limits = httpx.Limits(max_connections=5)
    async with httpx.AsyncClient(limits=limits, timeout=httpx.Timeout(15.0), headers=rh) as session:
        result = await session.get(url)
        return result
    
def getRank(asinList, asin, itemLookUp):
    currentTime = datetime.now()
    rank = asinList.index(asin) + 1
    return {"time":currentTime.strftime("%m/%d/%Y, %H:%M:%S"), "asin":asin, "rank": rank, "item name": itemLookUp[asin], "keyword": 'pencil'}

def getUrl(keyword,pageNo):
    item = keyword.replace(' ','+')
    return 'https://www.amazon.co.jp/s?k={itemName}&ref=nb_sb_noss'.format(itemName=item)


if __name__ == '__main__':
    res = asyncio.run(run())
    soup = bs(res, 'html.parser')
    result = soup.find_all('div',{"data-asin":True})
    asinList = []
    itemLookUp = dict()
    for item in result:
        if item['data-asin']:
            asinList.append(item['data-asin'])
            name = item.find('span',{'class':"a-size-base-plus a-color-base a-text-normal"})
            if name:
                itemLookUp[item['data-asin']] = name.contents
            else:
                itemLookUp[item['data-asin']] = 'not loaded'
    asinInput = 'B0BYM5XDCT'
    print(getRank(asinList, asinInput, itemLookUp))
