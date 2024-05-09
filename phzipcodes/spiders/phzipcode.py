import scrapy
from scrapy.http import Request
import urllib.parse as urlparse


class PhzipcodeSpider(scrapy.Spider):
    name = "phzipcode"
    allowed_domains = ["www.philippineszipcode.com"]
    start_urls = ["https://www.philippineszipcode.com/browse/"]

    def parse(self, response):
        regions = response.xpath(
            '//h1[@class="page-header"]/../div[last()]/div/div/a[0]/@href'
        ).getall()

        for path in regions:
            yield Request(url=urlparse.urljoin(response.url, path),callback=self.parse_region)

    def parse_region(self, response):
        areas = response.xpath(
            '//h1[@class="page-header"]/../div[last()]/div/div/a[0]/@href'
        ).getall()

        for path in areas:
            yield Request(
                url=urlparse.urljoin(response.url, path), callback=self.parse_area
            )

    def parse_area(self, response):

        rows = response.xpath(
            "//h1[contains(text(), 'Browse ZIP Code')]/../div/div/table/tbody/tr[position() > 1]"
        ).getall()

        for row in rows:
            yield {
                "location": row.xpath("/td[1]/strong/a/text()").get(),
                "municipality": row.xpath("/td[2]/strong/a/text()").get(),
                "province": row.xpath("/td[3]/strong/a/text()").get(),
                "region": row.xpath("/td[4]/strong/a/text()").get(),
                "zip_code": row.xpath("/td[5]/strong/a/text()").get()
            }

        next_page = response.xpath("//div/ul[@class='pagination']/li[last()-1]/a/@href").get()

        if next_page:
            yield Request(
                url=urlparse.urljoin(response.url, next_page), callback=self.parse_area
            )
