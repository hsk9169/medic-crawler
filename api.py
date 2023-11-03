from info import API_INFO
import xmltodict
import requests
import math
import time

class ApiCrawler:
    def __init__(self):
        self.key = API_INFO['serviceKey']
        self.url = API_INFO['base_url'] + API_INFO['path']['getList']
        self.session = requests.Session()
        self.headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        self.curPageNo = 0 
        self.totalPageNo = 0
        self.numOfRows = 5000
        self.count = 0
        self.retryNum = 5
        self.timeout = 120

    def setQueryParams(self, numOfRows, pageNo):
        queryParams = f'?ServiceKey={self.key}'
        queryParams = queryParams + f'&numOfRows={numOfRows}'
        queryParams = queryParams + f'&pageNo={pageNo}'
        return queryParams

    def initApiInfo(self):
        queryParams = self.setQueryParams(1, 1)
        trial = 0
        res = self.session.get(self.url + queryParams, headers=self.headers)
        print(f'status code: {res.status_code}')
        res_dict = xmltodict.parse(res.content)
        try:
            self.totalPageNo = math.ceil(int(res_dict['response']['body']['totalCount']) / self.numOfRows)
            print(f'Total PageNo: {self.totalPageNo}')
        except Exception as err:
            print(err)
            print(res_dict)
            print('error occurred during api request')

    def pageCountUp(self):
        self.curPageNo = self.curPageNo + 1

    def reqGetPage(self):
        queryParams = self.setQueryParams(self.numOfRows, self.curPageNo) 
        self.session.close()
        self.session = requests.Session()
        res = self.session.get(self.url + queryParams, headers=self.headers)
        print(f'status code: {res.status_code}')
        res_dict = xmltodict.parse(res.content)
        trial = 0
        ret = False
        #while trial < self.retryNum:
        try:
            header = res_dict['response']['header']
            res_msg = header['resultMsg']
            body = res_dict['response']['body']
            items = body['items']['item']
            ret = items
        except Exception as err:
            print(err)
            print(res_dict)
            print('error occurred during api request')
            trial = trial + 1
            time.sleep(10)
        return ret
