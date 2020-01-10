import scrapy
from ..items import SemanticscholarItem


class SemanticScholarSpider(scrapy.Spider):
    name = 'semanticscholar'
    custom_settings = {'CLOSESPIDER_ITEMCOUNT': 5000}
    f = open('start.txt', 'r')
    start_urls = [url.strip() for url in f.readlines()]
    f.close()

    def parse(self, response):
        items = SemanticscholarItem()

        link = response.css("link::attr(href)").extract_first()
        title = response.css("h1::text").extract_first()
        abstract = response.css("meta[name=description]::attr(content)").extract_first()
        year = response.css("ul.paper-meta span[data-selenium-selector=paper-year] > span  > span::text").extract_first()
        authors = response.css("meta[name=citation_author]::attr(content)").extract()
        refs = response.css("#references > div.card-content > div > div.citation-list__citations > div.paper-citation > div.citation__body > h2 > a::attr(href)").extract()
        for i in range(len(refs)):
            refs[i] = "https://www.semanticscholar.org" + refs[i]

        items['link'] = link
        items['title'] = title
        items['abstract'] = abstract
        items['year'] = year
        items['authors'] = authors
        items['refs'] = refs
        yield items

        next_links = refs[:5]
        if next_links:
            for link in next_links:
                yield response.follow(link, callback=self.parse)
