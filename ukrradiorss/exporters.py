from datetime import datetime
from xml.sax.xmlreader import AttributesImpl

from scrapy.exporters import XmlItemExporter


class RssExporter(XmlItemExporter):
    def __init__(self, *args, **kwargs):
        self.channel_element = 'channel'
        self.item_element = 'item'
        self.date_format = '%a, %d %b %Y %H:%M:%S %z'

        self.title = kwargs.pop('title')
        self.link = kwargs.pop('link')
        self.description = kwargs.pop('description')
        self.image = kwargs.pop('image')
        self.language = kwargs.pop('language', 'en-us')
        self.pubDate = kwargs.pop('pubDate')
        self.lastBuildDate = kwargs.pop('lastBuildDate')
        self.docs = "https://www.rssboard.org/rss-specification"
        self.generator = "scrapy"
        self.managingEditor = kwargs.pop('managingEditor')
        self.author = kwargs.pop('author')
        self.copyRight = kwargs.pop('copyRight')

        kwargs['root_element'] = 'rss'
        kwargs['item_element'] = 'item'
        super(RssExporter, self).__init__(*args, **kwargs)
        self.indent = 4

    def start_exporting(self):
        self.xg.startDocument()
        self.xg.startElement(self.root_element, AttributesImpl({
            'version': '2.0',
            'xmlns:atom': 'http://www.w3.org/2005/Atom'
        }))
        self._beautify_newline()
        self._beautify_indent(1)
        self.xg.startElement(self.channel_element, AttributesImpl({}))
        self._beautify_newline()

        self._export_xml_field('title', self.title, 2)
        self._export_xml_field('link', self.link, 2)
        self._export_xml_field('description', self.description, 2)
        if self.image:
            self._beautify_indent(2)
            self.xg.startElement("image", AttributesImpl({}))
            self._beautify_newline()
            self._export_xml_field('url', self.image, 3)
            self._export_xml_field('title', self.title, 3)
            self._export_xml_field('link', self.link, 3)
            self._beautify_indent(2)
            self.xg.endElement('image')
            self._beautify_newline()

        if self.pubDate:
            self._export_xml_field('pubDate', self.pubDate, 2)
        self._export_xml_field('lastBuildDate', self.lastBuildDate if self.lastBuildDate else datetime.now(), 2)
        self._export_xml_field('docs', self.docs, 2)
        self._export_xml_field('generator', self.generator, 2)
        if self.managingEditor:
            self._export_xml_field('managingEditor', self.managingEditor, 2)
        if self.author:
            self._export_xml_field('author', self.author, 2)
        if self.copyRight:
            self._export_xml_field('copyright', self.copyRight, 2)
        self._beautify_indent(2)
        self.xg.startElement('atom:link', AttributesImpl({
            'href': 'https://www.rssboard.org/files/sample-rss-2.xml',
            'rel': 'self',
            'type': 'application/rss+xml'
        }))
        self.xg.endElement('atom:link')
        self._beautify_newline()

    def export_item(self, item):
        self._beautify_indent(2)
        self.xg.startElement(self.item_element, AttributesImpl({}))
        self._beautify_newline()

        if "title" in item:
            self._export_xml_field("title", item.get("title"), 3)
        if "link" in item:
            self._export_xml_field("link", item.get("link"), 3)
        if "description" in item:
            self._export_xml_field("description", item.get("description"), 3)
        if "language" in item:
            self._export_xml_field("language", item.get("language"), 3)
        if "pubDate" in item:
            self._export_xml_field("pubDate", item.get("pubDate"), 3)
        if "guid" in item:
            self._export_xml_field("guid", item.get("guid"), 3)
        if "enc_url" in item:
            self._beautify_indent(3)
            self.xg.startElement('enclosure', AttributesImpl({
                'url': item.get("enc_url"),
                'length': item.get("enc_length"),
                'type': item.get("enc_type")
            }))
            self.xg.endElement('enclosure')
            self._beautify_newline()
        self._beautify_indent(2)
        self.xg.endElement(self.item_element)
        self._beautify_newline()

    def finish_exporting(self):
        self._beautify_indent(1)
        self.xg.endElement(self.channel_element)
        self._beautify_newline()
        self.xg.endElement(self.root_element)
        self.xg.endDocument()
