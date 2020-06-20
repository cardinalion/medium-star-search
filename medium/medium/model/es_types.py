# -*- coding: utf-8 -*-

from elasticsearch_dsl import Document, Completion, Keyword, Text, Integer, Date
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["localhost"])


class ArticleType(Document):

    suggest = Completion()
    title = Text()
    url = Keyword()
    author = Text()
    publication = Text()
    date = Date()
    content = Text()
    tags = Text()
    claps = Integer()

    class Index:
        name = "medium"


if __name__ == "__main__":
    data = ArticleType.init()
    print(data)

