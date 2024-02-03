from typing import Optional

from nonebot import on_command, logger
from nonebot.internal.params import Arg
from nonebot.params import Received, CommandArg
from nonebot.rule import to_me
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent

hello = on_command("debug", rule=to_me(), aliases={"测试"}, priority=10, block=True)


@hello.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    user_id = dict_event["author"]["id"]
    user_id_test = event.get_message
    logger.info(event.dict()["author"]["id"])
    logger.info(str(event.get_user_id))
    logger.info(f"uuid:{user_id_test}")
    message = dict_event["content"]
    await hello.send(event.json())
    if group_id is not None:
        await hello.send("群")
    else:
        await hello.send("频道")
    await hello.finish("guapi")
