import uuid
from pathlib import Path
from typing import Optional
from PIL import Image
import requests
from nonebot import on_command, logger, get_driver
from nonebot.rule import to_me
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams

config_ip = get_driver().config.dict()["guapi"]["ip"]
config_port = get_driver().config.dict()["guapi"]["port"]

rand_image = on_command("随机图片", rule=to_me(), aliases={"随机二次元"}, priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@rand_image.handle()
async def handle_function(event: Event = MessageEvent()):
    result = await download("https://www.dmoe.cc/random.php", imgfile_path)
    if result[0]:
        address = result[1]
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
                MessageMarkdownParams(key="text_start", values=[f"随机图片"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{result[2]}px #{result[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"]),
            ]
        )
        if group_id is not None:
            await rand_image.finish(MessageSegment.markdown(mdmsg))
        else:
            await rand_image.finish(MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
    else:
        await rand_image.finish("图片下载错误")


async def download(url: str, path: str):
    try:
        image_data = requests.get(url).content
        image_path = path + '/' + str(uuid.uuid4()) + '-cache.png'
        with open(image_path, "wb") as f:
            f.write(image_data)
        logger.info(f"成功下载图片至{image_path}")
        width, height = get_image_size(image_path)
        return [True, image_path, width, height]
    except Exception as e:
        logger.error(f"图片下载失败{e}")
        return [False]


def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height
