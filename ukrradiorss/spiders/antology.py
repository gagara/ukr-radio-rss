from ukrradiorss.spiders.ukrradio import UkrRadioSpider


class AntologiyaUkrAlbomSpider(UkrRadioSpider):
    name = "antologiya-ukr-albom"
    start_urls = ["https://ukr.radio/prog.html?id=604"]
