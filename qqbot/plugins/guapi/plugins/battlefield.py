from pathlib import Path
from typing import Optional

import mcstatus
from nonebot import on_command, logger, get_driver
from nonebot.adapters.qq import MessageSegment
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from ..utils.ppeteer import screenshot
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from ..utils.redisdata import redis_storage, get_redis_data, redis_storage_cover, remove_redis_data
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent, permission

config_ip = get_driver().config.dict()["guapi"]["ip"]
config_port = get_driver().config.dict()["guapi"]["port"]
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))

bf_set = on_command("bf绑定", rule=to_me(),
                    priority=10, block=True)
bfv_info = on_command("bfv", rule=to_me(),
                      priority=10, block=True)
bf1_info = on_command("bf1", rule=to_me(),
                      priority=10, block=True)
bf2042_info = on_command("bf2042", rule=to_me(),
                         priority=10, block=True)


@bf_set.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    if bf_id := args.extract_plain_text():
        guild_id: Optional = None
        group_id: Optional = None
        dict_event = event.dict()
        if "group_id" in dict_event:
            group_id = dict_event["group_id"]
        if "guild_id" in dict_event:
            guild_id = dict_event["guild_id"]
        user_id = dict_event["author"]["id"]
        message = dict_event["content"]
        redis_storage_cover(f"bf{user_id}", bf_id)
        await bf_set.finish(f"{user_id}成功绑定于{bf_id}")


@bfv_info.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    user_id = dict_event["author"]["id"]
    bf_id = get_redis_data(f"bf{user_id}")
    command = args.extract_plain_text().strip()
    if command == "weapons" or command == "vehicles":
        if bf_id is None:
            bfv_info.finish("请在指令后键入玩家名或者使用/bf绑定 [账号]")
        image = await screenshot(780, 1080, f"http://127.0.0.1:{config_port}/{command}?name={bf_id}&type=bfv",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{bf_id}的bfv战绩"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"]),
            ]
        )
        if group_id is not None:
            await bfv_info.finish(Message(MessageSegment.markdown(mdmsg)))
        else:
            await bfv_info.finish(
                MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
    if command != "":
        bf_id = command
    if bf_id is not None:
        image = await screenshot(780, 1080, f"http://127.0.0.1:{config_port}/bfv?name={bf_id}",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{bf_id}的bfv战绩"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"]),
            ]
        )
        kbmsg = MessageKeyboard(
            content={
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "21",
                                "render_data": {
                                    "label": "bfv全部武器",
                                    "visited_label": "bfv全部武器"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bfv weapons"
                                }
                            },
                            {
                                "id": "22",
                                "render_data": {
                                    "label": "bfv全部载具",
                                    "visited_label": "bfv全部载具"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bfv vehicles"
                                }
                            }
                        ]
                    },
                    {
                        "buttons": [
                            {
                                "id": "23",
                                "render_data": {
                                    "label": "bf账号绑定",
                                    "visited_label": "bf账号绑定"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bf绑定"
                                }
                            }
                        ]
                    }
                ]
            }
        )
        if group_id is not None:
            await bfv_info.finish(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))
        else:
            await bfv_info.finish(
                MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
    else:
        bfv_info.finish("请在指令后键入玩家名或者使用/bf绑定 [账号]")


@bf1_info.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    user_id = dict_event["author"]["id"]
    bf_id = get_redis_data(f"bf{user_id}")
    command = args.extract_plain_text().strip()
    if command == "weapons" or command == "vehicles":
        if bf_id is None:
            bfv_info.finish("请在指令后键入玩家名或者使用/bf绑定 [账号]")
        image = await screenshot(780, 1080, f"http://127.0.0.1:{config_port}/{command}?name={bf_id}&type=bf1",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{bf_id}的bfv战绩"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"]),
            ]
        )
        if group_id is not None:
            await bfv_info.finish(Message(MessageSegment.markdown(mdmsg)))
        else:
            await bfv_info.finish(
                MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
    if command != "":
        bf_id = command
    if bf_id is not None:
        image = await screenshot(780, 1080, f"http://127.0.0.1:{config_port}/bf1?name={bf_id}",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{bf_id}的bf1战绩"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"]),
            ]
        )
        kbmsg = MessageKeyboard(
            content={
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "21",
                                "render_data": {
                                    "label": "bf1全部武器",
                                    "visited_label": "bf1全部武器"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bf1 weapons"
                                }
                            },
                            {
                                "id": "22",
                                "render_data": {
                                    "label": "bf1全部载具",
                                    "visited_label": "bf1全部载具"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bf1 vehicles"
                                }
                            }
                        ]
                    },
                    {
                        "buttons": [
                            {
                                "id": "23",
                                "render_data": {
                                    "label": "bf账号绑定",
                                    "visited_label": "bf账号绑定"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bf绑定"
                                }
                            }
                        ]
                    }
                ]
            }
        )
        if group_id is not None:
            await bfv_info.finish(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))
        else:
            await bfv_info.finish(
                MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
    else:
        bfv_info.finish("请在指令后键入玩家名或者使用/bf绑定 [账号]")


@bf2042_info.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    user_id = dict_event["author"]["id"]
    bf_id = get_redis_data(f"bf{user_id}")
    command = args.extract_plain_text().strip()
    if command == "weapons" or command == "vehicles":
        if bf_id is None:
            bfv_info.finish("请在指令后键入玩家名或者使用/bf绑定 [账号]")
        image = await screenshot(780, 1080, f"http://127.0.0.1:{config_port}/{command}?name={bf_id}&type=bf2042",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{bf_id}的bfv战绩"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"]),
            ]
        )
        if group_id is not None:
            await bfv_info.finish(Message(MessageSegment.markdown(mdmsg)))
        else:
            await bfv_info.finish(
                MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
    if command != "":
        bf_id = command
    if bf_id is not None:
        image = await screenshot(780, 1080, f"http://127.0.0.1:{config_port}/bf2042?name={bf_id}",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{bf_id}的bf2042战绩"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"]),
            ]
        )
        kbmsg = MessageKeyboard(
            content={
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "21",
                                "render_data": {
                                    "label": "bf2042全部武器",
                                    "visited_label": "bf2042全部武器"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bf2042 weapons"
                                }
                            },
                            {
                                "id": "22",
                                "render_data": {
                                    "label": "bf2042全部载具",
                                    "visited_label": "bf2042全部载具"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bf2042 vehicles"
                                }
                            }
                        ]
                    },
                    {
                        "buttons": [
                            {
                                "id": "23",
                                "render_data": {
                                    "label": "bf账号绑定",
                                    "visited_label": "bf账号绑定"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                        "specify_role_ids": [
                                            "1",
                                            "2",
                                            "3"
                                        ]
                                    },
                                    "unsupport_tips": "兼容文本",
                                    "data": "/bf绑定"
                                }
                            }
                        ]
                    }
                ]
            }
        )
        if group_id is not None:
            await bfv_info.finish(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))
        else:
            await bfv_info.finish(
                MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
    else:
        bfv_info.finish("请在指令后键入玩家名或者使用/bf绑定 [账号]")
