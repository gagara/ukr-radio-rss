# ukr-radio-rss
Scraper of radio shows archive from [ukr.radio](https://ukr.radio)

---

[Scrapy](https://www.scrapy.org/)-based scraper which produces RSS-feed of radio shows archive.

## How to use

Install required dependencies
```
pip install -r requirements.txt
```

Run scraper for particular show. e.g.:
```
scrapy crawl <spider-name>
```

Each show has it's own spider. To get the list of available spider names:
```
grep "name = " ukrradiorss/spiders/*.py
```

RSS feed with the name `<spider-name>-feed.rss` produced in current directory. It can be directly imported to RSS reader/podcast App of your choice (if it supports local file import) or published somewhere.

Current repository contains all generated feeds in [this release](https://github.com/gagara/ukr-radio-rss/releases/tag/latest). Published RSS feeds can be directly imported to your RSS reader/podcast App, or you can search for them in https://podcastindex.org/.

## Automation

`bin/` directory contains scripts for automated RSS feed generation and upload to your github repo.

### Prerequisites
0. Edit `bin/release-feed.sh` and set correct values for:
```
GH_OWNER="<your_github_id>"
GH_REPO="<your_github_repo_name>"
GH_TAG="<your_repo_release>"
```
1. Create release in your github repository with tag `GH_TAG`
2. Generate github token with `contents:write` permission.
3. Export token to environment variable:
```
export GH_TOKEN="<your_token>"
```

### Run
```
bin/release-feed.sh -s <spider-name>
```
this will generate RSS feed for given show and upload it to assets of `GH_TAG` release in `GH_REPO` repository.

## Add new show from ukr.radio
Copy existing spider. e.g:
```
cp ukrradiorss/spiders/{meloman,another_show}.py
```

In new spider:
* change class name
* set new `name` of your choice
* provide correct URL

Example:
```
class AnotherShowSpider(UkrRadioSpider):
    name = "another-show"
    start_urls = ["https://ukr.radio/prog.html?id=123"]
```

Now you should be able to produce RSS feed of this show with:
```
scrapy crawl another-show
```
