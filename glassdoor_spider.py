from scrapy import Spider, Request
from glassdoor.items import GlassdoorItem
import re


class GlassdoorSpider(Spider):
    name = "glassdoor_spider"
    allowed_urls = ['https://www.glassdoor.com/']
    start_urls = ['https://www.glassdoor.com/Reviews/J-P-Morgan-Reviews-E145.htm']

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
                'J-P-Morgan-Reviews-E145',
                'Citi-Reviews-E8843',
                'Morgan-Stanley-Reviews-E2282',
                'Goldman-Sachs-Reviews-E2800',
                'Bank-of-America-Reviews-E8874',
                'Evercore-Partners-Reviews-E11361',
                'Centerview-Partners-Reviews-E278475',
                'Duff-and-Phelps-Reviews-E14393',
                'Stifel-Financial-Reviews-E388861',
                'Brown-Brothers-Harriman-Reviews-E3668',
                'Cantor-Fitzgerald-Reviews-E12073',
                'Deutsche-Bank-Reviews-E3150',
                'Wells-Fargo-Reviews-E8876'
                ]

        for index, name in enumerate(rev):
            url = 'https://www.glassdoor.com/Reviews/{}.htm'.format(name)

            i = 2
            names_url = 'https://www.glassdoor.com/Reviews/' + name + '_P' + str(i) + '.htm'

            yield Request(url, callback = self.parse_review, meta={'name': name})
            yield Request(names_url, callback= self.parse_company, meta={'name': name})



    def parse_company(self, response):
        i = 2
        num_reviews = response.xpath('.//div[@class="padTopSm margRtSm margBot minor"]/text()').extract_first()
        if re.findall("\d+[,.]\d+", num_reviews) != []:
            tot_review = re.findall("\d+[,.]\d+", num_reviews)[0]
        else:
            tot_review = re.findall("\d+", num_reviews)[0]
        rev_count = int(tot_review.replace(',', ''))
        page_num = rev_count / 10


        while(i< page_num):
        # while(i < 5):
            names_url = 'https://www.glassdoor.com/Reviews/' + response.meta['name'] + '_P' + str(i) + '.htm'
            # print(names_url,'!' * 50)
            # if i > page_num:
                # break
            # else:

            yield Request(names_url, callback = self.parse_review)

            i += 1

    def parse_review(self, response):

        rows = response.xpath('//*[@id="ReviewsFeed"]/ol/li')

        for i in range(0, len(rows)):
            Name = rows[i].xpath('//*[@id="EmpHeroAndEmpInfo"]/div[3]/div[2]/p/text()').extract_first()
            Rating = rows[i].xpath('.//span[@class="value-title"]/@title').extract_first()

            # if 'Work/Life Balance' in rows[i].xpath('.//div[@class="minor"]/text()').extract():
            #     l = rows[i].xpath('.//div[@class="minor"]/text()').extract().index('Work/Life Balance')
            # else:
            #     l = []

            # if l != []:
            #     WorkLife = row.xpath('.//span[@class="gdBars gdRatings med "]/@title').extract()[l]
            # else:
            #     WorkLife = ''




            WorkLife = rows[i].xpath('./div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[1]/span/@title').extract_first()
            CultureVal = rows[i].xpath('./div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[2]/span/@title').extract_first()
            CareerOpp = rows[i].xpath('./div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[3]/span/@title').extract_first()
            CompBen = rows[i].xpath('./div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[4]/span/@title').extract_first()
            SnrMgmt = rows[i].xpath('./div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[5]/span/@title').extract_first()

            //*[@id="empReview_16032669"]/div/div[2]/div/div[2]/div/div[1]/span/div/ul/li[1]/div


            if 'Recommends' in rows[i].xpath('.//span[@class="middle"]/text()').extract():
                Recommend = 'Recommends'
            elif 'Doesn\'t Recommend' in rows[i].xpath('.//span[@class="middle"]/text()').extract():
                Recommend = 'Doesn\'t Recommend'
            else:
                Recommend = ''

            if 'Neutral Outlook' in rows[i].xpath('.//span[@class="middle"]/text()').extract():
                Outlook ='Neutral Outlook'
            elif 'Positive Outlook' in rows[i].xpath('.//span[@class="middle"]/text()').extract():
                Outlook = 'Positive Outlook'
            elif 'Negative Outlook' in rows[i].xpath('.//span[@class="middle"]/text()').extract():
                Outlook = 'Negative Outlook'
            else:
                Outlook = ''

            OpCEO = rows[i].xpath('.//span[@class="showDesk"]/text()').extract_first()

            if 'Current' in ''.join(rows[i].xpath('.//span[@class="authorJobTitle middle reviewer"]/text()').extract()).split():
                EmpType = 'Current'
            elif 'Former' in ''.join(rows[i].xpath('.//span[@class="authorJobTitle middle reviewer"]/text()').extract()).split():
                EmpType = 'Former'
            else:
                EmpType = ''

            AuthTitle = rows[i].xpath('.//span[@class="authorJobTitle middle reviewer"]/text()').extract_first()
            AuthLoc = rows[i].xpath('.//span[@class="authorLocation middle"]/text()').extract_first()
            DateRev = rows[i].xpath('.//time[@class="date subtle small"]/text()').extract_first()
            UserSumm = rows[i].xpath('.//p[@class=" tightBot mainText"]/text()').extract_first()


            Pros = ' '.join(rows[i].xpath('.//p[@class=" pros mainText truncateThis wrapToggleStr"]/text()').extract())
            Cons = ' '.join(rows[i].xpath('.//p[@class=" cons mainText truncateThis wrapToggleStr"]/text()').extract())
            Advice = ' '.join(rows[i].xpath('.//p[@class=" adviceMgmt mainText truncateThis wrapToggleStr"]/text()').extract())

            Name = self.verify(Name)
            Rating = self.verify(Rating)
            WorkLife = self.verify(WorkLife)
            CultureVal = self.verify(CultureVal)
            CareerOpp = self.verify(CareerOpp)
            CompBen = self.verify(CompBen)
            SnrMgmt = self.verify(SnrMgmt)
            Recommend = self.verify(Recommend)
            Outlook = self.verify(Outlook)
            OpCEO = self.verify(OpCEO)
            EmpType = self.verify (EmpType)
            AuthTitle = self.verify(AuthTitle)
            AuthLoc = self.verify(AuthLoc)
            DateRev = self.verify(DateRev)
            UserSumm = self.verify(UserSumm)
            Pros = self.verify(Pros)
            Cons = self.verify(Cons)
            Advice = self.verify(Advice)

            item = GlassdoorItem()
            item['Name'] = Name
            item['Rating'] = Rating
            item['WorkLife'] = WorkLife
            item['CultureVal'] = CultureVal
            item['CareerOpp'] = CareerOpp
            item['CompBen'] = CompBen
            item['SnrMgmt'] = SnrMgmt
            item['Recommend'] = Recommend
            item['Outlook'] = Outlook
            item['OpCEO'] = OpCEO
            item['AuthTitle'] = AuthTitle
            item['EmpType'] = EmpType
            item['AuthLoc'] = AuthLoc
            item['DateRev'] = DateRev
            item['UserSumm'] = UserSumm
            item['Pros'] = Pros
            item['Cons'] = Cons
            item['Advice'] = Advice

            yield item