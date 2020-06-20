from django.shortcuts import render
import json
from django.views.generic.base import View
from search.models import ArticleType
from django.http import HttpResponse
from elasticsearch import Elasticsearch
from datetime import datetime
import redis

client = Elasticsearch(hosts=["127.0.0.1"])
redis_cli = redis.StrictRedis()


class IndexView(View):
    # 首页
    def get(self, request):
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        topn_search = [search.decode() for search in topn_search]
        past_search = redis_cli.lrange('last_five_keywords', 0, -1)
        past_search = [search.decode() for search in past_search]
        return render(request, "index.html", {"topn_search": topn_search, "past_search": past_search})


class SearchSuggest(View):
    def get(self, request):
        key_words = request.GET.get('s', '')
        re_datas = []
        if key_words:
            s = ArticleType.search()
            s = s.suggest('my_suggest', key_words, completion={
                "field": "suggest", "fuzzy": {
                    "fuzziness": 2
                },
                "size": 10
            })
            response = s.execute()
            for match in response.suggest.my_suggest[0].options:
                re_datas.append(match._source["title"])
        return HttpResponse(json.dumps(re_datas), content_type="application/json")


class SearchView(View):
    """
    搜索视图，根据搜索词q和类型s_type返回搜索结果
    """
    def get(self, request):
        key_words = request.GET.get("q", "")

        redis_cli.zincrby("search_keywords_set", 1, key_words)
        topn_search = redis_cli.zrevrangebyscore("search_keywords_set", "+inf", "-inf", start=0, num=5)
        topn_search = [search.decode() for search in topn_search]

        redis_cli.lrem('last_five_keywords', 0, key_words)
        redis_cli.lpush('last_five_keywords', key_words)
        past_search = redis_cli.lrange('last_five_keywords', 0, -1)
        past_search = [search.decode() for search in past_search]
        if len(past_search) > 5:
            redis_cli.rpop('last_five_keywords')
            past_search = past_search[:5]
        print(past_search)

        page = request.GET.get("p", "1")
        try:
            page = int(page)
        except:
            page = 1

        start_time = datetime.now()
        response = client.search(
            index="medium",
            body={
                "query": {
                    "multi_match": {
                        "query": key_words,
                        "fields": ["tags", "title", "content"]
                    }
                },
                "from": (page-1)*10,
                "size": 10,
                "highlight": {
                    "pre_tags": ['<span class="keyWord">'],
                    "post_tags": ['</span>'],
                    "fields": {
                        "title": {},
                        "content": {},
                    }
                }
            }
        )
        end_time = datetime.now()
        last_seconds = (end_time-start_time).total_seconds()  # 搜索计时
        total_nums = response["hits"]["total"]["value"]
        if (page % 10) > 0:
            page_nums = int(total_nums/10) + 1
        else:
            page_nums = int(total_nums/10)
        hit_list = []
        for hit in response["hits"]["hits"]:
            hit_dict = {}
            if "title" in hit["highlight"]:
                hit_dict["title"] = "".join(hit["highlight"]["title"])
            else:
                hit_dict["title"] = hit["_source"]["title"]
            if "content" in hit["highlight"]:
                hit_dict["content"] = "".join(hit["highlight"]["content"])[:500]
                for i in range(len(hit_dict["content"])-1):
                    if hit_dict["content"][-i] == '>':
                        break
                    elif hit_dict["content"][-i] == '<':
                        hit_dict["content"] = hit_dict["content"][:-i-1]
                        break
                # print(hit_dict["content"])
            else:
                hit_dict["content"] = hit["_source"]["content"][:500]

            hit_dict["url"] = hit["_source"]["url"]
            hit_dict["published_date"] = (hit["_source"]["date"])[:10]
            hit_dict["score"] = hit["_score"]

            hit_list.append(hit_dict)

        medium_nums = (client.count(index="medium"))["count"]
        # print(past_search)
        return render(request, "result.html", {"page": page,
                                               "all_hits": hit_list,
                                               "key_words": key_words,
                                               "total_nums": total_nums,
                                               "page_nums": page_nums,
                                               "last_seconds": last_seconds,
                                               "past_search": past_search,
                                               "topn_search": topn_search,
                                               "medium_nums": medium_nums})
