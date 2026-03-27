from ukrradiorss.spiders.ukrradio import UkrRadioSpider


class KulturaVSLSpider(UkrRadioSpider):
    name = "kultura-z-vsl"
    start_urls = ["https://ukr.radio/prog.html?id=1195"]
