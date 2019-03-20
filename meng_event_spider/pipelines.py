# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from mengEventProject.models import db_connect, create_news_table, Article
from mengEventProject.spiders import stupidSpider


class PromengeventPipeline(object):
    def process_item(self, item, spider):
        return item


class SaveFilePipline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        # 将抓取到的GoogleNews先存到文件中
        # with open("data/originalPage.html","w",encoding='utf-8') as f:
        #     f.write(item["originalPage"])

        with open("data/links.txt", 'a+', encoding='utf-8') as f:
            f.writelines(line + '\n' for line in item['newsLinks'])


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class ArticleDataBasePipeline(object):
    """保存文章到数据库"""

    def __init__(self):
        engine = db_connect()
        create_news_table(engine)
        self.Session = sessionmaker(bind=engine)

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        a = Article(url=item["url"],
                    title=item["title"].encode("utf-8"),
                    publish_time=item["publish_time"].encode("utf-8"),
                    body=item["body"].encode("utf-8"))
        with session_scope(self.Session) as session:
            session.add(a)

    def close_spider(self, spider):
        pass


class ArticleFilePipline(object):

    def __init__(self):
        pass

    def open_spider(self, spider):
        """This method is called when the spider is opened."""
        pass

    def process_item(self, item, spider):
        with open("data/WeChatArticles/" + item["title"] + ".txt", "w", encoding="utf-8") as f:
            f.write(item["title"] + "\n" + item['author'] + "\n" + item["body"])

    def close_spider(self, spider):
        pass
