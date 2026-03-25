import requests
from scrapy import Item
from scrapy.exceptions import DropItem

from ukrradiorss.exporters import RssExporter
from ukrradiorss.items import ChannelItem, RssItem

class EnclosureMetadataPipeline:
    def process_item(self, item: Item):
        if type(item) is RssItem:
            rsp = requests.head(str(item.get("enc_url")), headers={
                                'User-Agent': 'python/requests'})
            if rsp.ok:
                item["enc_length"] = rsp.headers["content-length"]
        return item


class RssOutputPipeline:

    def open_spider(self, spider):
        self.file = open(spider.name + "-feed.rss", "w")

    def close_spider(self):
        self.exporter.finish_exporting()
        self.file.close()

    def _channel_init(self, item: Item):
        self.exporter = RssExporter(
            file=self.file,
            title=item.get("title"),
            link=item.get("link"),
            description=item.get("description"),
            image=item.get("image", None),
            language="uk-UA",
            pubDate=item.get("pubDate", None),
            lastBuildDate=item.get("lastBuildDate", None),
            managingEditor=item.get("managingEditor", None),
            copyRight=item.get("copyRight", None)
        )
        self.exporter.start_exporting()

    def process_item(self, item: Item):
        if isinstance(item, ChannelItem):
            if not hasattr(self, 'exporter'):
                self._channel_init(item)
            else:
                raise DropItem("already recorded")
        else:
            self.exporter.export_item(item)
        return item
