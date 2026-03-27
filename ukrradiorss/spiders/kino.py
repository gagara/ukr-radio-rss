from ukrradiorss.spiders.ukrradio import UkrRadioSpider


class ViraVKinoSpider(UkrRadioSpider):
    name = "vira-v-kino"
    start_urls = ["https://ukr.radio/prog.html?id=1122"]
