# -*- coding: utf-8 -*-


class ElasticsearchPipeline(object):

    def process_item(self, item, spider):

        item.save_to_es()

        return item
