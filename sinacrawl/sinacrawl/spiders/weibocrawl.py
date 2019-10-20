# -*- coding: utf-8 -*-
import scrapy
from sinacrawl.items import SinacrawlItem


class WeibocrawlSpider(scrapy.Spider):

    name = 'weibocrawl'
    allowed_domains = ['weibo.com']
    page_num = 0
    start_urls = 'https://weibo.cn/comment/hot/Hx1gulh4A?rl=1&oid=4378696905070520&page=1'
    cookies = {'ALC': 'ac%3D0%26bt%3D1571499708%26cv%3D5.0%26et%3D1603035708%26ic%3D1881814089%26login_time%3D1571499708%26scf%3D%26uid%3D2321195545%26vf%3D0%26vs%3D0%26vt%3D0%26es%3Dc751b9e1f01096bca62b4d256e10077b', 'SRF': '1571499708', 'SRT': 'D.QqHBJZP3VZm3VrMb4cYGSPHKibSi4NsOW!9w5csHNEYdPDi4R-kpMERt4EPKRcsrA4uJPcuGTsVuOb43INsBi4SlRdsfP!AqAeSdN-yq4sPlSP9gA!P8SFYY*B.vAflW-P9Rc0lR-ykcDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPVsNrMFisEEU4PDPqB8ApsBPrEKieXti49ndDPIJcYPSrnlMcywJFP6JevoNpsc4-XkJcM1OFyHMPYJ5mkiODmk5!oCUrHJ5mkiODEIA!oCUrsJ5mkCOmzlJ!noN39J5mjkODmpJ!oCNpuJ5mkCOmzlS4noIOHr', 'ALF': '1603035708', 'SCF': 'AqbNIxlMC-3BwSMADhNtrzl7cQT7y1dd8Uzq5vFKy_LqdCSvD1VYDjflNprJqP71bocQp_plfaEQKDfcigqLTis.', 'SUB': '_2A25wr17tDeRhGeRN6VMQ-SvJzzmIHXVQUGKlrDV_PUJbm9AKLUX4kW1NU7--A1DnGrIitU1qnHwAcWrjG5NUI947', 'sso_info': 'v02m6alo5qztKWRk5yljpSIpZCjkKWRk5yljpOQpZCjnKWRk5ClkKSEpY6TiKWRk5SljoSEpZCTpKWRk5ClkKSMpY6UhKadlqWkj5OIs4yjhLGOk5S1jYOUwA==', 'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5KDF7QEmECW0bC-AWAN6x85JpX5K2hUgL.Foz0eo2p1K-fSh-2dJLoIEXLxKML1-zLBoBLxKML1KBLBoMLxKBLB.2L1KzLxK-L122LBK.LxKBLB.eL1-2t', 'SUHB': '0auRBdu0ApI0hn'}

    def start_requests(self):
        print(1)
        yield scrapy.Request(url=self.start_urls, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        """
        第一页抓取获取page
        :param response:
        :return:
        """
        url = f'https://weibo.cn/comment/hot/Hx1gulh4A?rl=1&oid=4378696905070520&page={self.page_num}'
        page = response.selector.css('[value]').re_first(r'(\d+)')
        print(page)

        try:
            print(2)
            while self.page_num < int(page):
                print(3)
                self.page_num += 1
                url = f'https://weibo.cn/comment/hot/Hx1gulh4A?rl=1&oid=4378696905070520&page={self.page_num}'
                print(5)
                yield scrapy.Request(url=url, callback=self.commen_parse, cookies=self.cookies, dont_filter=True )
            return None
        except Exception as eRR:
            print(7)
            raise eRR

    def commen_parse(self, response):
        """
        抓取评论
        :param response:
        :return:
        """
        item = SinacrawlItem()

        try:
            comment = response.xpath(r'//div[@class="c"]/span[1]/text()').extract()
            like = response.xpath(r'//div[@class="c"]/span[2]/a/text()').extract() # [i][2:-1]
            user_id = response.xpath(r'//*[@class="c"]/@id').extract() # [i] [2:]
            for i in range(10):
                try:
                    item['comment'] = comment[i]
                    item['like'] = like[i][2:-1]
                    item['user_id'] = user_id[i]
                except IndexError:
                    item['none'] = '没有数据'

                yield item

        except Exception as ERR:
            raise ERR
