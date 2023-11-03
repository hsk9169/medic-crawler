import time
from api import ApiCrawler 
from db import DbClient 

if __name__ == '__main__':
    print('start')
    crawler = ApiCrawler()
    crawler.initApiInfo()

    dbClient = DbClient()
    dbClient.connectDb()
    dbClient.dropDb()
    dbClient.createDb()
    dbClient.createTable()

    for pageNo in range(crawler.totalPageNo):
        try:
            print(f'Page Number: {pageNo}')
            crawler.pageCountUp()
            pageItems = crawler.reqGetPage()
            if pageItems is not False:
                for item in pageItems:
                    dbClient.addRow(item['yadmNm'], item['addr'])
                dbClient.commitQueries()
                num = dbClient.getRowNum()
                if num is not False:
                    print(f'Total row num: {num}')
                else:
                    print('Failed getting row num')
                    break
                time.sleep(5)
            else:
                print('Failed to get hospital info page, terminating')
                break
        except Exception as err:
            print(err)
            print('Stop crawling because of an error')
            break
    
    print('Crawling successfully executed')
    dbClient.close()
