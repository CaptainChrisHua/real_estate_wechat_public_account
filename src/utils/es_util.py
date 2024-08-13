# -*- coding:utf-8 -*-
import json
import time
import traceback
from collections import deque
from math import ceil
from typing import List, Any

from elasticsearch import helpers
from elasticsearch.exceptions import RequestError
from elasticsearch_dsl import connections, Search
from requests import sessions
from requests.exceptions import ReadTimeout


class ParamException(Exception):

    def __init__(self, message):
        self.message = message


class ESUtil(object):
    # 使用示例
    """
    from algo_database_utils.es_util import ESUtil

    ES_BIGDATA = {
        'esHost': 'xxx',
        'esPass': 'xxx',
        'esPort': 9200,
        'esUser': 'xxx'
    }

    es_util = ESUtil(ES_BIGDATA)
    result = es_util.search(dsl)
    """

    def __init__(self, es_config: dict, index: str):
        # 创建es连接，默认使用Transport的连接池机制
        self.es = connections.create_connection(
            hosts=[f"{es_config['esHost']}:{es_config['esPort']}"],
            http_auth=(es_config['esUser'], es_config['esPass'])
        )
        self.index = index

    def search(self, dsl: dict, index=None):
        """
        es单条查询
        dsl: es查询语句
        """

        for i in range(3):  # es索引更新的时候会报 RequestError(400, 'index_closed_exception', 'closed')，重试3次
            try:
                res = self.es.search(body=dsl, index=index or self.index)
                return res
            except RequestError:
                database_logger.warning(f"ES请求{self.index}索引超时，重试中")
                time.sleep(0.5)
        else:
            raise RequestError(f"ES请求{self.index}索引连续3次超时，请稍后重试")

    def search_dsl(self, dsl: dict, index=None):
        for i in range(3):  # es索引更新的时候会报 RequestError(400, 'index_closed_exception', 'closed')，重试3次
            try:
                res = Search.from_dict(dsl).using(self.es).index(index).params(
                    request_timeout=300).execute(ignore_cache=True)
                return res
            except RequestError:
                database_logger.warning(f"ES请求{self.index}索引超时，重试中")
                time.sleep(0.5)
        else:
            raise RequestError(f"ES请求{self.index}索引连续3次超时，请稍后重试")

    def count(self, dsl, index=None):
        """
        es查询数量统计
        dsl: es查询语句
        """
        res = self.es.count(index=index or self.index, body=dsl).get("count", 0)
        return res

    def scroll_search(self, scroll_id: str, scroll: str):
        """
        es滚动查询
        """
        return self.es.scroll(scroll_id=scroll_id, scroll=scroll, request_timeout=300)

    def get_scroll_id(self, dsl: dict, scroll: str, index=None):
        """
        es滚动查询并获取scroll_id
        """
        return self.es.search(body=dsl, index=index or self.index, scroll=scroll)

    def update(self, data: List, refresh=None):
        """
        es批量更新
        data: 需要更新的数据列表，列表中元素是要更新的数据字典，eg:
        [{
            "_index": index,
            "_id": es_id,
            "_op_type": "update",
            "doc": {"field": "value"}
        }]
        """
        helpers.bulk(self.es, data, refresh=refresh)

    def es_mget(self, body, index=None):
        """
        批量查询
        """
        res = self.es.mget(body=body, index=index or self.index).get("docs")
        return res

    def analyze(self, word):
        """
        ik分词
        """
        body = {
            "analyzer": "ik_smart",
            "text": word
        }
        tokens = self.es.indices.analyze(body=body).get("tokens")
        token_words = list(map(lambda x: x.get("token"), tokens)) if tokens else []
        return token_words

    def analyze_all(self, word):
        """
        ik分词并组合成数组
        """
        body = {
            "analyzer": "ik_smart",
            "text": word
        }
        tokens = self.es.indices.analyze(body=body).get("tokens")
        token_words = list(map(lambda x: x.get("token"), tokens)) if tokens else []
        end_off = list(map(lambda x: x.get("end_offset"), tokens)) if tokens else []
        return_list = list(zip(end_off, token_words))
        return return_list

    def analyze_list(self, word_list):
        """
        ik分词数组并按顺序整理成二维数组：
        输入 ["木材加工和木、竹、藤、棕、草制品it", "地板"]
        输出 [['木材', '加工', '和', '木', '竹', '藤', '棕', '草', '制品'], ['地板']]
        """
        es_word_list = self.analyze_all(word_list)
        n_list = [len(item) for item in word_list]
        i, j = 0, 1
        while j < len(n_list):
            n_list[j] += n_list[i] + 1
            i += 1
            j += 1
        es_word_list = deque(es_word_list)
        return_list = []
        item = es_word_list.popleft()
        for num in n_list:
            temp_list = []
            while item and num >= item[0]:
                temp_list.append(item[1])
                if es_word_list:
                    item = es_word_list.popleft()
                else:
                    item = []
            return_list.append(temp_list)
        return return_list


