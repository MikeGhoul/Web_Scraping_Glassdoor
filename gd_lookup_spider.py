from scrapy import Spider, Request
from gd_lookups.items import GdLookupsItem
import re


class GDSpider(Spider):
    name = "gd_lookup_spider"
    allowed_urls = ['https://www.glassdoor.com/']
    start_urls = ['https://www.glassdoor.com/Overview/Working-at-J-P-Morgan-EI_IE145.11,21.htm']

    def verify(self, content):
        if isinstance(content, list):
            if len(content) > 0:
                return content[0]
            else:
                return ""
        else:
            return content

    def parse(self, response):

        rev= [
                'Overview/Working-at-J-P-Morgan-EI_IE145.11,21.htm',
                'citi',
                'Overview/Working-at-Morgan-Stanley-EI_IE2282.11,25.htm',
                'Overview/Working-at-Goldman-Sachs-EI_IE2800.11,24.htm',
                'Overview/Working-at-Bank-of-America-EI_IE8874.11,26.htm',
                'Overview/Working-at-Evercore-Partners-EI_IE11361.11,28.htm',
                'Overview/Working-at-Centerview-Partners-EI_IE278475.11,30.htm',
                'Overview/Working-at-Duff-and-Phelps-EI_IE14393.11,26.htm',
                'Overview/Working-at-Stifel-Financial-EI_IE388861.11,27.htm',
                'Overview/Working-at-Brown-Brothers-Harriman-EI_IE3668.11,34.htm',
                'Overview/Working-at-Cantor-Fitzgerald-EI_IE12073.11,28.htm',
                'Overview/Working-at-Deutsche-Bank-EI_IE3150.11,24.htm',
                'Overview/Working-at-Wells-Fargo-EI_IE8876.11,22.htm'
                ]

        for index, name in enumerate(rev):
            url = 'https://www.glassdoor.com/{}'.format(name)

            yield Request(url, callback = self.parse_overview, meta={'name': name})


    def parse_overview(self, response):

        rows = response.xpath('//*[@id="EmpBasicInfo"]')


        Name = response.xpath('//*[@id="EmpHeroAndEmpInfo"]/div[3]/div[2]/h1/text()').extract_first()

        if 'Headquarters' in rows.xpath('.//div[@class="infoEntity"]/label/text()').extract():
            l = rows.xpath('.//div[@class="infoEntity"]/label/text()').extract().index('Headquarters')
        else:
            l = []

        if l != []:
            HeadQ = rows.xpath('.//span[@class="value"]/text()').extract()[l-1]
        else:
            HeadQ = ''


        if 'Size' in rows.xpath('.//div[@class="infoEntity"]/label/text()').extract():
            l = rows.xpath('.//div[@class="infoEntity"]/label/text()').extract().index('Size')
        else:
            l = []

        if l != []:
            Size = rows.xpath('.//span[@class="value"]/text()').extract()[l-1]
        else:
            Size = ''

        if 'Founded' in rows.xpath('.//div[@class="infoEntity"]/label/text()').extract():
            l = rows.xpath('.//div[@class="infoEntity"]/label/text()').extract().index('Founded')
        else:
            l = []

        if l != []:
            Founded = rows.xpath('.//span[@class="value"]/text()').extract()[l-1]
        else:
            Founded = ''


        if 'Type' in rows.xpath('.//div[@class="infoEntity"]/label/text()').extract():
            l = rows.xpath('.//div[@class="infoEntity"]/label/text()').extract().index('Type')
        else:
            l = []

        if l != []:
            Type = rows.xpath('.//span[@class="value"]/text()').extract()[l-1]
        else:
            Type = ''


        if 'Revenue' in rows.xpath('.//div[@class="infoEntity"]/label/text()').extract():
            l = rows.xpath('.//div[@class="infoEntity"]/label/text()').extract().index('Revenue')
        else:
            l = []

        if l != []:
            Revenue = rows.xpath('.//span[@class="value"]/text()').extract()[l-1]
        else:
            Revenue = ''



        Name = self.verify(Name)
        HeadQ = self.verify(HeadQ)
        Size = self.verify(Size)
        Founded = self.verify(Founded)
        Type = self.verify(Type)
        Revenue = self.verify (Revenue)




        item = GdLookupsItem()
        item['Name'] = Name
        item['HeadQ'] = HeadQ
        item['Size'] = Size
        item['Founded'] = Founded
        item['Type'] = Type
        item['Revenue'] = Revenue

        yield item

