from scraper import *
import pprint
class Main:
    def __init__(self, keyword, asin):
        self.keyword = keyword
        self.asin = asin
    
    async def run(self):
        scraper = Scraper(self.keyword, self.asin)
        rank = await scraper.run()
        return rank

if __name__ == "__main__":
    keyword = input()
    asin = input()
    app = Main(keyword, asin)
    result = asyncio.run(app.run())
    pprint.pprint(result)
