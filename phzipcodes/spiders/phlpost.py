import scrapy


class PhlpostSpider(scrapy.Spider):
    name = "phlpost"
    allowed_domains = ["phlpost.gov.ph"]
    start_urls = ["https://phlpost.gov.ph/zip-code-locator/"]

    def parse(self, response):
        for row in response.xpath('//table[@id="offices"]/tbody/tr'):
            yield {
                "zip": row.xpath("./td[4]/text()").get(),
                "region": row.xpath("./td[1]/text()").get(),
                "province": row.xpath("./td[2]/text()").get(),
                "city": row.xpath("./td[3]/text()").get()
            }