class IPSBigDataApi(object):
    """
    大数据es查询接口
    """

    def __init__(self, ips_base_url, timeout=5):
        self.ips_base_url = ips_base_url
        self.time_out = timeout

    def _get_token(self):
        """
        获取es连接token
        """
        url = self.ips_base_url + f'/escommon/search/register'
        payload = {}
        headers = {}
        with sessions.Session() as session:
            try:
                rsp = session.request('GET', url, headers=headers, json=payload, timeout=self.time_out)
                if rsp.status_code == 200:
                    return rsp.json()
                else:
                    database_logger.error(
                        f"调用大数据ES register 接口失败，status_code={rsp.status_code}, \n text={rsp.text}")
                    return {}
            except (RequestError, ReadTimeout):
                database_logger.error(traceback.format_exc())
                return {}

    def _get_data_by_dsl(self, payload):
        """
        根据dsl查询es
        """
        url = self.ips_base_url + f'/escommon/search/admin/verify'
        headers = {'Content-Type': 'application/json'}
        with sessions.Session() as session:
            try:
                rsp = session.request('POST', url, headers=headers, json=payload, timeout=self.time_out)
                if rsp.status_code == 200:
                    return rsp.json()
                else:
                    database_logger.error(
                        f"调用大数据ES search 接口失败，status_code={rsp.status_code}, \n text={rsp.text}")
                    return {}
            except (RequestError, ReadTimeout):
                database_logger.error(traceback.format_exc())
                return {}

    def _get_data_by_scroll_id(self, payload):
        """
        根据dsl查询es
        """
        url = self.ips_base_url + f'/escommon/search/scroll'
        headers = {'Content-Type': 'application/json'}
        with sessions.Session() as session:
            try:
                rsp = session.request('POST', url, headers=headers, json=payload, timeout=self.time_out)
                if rsp.status_code == 200:
                    return rsp.json()
                else:
                    database_logger.error(
                        f"调用大数据ES scroll 接口失败，status_code={rsp.status_code}, \n text={rsp.text}")
                    return {}
            except (RequestError, ReadTimeout):
                database_logger.error(traceback.format_exc())
                return {}


