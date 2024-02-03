import redis
from typing import Optional
from nonebot import logger
from pydantic import BaseModel
from redis import Redis

redis_obj: Optional[Redis] = None


def init_redis():
    global redis_obj
    if redis_obj is None:
        red = redis.Redis(host='localhost', port=6379, decode_responses=True)  # 创建连接对象
        return red
    else:
        return redis_obj


def redis_storage_cover(key: str, data: any):
    global redis_obj
    if redis_obj is None:
        redis_obj = init_redis()
    if type(data) == list:
        redis_obj.delete(key)  # 先清除原来的元素
        for list_data in data:
            redis_obj.sadd(key, str(list_data))
    else:
        str_data = str(data)  # 除了list其他全部强制转换为str set存储
        redis_obj.set(key, str_data)


def redis_storage(key: str, data: any):
    global redis_obj
    if redis_obj is None:
        redis_obj = init_redis()
    if type(data) == list:
        for list_data in data:
            if type(list_data) == dict:
                redis_obj.zadd(key, list_data)
            else:
                redis_obj.sadd(key, str(list_data))
    else:
        return None  # 不支持除了list以为的


def get_redis_data(key: str):
    global redis_obj
    if redis_obj is None:
        redis_obj = init_redis()
    key_type = redis_obj.type(key)
    if key_type == 'string':
        return redis_obj.get(key)
    elif key_type == 'list':
        return redis_obj.lrange(key, 0, -1)
    elif key_type == 'set':
        return redis_obj.smembers(key)
    elif key_type == 'hash':
        return redis_obj.hgetall(key)
    elif key_type == 'zset':
        return redis_obj.zrange(key, 0, -1, withscores=True)
    else:
        return None


def remove_redis_data(key: str, data: any):
    global redis_obj
    if redis_obj is None:
        redis_obj = init_redis()
    try:
        redis_obj.srem(key, data)
        return True
    except Exception as e:
        logger.error(f"redis_del{e}")
        return False
