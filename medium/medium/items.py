# -*- coding: utf-8 -*-

import scrapy
from medium.model.es_types import ArticleType
from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections
es = connections.create_connection(using=Elasticsearch('localhost'))  # connect to existed connection


def gen_suggests(index, info_tuple):
    used_words = set()
    suggests = []
    for texts, weight in info_tuple:
        new_words = set()
        if texts:
            analyzed_words = set()
            for text in texts:
                words = es.indices.analyze(index=index, body={"text": text})
                analyzed_words = analyzed_words.union(set([r["token"] for r in words["tokens"] if len(r["token"]) > 1]))
            new_words = new_words.union(analyzed_words - used_words)

        if new_words:
            suggests.append({"input": list(new_words), "weight": weight})
            used_words = used_words.union(new_words)

    return suggests


class ArticlesItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    publication = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    claps = scrapy.Field()

    def save_to_es(self):
        article = ArticleType()
        article.title = self['title']
        article.url = self["url"]
        article.author = self['author']
        article.publication = self['publication']
        article.date = self["date"]
        article.content = self["content"]
        article.tags = self["tags"]
        article.claps = self["claps"]
        article.suggest = gen_suggests("medium", (([article.title], 10), (article.tags, 3)))

        article.save()

        return

