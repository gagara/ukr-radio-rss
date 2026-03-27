from ukrradiorss.spiders.ukrradio import UkrRadioSpider


class MuzychniIstoriiSpider(UkrRadioSpider):
    name = "muzychni-istorii"
    start_urls = ["https://ukr.radio/prog.html?id=665"]