class EsApiUtil(IPSBigDataApi):

    def __init__(self, env, service, short_name, redis_config, timeout=5):
        tmp = f'-{env}' if env in ('dev', 'test', 'pre') else ''
        if env == 'test':
            tmp = f'-nts'
        ips_base_url = f'http://ips-gateway{tmp}-lan.qizhidao.com'  # ips(大数据)环境
        super(EsApiUtil, self).__init__(ips_base_url, timeout)
        self.service_person = service
        self.token_key = f"{short_name}:{env}:TOKEN:BIGDATA_TOKEN"
        self.rds = RedisUtil(redis_config, decode_responses=False)

    # 获取大数据token
    def get_token(self, from_api=False):
        # 先去redis里面取没有再调用接口获取token再存入redis设置9小时过期时间(token失效是10小时)
        raw_token = self.rds.get(self.token_key)
        if raw_token and not from_api:
            token = json.loads(raw_token)
        else:
            token = self._get_token()
            self.rds.set(self.token_key, json.dumps(token, ensure_ascii=False))
            self.rds.expire(self.token_key, 32400)
        return token

    # 大数据接口查询带token
    def get_data(self, dsl, index, queryType=0, env=1, from_api=False) -> dict:
        """
        调用大数据es查询接口获取数据
        :param dsl
        :param index es索引
        :param queryType  查询类别 0-检索 1-聚合 2-检索+聚合 默认值为0
        :param env es环境 0-阿里云 1-混合云  默认值为1
        :param from_api 是否直接从api获取token
        """
        token = self.get_token(from_api=from_api)
        _payload = {
            "requestServiceAndPerson": self.service_person,
            "index": index,
            "queryType": queryType,  # 查询类别:0->检索 1->聚合 2->检索+聚合 默认值为0
            "struct": json.dumps(dsl, ensure_ascii=False),
            "token": token,
            "env": env  # 阿里云es:0,混合云es:1
        }
        query_data = self._get_data_by_dsl(payload=_payload)
        if query_data.get("code") != "0":
            query_data = self.get_data(dsl, index, queryType, env, from_api=True)
        return query_data

    def get_scroll_id(self, dsl, index, env=1, scroll: str = None):
        """
        调用大数据es查询接口获取 scroll_id
        :param dsl
        :param index es索引
        :param env es环境 0-阿里云 1-混合云  默认值为1
        :param scroll scroll过期时间
        :return 返回 scroll_id, total_size, query_data_party1
        """
        token = self.get_token()
        database_logger.debug(json.dumps(dsl, ensure_ascii=False))
        pathParam = f"?scroll={scroll}" if scroll else "?scroll=3m"
        payload = {
            "requestServiceAndPerson": self.service_person,
            "index": index,
            "queryType": 2,  # queryType必须为2才能拿到scroll_id
            "struct": json.dumps(dsl, ensure_ascii=False),
            "token": token,
            "env": env,  # 阿里云es:0,混合云es:1
            "pathParam": pathParam
        }
        query_data = self._get_data_by_dsl(payload=payload)
        if query_data:
            data = query_data.get("data")
            scroll_id = data["restResponse"]["_scroll_id"]
            total_size = data["totalSize"]
            hits = data["restResponse"]["hits"]["hits"]
            return scroll_id, total_size, hits
        else:
            return None, None, None

    def search_by_scroll_id(self, scroll_id: str = None, scroll: str = None, env: int = None) -> List[Any]:
        """
        根据scroll_id滚动查询
        :param env 环境 0：阿里云 1：混合云
        :param scroll_id 滚动查询id
        :param scroll scroll过期时间
        """
        if not env:
            database_logger.warning("传入环境类型。tips： 0-阿里云，1-混合云")
            return
        if not scroll_id:
            database_logger.warning("请传入 scroll_id!")
            return
        if not scroll:
            scroll = "3m"
        _payload = {
            "scroll": scroll,
            "scrollId": scroll_id,
            "env": env  # 阿里云es:0,混合云es:1
        }
        query_data = self._get_data_by_scroll_id(payload=_payload)
        try:
            query_data = query_data.get("data")
            query_data = query_data.get("restResponse")
        except Exception as e:
            database_logger.warning("获取scroll_id失败, text=%s", e)
            return None
        return query_data

    def search_all_by_scroll(self, dsl, index, queryType=2, env=1, expected_page_num=None,
                             scroll: str = None) -> list:
        """
        分页查询
        :param dsl
        :param index es索引
        :param queryType  查询类别 0-检索 1-聚合 2-检索+聚合 默认值为0
        :param env es环境 0-阿里云 1-混合云  默认值为1
        :param scroll scroll过期时间
        :return 返回 scroll_id, total_size, query_data_party1
        """
        result = []
        size = dsl.get('size', 1000)
        dsl["size"] = size
        scroll_id, total_size, query_data = self.get_scroll_id(dsl=dsl, index=index, queryType=queryType,
                                                               env=env, scroll=scroll)

        database_logger.debug('查询数据量: total=%s, size=%s, scroll_id=%s', total_size, size, scroll_id)
        if not scroll_id or not total_size or not query_data:
            database_logger.warning('查询数据量: total=%s, size=%s, scroll_id=%s', total_size, size, scroll_id)
            return []

        page_num = ceil(total_size / size)
        if expected_page_num is not None and expected_page_num != 0:
            page_num = int(min(page_num, expected_page_num))

        result.extend(query_data)

        database_logger.debug("ES Scroll Page 1/%s ------------------ %f%%", page_num,
                              result.__len__() * 1.0 / min(page_num * size, total_size) * 100)
        try:
            for i in range(0, page_num - 1):
                scroll_result = self.search_by_scroll_id(scroll_id=scroll_id, scroll=scroll, env=env)
                if not scroll_result:
                    continue
                result.extend(scroll_result.get("hits").get("hits"))
                database_logger.debug("ES Scroll Page %s/%s ------------------ %f%%", i + 2, page_num,
                                      result.__len__() * 1.0 / min(page_num * size, total_size) * 100)

            database_logger.debug("查询完毕！")

        finally:
            self.clear_scroll(scroll_id)  # 清除scroll_id: 解决search.max_open_scroll_context超过限制的问题
        return result

    def clear_scroll(self, scroll_id):
        # 等待es提供clear_scroll接口
        pass
