from datetime import datetime
import re
from urllib.parse import urljoin

import scrapy

from ukrradiorss.items import ChannelItem, RssItem


class UkrRadioSpider(scrapy.Spider):
    allowed_domains = ["ukr.radio"]
    date_format = '%d.%m.%Y %H:%M:%S'

    def _extract(self, response, path):
        s = response.css(path).get()
        if s is None:
            return ""
        else:
            return re.sub(r"<.*?>", "", s).strip()

    def parse(self, response):
        channel = ChannelItem(
            title=self._extract(
                response, "div.prog-preview div.news-category-title::text") + ' | ' + self._extract(
                response, "div.program-item-controls div::attr(data-media-channel)"),
            link=urljoin(response.url, self._extract(
                response, "div.program-item-controls div::attr(data-media-url)")),
            description=self._extract(
                response, "div.prog-preview div.prog-descr p span span::text"),
            image=urljoin(response.url, self._extract(
                response, "div.prog-preview img::attr(src)")),
            managingEditor="ua.info@suspilne.media",
            copyRight="https://ukr.radio/",
        )
        yield channel
        if response.css("div.program-item"):
            for i in response.css("div.program-item"):
                item = RssItem(
                    title='Ефір ' +
                    self._extract(
                        i, "div.program-item-content div.program-date::text"),
                    link=urljoin(response.url, self._extract(
                        i, "div.program-item-controls div::attr(data-media-period-item-url)")),
                    description=self._extract(
                        i, "div.program-item-content div:nth-of-type(3)"),
                    language="uk-UA",
                    pubDate=datetime.strptime(self._extract(
                        i, "div.program-item-content div.program-date::text"), self.date_format),
                    guid=urljoin(response.url, self._extract(
                        i, "div.program-item-controls div::attr(data-media-period-item-url)")),
                    enc_url=urljoin(response.url, self._extract(
                        i, "div.program-item-controls div::attr(data-media-path)")),
                    enc_type="audio/mpeg"
                )
                yield item

            # navigate next page
            curr_page = self._extract(
                response, "div.btn-pagination ul li.current a::text")
            if curr_page.isdigit():
                yield response.follow(response.url + "&page=" + str(int(curr_page) + 1), self.parse)
