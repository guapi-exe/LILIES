import datetime
import json

from nonebot.message import event_postprocessor, handle_event, event_preprocessor
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot import on_command, logger
from ..libs import day_used
from ..utils.redisdata import redis_storage, get_redis_data, redis_storage_cover

clear = on_command("clear", aliases={"清除"}, priority=10, block=True)


@event_postprocessor
async def record_recv_msg(event: MessageEvent):
    user = event.dict()["author"]["id"]
    await update_chatrecorder(user)


async def update_chatrecorder(uuid: str):
    global DAU, chat_recorder_json
    today = datetime.date.today()
    chat_recorder = get_redis_data("chat_recorder")
    chat_recorder_json = json.loads(chat_recorder)
    if "times" not in chat_recorder_json:
        chat_recorder_json["times"] = [today]
    if chat_recorder is not None:
        if chat_recorder_json["month_dau"] is None or chat_recorder_json["month_messages"] is None:  # 数据损坏 强行写入新数据重试
            all_used = day_used(
                today=today,
                times=[today],
                dau=1,
                month_dau=[1],
                day_messages=1,
                month_messages=[1]
            )
            logger.info(all_used)
            redis_storage_cover("chat_recorder", all_used.json())
        if str(today) == chat_recorder_json["today"]:
            redis_storage("Used_today", [uuid])
        else:
            redis_storage_cover("Used_today", [uuid])
            if len(chat_recorder_json["month_dau"]) >= 30:
                del chat_recorder_json["times"][0]
                del chat_recorder_json["month_dau"][0]
                del chat_recorder_json["month_messages"][0]
            if "times" not in chat_recorder_json:
                chat_recorder_json["times"] = [today]
            else:
                chat_recorder_json["times"].append(today)
            chat_recorder_json["month_dau"].append(1)
            chat_recorder_json["month_messages"].append(1)
            chat_recorder_json["day_messages"] = 0
            logger.info(chat_recorder_json)

    today_users = get_redis_data("Used_today")
    if today_users is not None:
        DAU = len(today_users)
    else:
        DAU = 0
    if chat_recorder is None:
        all_used = day_used(
            today=datetime.date.today(),
            times=[datetime.date.today()],
            dau=1,
            month_dau=[1],
            day_messages=1,
            month_messages=[1]
        )
        logger.info(all_used)
        redis_storage_cover("chat_recorder", all_used.json())
    else:
        chat_recorder_json["month_dau"][-1] = DAU
        chat_recorder_json["day_messages"] = chat_recorder_json["day_messages"] + 1
        chat_recorder_json["month_messages"][-1] = chat_recorder_json["month_messages"][-1] + 1
        all_used = day_used(
            today=datetime.date.today(),
            times=chat_recorder_json["times"],
            dau=DAU,
            month_dau=chat_recorder_json["month_dau"],
            day_messages=chat_recorder_json["day_messages"],
            month_messages=chat_recorder_json["month_messages"]
        )
        logger.info(all_used)
        redis_storage_cover("chat_recorder", all_used.json())


@clear.handle()
async def clear_chatrecorder():
    all_used = day_used(
        today=datetime.date.today(),
        times=[datetime.date.today()],
        dau=1,
        month_dau=[1],
        day_messages=1,
        month_messages=[1]
    )
    logger.info(all_used)
    redis_storage_cover("chat_recorder", all_used.json())
