# -*- coding:utf-8 -*-
from pymongo import MongoClient


class MongoUtil(object):
    # 使用示例
    """
    from algo_database_utils.mongo_util import MongoUtil

    MONGODB_CRAWLER = {
    "url": "mongodb://qzd_algo_user_ro:c0NIG3j8mwODTfY6JBqn@data-crawler-mongo-dev.qizhidao.net:31017/data_crawler_db"
    }

    mongo_util = MongoUtil(MONGODB_CRAWLER)
    result = mongo_util.find_one(collection, uuid)
    """

    def __init__(self, config, read_preference="secondaryPreferred"):
        host = config.get("url")
        database = host.split('/')[-1]
        self.conn = MongoClient(host=host, readPreference=read_preference)
        self.mongo = self.conn.get_database(database)
        self.collection = None

    def close(self):
        return self.conn.close()

    def set_collection(self, name):
        self.collection = self.conn.get_collection(name)

    def insert_one(self, colletion_name, record):
        self.db.get_collection(colletion_name).insert_one(record)

    def delete_all(self, colletion_name):
        self.db.get_collection(colletion_name).delete_many({})

    def aggregate(self):
        return self.db.get_collection("Newss").aggregate([{"$sample": {"size": 1}}])

    def delete(self, colletion_name, filter):
        self.db.get_collection(colletion_name).delete_many(filter)

    def find_all_sort(self, colletion_name, query=None):
        records = self.db.get_collection(colletion_name).find(query)
        return records

    def find_all_sort_sort_limit(self, colletion_name):
        records = self.db.get_collection(colletion_name).find().sort("grade", pymongo.DESCENDING).limit(5)
        return records

    def find(self, colletion_name, query=None, ref_query=None):
        records = self.db.get_collection(colletion_name).find(query, ref_query)
        return records

    def find_one(self, colletion_name, query, ref_query=None):
        try:
            records = self.db.get_collection(colletion_name).find_one(query, ref_query)
        except Exception:
            logger.error(traceback.format_exec())
            records = {}
        self.close()
        return records

    def count_filter(self, colletion_name, query):
        return self.db.get_collection(colletion_name).count(query)

    def find_sort_by_asc(self, colletion_name, query, ref_query, sort_key):
        records = self.db.get_collection(colletion_name).find(query, ref_query).sort(sort_key, pymongo.ASCENDING)
        return records

    def find_sort_by_asc_with_limit(self, colletion_name, query, sort_key, limit=5):
        records = self.db.get_collection(colletion_name).find(query, None).sort(sort_key, pymongo.ASCENDING).limit(
            limit)
        return records

    def search(self, colletion_name, query=None, page=0, ref_query=None):
        records = self.db.get_collection(colletion_name).find(query, ref_query).sort([("article_time", -1)]).skip(
            page).limit(5)
        return records

    def find_sort_by_desc_with_limit(self, colletion_name, query, ref_query, sort_key, limit=100):
        records = self.db.get_collection(colletion_name).find(query, ref_query).sort(sort_key, pymongo.ASCENDING).limit(
            limit)
        return records

    def find_sort_by_desc(self, colletion_name, query, ref_query, sort_key):
        records = self.db.get_collection(colletion_name).find(query, ref_query).sort(sort_key, pymongo.DESCENDING)
        return records

    def update_one(self, colletion_name, query, update):
        self.db.get_collection(colletion_name).update_one(query, {"$set": update})

    def find_one_and_update(self, colletion_name, query, update):
        self.db.get_collection(colletion_name).update_one(query, update, upsert=True)

    def show_collections(self):
        return self.db.collection_names()

    def find_in_hours(self, colletion_name):
        return self.db.get_collection(colletion_name).find(
            ({"article_time": {"$gte": datetime(2016, 9, 23, 22), "$lt": datetime(2019, 11, 24, 22)}}))
