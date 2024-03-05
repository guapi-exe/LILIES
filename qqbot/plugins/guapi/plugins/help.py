from typing import Optional

from nonebot import on_command, logger, get_driver
from nonebot.internal.params import Arg
from nonebot.params import Received
from nonebot.rule import to_me
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
config_ip = get_driver().config.dict()["guapi"]["ip"]
config_port = get_driver().config.dict()["guapi"]["port"]

help = on_command("help", rule=to_me(), aliases={"帮助"}, priority=10, block=True)
afd = on_command("afd", rule=to_me(), aliases={"爱发电"}, priority=10, block=True)


@afd.handle()
async def handle_function(event: Event = MessageEvent()):
    mdmsg = MessageMarkdown(
        custom_template_id="102071975_1702460123",
        params=[
            MessageMarkdownParams(key="text_start", values=[f"喂口饭吃"]),
            MessageMarkdownParams(key="img_dec", values=[f"img #750px #1028px"]),
            MessageMarkdownParams(key="img_url",
                                  values=[f"http://{config_ip}:{config_port}/static/img/afdian-guapi_exe.jpg"]),
        ]
    )
    await afd.finish(MessageSegment.markdown(mdmsg))


@help.handle()
async def handle_function(event: Event = MessageEvent()):
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    user_id = dict_event["author"]["id"]
    message = dict_event["content"]

    mdmsg = MessageMarkdown(
        custom_template_id="102071975_1702460123",
        params=[
            MessageMarkdownParams(key="text_start", values=[f"功能帮助:基于nonebot2的多功能机器人"]),
            MessageMarkdownParams(key="text_end", values=[f"成分复杂"])
        ]
    )
    kbmsg = MessageKeyboard(
        content={
            "rows": [
                {
                    "buttons": [
                        {
                            "id": "1",
                            "render_data": {
                                "label": "服务器状态",
                                "visited_label": "服务器状态"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/服务器状态"
                            }
                        },
                        {
                            "id": "9",
                            "render_data": {
                                "label": "设置群MC服务器",
                                "visited_label": "设置群MC服务器"
                            },
                            "action": {
                                "type": 2,
                                "permission": {
                                    "type": 1,
                                    "specify_role_ids": [
                                        "1",
                                        "2",
                                        "3"
                                    ]
                                },
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/设置群服务器"
                            }
                        },
                        {
                            "id": "2",
                            "render_data": {
                                "label": "机器人状态",
                                "visited_label": "机器人状态"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/机器人状态"
                            }
                        }
                    ]
                },
                {
                    "buttons": [
                        {
                            "id": "17",
                            "render_data": {
                                "label": "⭕角色面板",
                                "visited_label": "⭕角色面板"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/面板 "
                            }
                        },
                        {
                            "id": "18",
                            "render_data": {
                                "label": "⭕uuid绑定",
                                "visited_label": "⭕uuid绑定"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/面板 绑定"
                            }
                        }
                        ,
                        {
                            "id": "19",
                            "render_data": {
                                "label": "⭕队伍伤害估算",
                                "visited_label": "⭕队伍伤害估算"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/队伍伤害"
                            }
                        }
                    ]
                },
                {
                    "buttons": [
                        {
                            "id": "3",
                            "render_data": {
                                "label": "MC百科",
                                "visited_label": "MC百科"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/MC"
                            }
                        }, {
                            "id": "4",
                            "render_data": {
                                "label": "MDT-WIKI",
                                "visited_label": "MDT-WIKI"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/像素工厂"
                            }
                        }, {
                            "id": "5",
                            "render_data": {
                                "label": "hypixel信息",
                                "visited_label": "hypixel信息"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/hyp"
                            }
                        }
                    ]
                },
                {
                    "buttons": [
                        {
                            "id": "6",
                            "render_data": {
                                "label": "天气",
                                "visited_label": "天气"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/天气"
                            }
                        }, {
                            "id": "7",
                            "render_data": {
                                "label": "随机图片",
                                "visited_label": "随机图片"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/随机图片"
                            }
                        }
                    ]
                },
                {
                    "buttons": [
                        {
                            "id": "8",
                            "render_data": {
                                "label": "📅 签到",
                                "visited_label": "📅 签到"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/签到"
                            }
                        },
                        {
                            "id": "11",
                            "render_data": {
                                "label": "赞助一下",
                                "visited_label": "赞助一下"
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
                                "click_limit": 10,
                                "unsupport_tips": "兼容文本",
                                "data": "/afd"
                            }
                        }
                    ]
                }
            ]
        }
    )
    if group_id is not None:
        await help.finish(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))
    else:
        await help.finish(
            f"功能列表:\n/服务器状态 -查看Mc和Mdt服务器状态\n/机器人状态 -查看机器人状态和运行服务器状态\n/MDT [参数] -查看Mdt-wiki\n/随机二次元 "
            f"-随机图片\n/天气 [地点] -查看天气\n/MC [参数] -查看Mc百科")
