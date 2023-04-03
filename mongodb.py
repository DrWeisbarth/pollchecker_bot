import os
from datetime import datetime

import pymongo


def get_collection() -> pymongo.collection:
    return pymongo.MongoClient(os.getenv("MONGO_DB_CONNECTION_STRING")).get_database("poll_checker_bot").get_collection(
        "user_data")


def is_setting_list(id: str) -> bool:
    user_data = get_collection().find_one({"userid": id})
    return user_data and user_data["is_setting_list"]


def set_setting_list(id: str, value: bool) -> None:
    if not get_collection().find_one_and_update({"userid": id}, {'$set': {"is_setting_list": value, "timestamp_setting_list": datetime.now().timestamp()}},
                                                return_document=pymongo.ReturnDocument.AFTER):
        get_collection().insert_one({
            "userid": id,
            "is_setting_list": value,
            "timestamp_setting_list": datetime.now().timestamp(),
            "list": None
        })


def has_list(id: str) -> bool:
    user_data = get_collection().find_one({"userid": id})
    if not user_data:
        return False
    if user_data["list"]:
        return True
    return False


def get_list(id: str) -> list:
    return get_collection().find_one({"userid": id})["list"]


def set_list(id: str, strings: list) -> None:
    set_setting_list(id, False)  # creates document if not found
    get_collection().find_one_and_update({"userid": id}, {'$set': {"list": strings}})
    print(get_collection().find_one({"userid": id}))
