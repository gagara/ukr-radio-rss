from ukrradiorss.spiders.ukrradio import UkrRadioSpider


class HodynaMelomanaSpider(UkrRadioSpider):
    name = "hodyna-melomana"
    start_urls = ["https://ukr.radio/prog.html?id=603"]
