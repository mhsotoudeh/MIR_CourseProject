import scrapy
from ..items import SemanticscholarItem


class SemanticScholarSpider(scrapy.Spider):
    name = 'semanticscholar'
    f = open('start.txt', 'r')
    start_urls = [url.strip() for url in f.readlines()]
    f.close()
    print(start_urls)

    def parse(self, response):
        items = SemanticscholarItem()

        title = response.css("h1::text").extract_first()
        abstract = response.css("meta[name=description]::attr(content)").extract_first()
        year = response.css("ul.paper-meta span[data-selenium-selector=paper-year] > span  > span::text").extract_first()
        authors = response.css("meta[name=citation_author]::attr(content)").extract()
        refs = response.css("#references > div.card-content > div > div.citation-list__citations > div.paper-citation > div.citation__body > h2 > a::attr(href)").extract()

        items['title'] = title
        items['abstract'] = abstract
        items['year'] = year
        items['authors'] = authors
        items['refs'] = refs

        # print("/////////// For Test ////////////")
        # for item in items:
        #     print(item['title'])
        # print("/////////// End Test ////////////")

        yield items

        next_links = refs[:5]
        for link in next_links:
            link = "https://www.semanticscholar.org" + link

        if next_links:
            yield scrapy.Request(response.urljoin(next_links), callback=self.parse)
