from pathlib import Path
from typing import Optional
from nonebot import on_command, get_driver
from nonebot.params import CommandArg
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
import urllib.parse
from ..utils.ppeteer import screenshot
config_ip = get_driver().config.dict()["guapi"]["ip"]

weather = on_command("天气", aliases={"weather", "查天气"}, priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@weather.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    if location := args.extract_plain_text():
        url_code = urllib.parse.quote(location)
        image = await screenshot(1920, 1080, f"https://www.msn.cn/zh-cn/weather/forecast/in-{url_code}",
                                 imgfile_path, None, True, 0)
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
                MessageMarkdownParams(key="text_start", values=[f"{location}天气"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:8099/api/files/{image_id}"])
            ]
        )
        if group_id is not None:
            await weather.finish(MessageSegment.markdown(mdmsg))
        else:
            await weather.finish(MessageSegment.image(f"http://{config_ip}:8099/api/files/{image_id}"))
    else:
        await weather.finish("请输入地名")
