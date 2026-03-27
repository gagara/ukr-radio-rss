import scrapy
from datetime import datetime


def rfc822_date(date=None):
    date_format = '%a, %d %b %Y %H:%M:%S%z'
    if date is None:
        return datetime.now().strftime(date_format)
    if isinstance(date, datetime):
        return date.strftime(date_format)
    return str(date)


class ChannelItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
    language = scrapy.Field()
    pubDate = scrapy.Field(serializer=rfc822_date)
    lastBuildDate = scrapy.Field(serializer=rfc822_date)
    managingEditor = scrapy.Field()
    author = scrapy.Field()
    copyRight = scrapy.Field()

class RssItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    language = scrapy.Field()
    pubDate = scrapy.Field(serializer=rfc822_date)
    guid = scrapy.Field()
    enc_url = scrapy.Field()
    enc_length = scrapy.Field()
    enc_type = scrapy.Field()
