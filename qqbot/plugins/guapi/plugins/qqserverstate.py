from pathlib import Path
from typing import Optional

from nonebot import on_command, get_driver
from nonebot.rule import to_me
from nonebot.adapters.qq import MessageSegment
from ..utils.ppeteer import screenshot
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams

config_ip = get_driver().config.dict()["guapi"]["ip"]

serverstate = on_command("机器人状态", rule=to_me(), aliases={"状态"}, priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@serverstate.handle()
async def handle_function(event: Event = MessageEvent()):
    image = await screenshot(1920, 1080, f"http://127.0.0.1:8099/index",
                             imgfile_path, None, True, 5)
    address = image[1]
    parts = address.split("/")
    image_id = parts[-1]
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    mdmsg = MessageMarkdown(
        custom_template_id="102071975_1702460123",
        params=[
            MessageMarkdownParams(key="text_start", values=[f"机器人状态"]),
            MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
            MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:8099/api/files/{image_id}"])
        ]
    )
    if group_id is not None:
        await serverstate.finish(MessageSegment.markdown(mdmsg))
    else:
        await serverstate.finish(MessageSegment.image(f"http://{config_ip}:8099/api/files/{image_id}"))
