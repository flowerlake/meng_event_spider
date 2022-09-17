import scrapy, time
from scrapy.spiders import CrawlSpider
from mengEventProject.items import ArticleItem
import random


class stupidSpider(CrawlSpider):
    name = "stupidSpider"

    allowed_domain = []

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        with open("data/articleLinks3.txt", "r", encoding="utf-8") as f:
            self.urls = f.readlines()
        self.urls = [i.strip() for i in self.urls]
        # print(self.urls)
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        self.xpaths = {
            "www.aljazeera.com": {
                "title": "//div[@class='article-heading']/h1[@class='post-title']/text()",
                "body": "//div[@class='article-p-wrapper']",
                "publish_time": "//time[@class='timeagofunction']/text()"
            },
            "www.nbcnews.com": {
                "title": "//div[@class='articleHero___37q3K']/h1[c@class='headline___CuovH f8 f9-m fw3 mb3 mt0 founders-cond lh-none f10-xl']/text()",
                "body": "//div[@class='body___2BbXy publico-txt f4 f5-m lh-copy gray-100']",
                "publish_time": "//time[@class='relative z-1']/text()"
            },
            "www.cbsnews.com": {
                "title": "//header[@class='content__header  content__header--no-promo ']/h1/text()",
                "body": "//section[@data-page='1']",
                "publish_time": "//time/text()"
            },
            "www.bbc.co.uk": {
                "title": "//div[@class='story-body']/h1/text()",
                "body": "//div[@property='articleBody']",
                "publish_time": "//div[@class='mini-info-list-wrap']/ul/li/div/text()"
            },
            "uk.reuters.com": {
                "title": "//div[@class='ArticleHeader_content-container']/h1[@class='ArticleHeader_headline']/text()",
                "body": "//div[@class='StandardArticleBody_body']",
                "publish_time": "//div[@class='ArticleHeader_content-container']/div[@class='ArticleHeader_date']/text()"
            },
            "www.reuters.com": {
                "title": "//div[@class='ArticleHeader_content-container']/h1[@class='ArticleHeader_headline']/text()",
                "body": "//div[@class='StandardArticleBody_body']",
                "publish_time": "//div[@class='ArticleHeader_content-container']/div[@class='ArticleHeader_date']/text()"
            },
            "abcnews.go.com": {
                "title": "//article[@class='StoryPage__article--3uYE7']/header/h1/text()",
                "body": "//div[@class='StoryPage__content--3u3Oe']/div/div[@class='StoryBody__main--1VIBe fonts__tiemposTextRegular--1u6HI']",
                "publish_time": "//span[@class='StoryPage__date--UmODz']/text()"
            },
            "www.foxnews.com": {
                "title": "//header[@class='article-header']/h1/text()",
                "body": "//div[@class='article-body']",
                "publish_time": "//header[@class='article-header']/div/div[@class='article-date']/time/text()"
            },
            "edition.cnn.com": {
                "title": "",
                "body": "",
                "publish_time": ""
            },
            "www.npr.org": {
                "title": "//div[@class='storytitle']/h1/text()",
                "body": "//div[@id='storytext']",
                "publish_time": "//div[@class='dateblock']/time/span[@class='date']/text()"
            },
            "www.nytimes.com": {
                "title": "//span[@class='balancedHeadline']/text()",
                "body": "//section[@name='articleBody']",
                "publish_time": "//time[@class='css-qddhf4 e16638kd0']/text()"

            },
            "mp.weixin.qq.com": {
                "title": "//div[@id='img-content']/h2/text()",
                "author": "//div[@id='img-content']/div/span/a/text()",
                "publish_time": "//div[@id='img-content']/div/em[@id='publish_time']/text()",
                "body": "//div[@id='img-content']/div[@class='rich_media_content ']"
            }
        }

        with open("data/available_proxy.txt", "r", encoding="utf-8") as f:
            self.proxies = f.readlines()

        self.proxies = [eval(i.strip("\n")) for i in self.proxies]

    def start_requests(self):
        start_url = self.urls

        for url in start_url:
            yield scrapy.Request(url, callback=self.parse_body, dont_filter=False, headers=self.header)
            # meta={"proxy": self.proxies[random.randint(0, len(self.proxies))]["https"]})

    def parse_body(self, response):
        article = ArticleItem()

        url = str(response).split('/')[2]

        try:
            title = response.xpath(self.xpaths[url]["title"]).extract()[0]
            article["title"] = title.strip()
            article["author"] = response.xpath(self.xpaths[url]["author"]).extract()[0].strip()
            data = response.xpath(self.xpaths[url]["body"])
            article["body"] = data.xpath("string(.)").extract()[0].strip()
            # article["publish_time"] = response.xpath(self.xpaths[url]["publish_time"]).extract()[0]
            print(article["title"] + "\n")
        except Exception as e:
            print(e)

        time.sleep(3)

        return article

    def test(self):
        pass

# if __name__ == "__main__":
#     a = stupidSpider()
#     a.test()
