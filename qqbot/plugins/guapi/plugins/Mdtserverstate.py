from pathlib import Path
from typing import Optional
from nonebot import on_command, logger, get_driver
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from ..utils.ppeteer import screenshot
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent, permission
from ..utils.redisdata import redis_storage_cover, get_redis_data
config_ip = get_driver().config.dict()["guapi"]["ip"]
config_port = get_driver().config.dict()["guapi"]["port"]

imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))

look_server_state = on_command("服务器状态", rule=to_me(), priority=10)
set_mdt_server = on_command("设置群MDT服务器", rule=to_me(),
                            priority=10, block=True)


@set_mdt_server.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    if server_ip := args.extract_plain_text():
        guild_id: Optional = None
        group_id: Optional = None
        dict_event = event.dict()
        if "group_id" in dict_event:
            group_id = dict_event["group_id"]
        if "guild_id" in dict_event:
            guild_id = dict_event["guild_id"]
        user_id = dict_event["author"]["id"]
        message = dict_event["content"]
        redis_storage_cover(f"MDT{group_id}", server_ip)
        await set_mdt_server.finish(f"设置成功")


@look_server_state.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    server_ip = get_redis_data(f"MDT{group_id}")
    command = args.extract_plain_text().strip()

    if server_ip is None:
        await look_server_state.finish()
    else:
        if command != "":
            server_ip = command
        image = await screenshot(1260, 1080, f"https://www.mindustry.top/server",
                                 imgfile_path, None, True, 0)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"服务器状态信息"]),
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
                                "id": "12",
                                "render_data": {
                                    "label": "服务器状态 all",
                                    "visited_label": "服务器状态 all"
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
                                    "data": "/服务器状态 all"
                                }
                            }
                        ]
                    }
                ]
            }
        )
        if group_id is not None:
            await look_server_state.finish(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))
        else:
            await look_server_state.finish(MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
