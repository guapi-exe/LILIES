from pathlib import Path
from typing import Optional

from nonebot import on_command, logger, get_driver
from nonebot.internal.params import Arg
from nonebot.params import Received, CommandArg
from nonebot.rule import to_me
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent

from ..utils.ppeteer import screenshot
from ..utils.redisdata import redis_storage_cover, get_redis_data
config_ip = get_driver().config.dict()["guapi"]["ip"]

hyp = on_command("hyp", rule=to_me(), aliases={"hypixel"}, priority=10)
hyp_api = on_command("update_hyp_apikey", rule=to_me(), aliases={"更新api"}, priority=10, block=True)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@hyp.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    if name := args.extract_plain_text():
        api_key = get_redis_data("hyp_api_key")
        guild_id: Optional = None
        group_id: Optional = None
        dict_event = event.dict()
        if "group_id" in dict_event:
            group_id = dict_event["group_id"]
        if "guild_id" in dict_event:
            guild_id = dict_event["guild_id"]
        if api_key is not None:
            image = await screenshot(1920, 1080, f"http://127.0.0.1:8099/hypinfo?name={name}",
                                     imgfile_path, None, True, 4)
            address = image[1]
            parts = address.split("/")
            image_id = parts[-1]
            mdmsg = MessageMarkdown(
                custom_template_id="102071975_1702460123",
                params=[
                    MessageMarkdownParams(key="text_start", values=[f"{name}的hypixel信息"]),
                    MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                    MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:8099/api/files/{image_id}"])
                ]
            )
            if group_id is not None:
                await hyp.finish(MessageSegment.markdown(mdmsg))
            else:
                await hyp.finish(MessageSegment.image(f"http://{config_ip}/api/files/{image_id}"))
        else:
            await hyp.finish("apikey不可用")
    else:
        await hyp.finish("后请跟玩家名")


@hyp_api.handle()
async def handle_function(args: Message = CommandArg()):
    if key := args.extract_plain_text():
        redis_storage_cover("hyp_api_key", key)
        api_key = get_redis_data("hyp_api_key")
        await hyp_api.finish(f"更新api{api_key}")
    else:
        await hyp_api.finish(f"请输入api")
