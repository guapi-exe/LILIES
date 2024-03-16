import uuid
from pathlib import Path
from typing import Optional
from PIL import Image
import requests
from nonebot import on_command, logger, get_driver
from nonebot.rule import to_me
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from nonebot.params import CommandArg
from qqbot.plugins.guapi.utils.bing_image import dell_create_image

config_ip = get_driver().config.dict()["guapi"]["ip"]
config_port = get_driver().config.dict()["guapi"]["port"]
cookie = get_driver().config.dict()["guapi"]["bing_cookie"]
agent_http = get_driver().config.dict()["guapi"]["agent_http"]

rand_image = on_command("随机图片", rule=to_me(), aliases={"随机二次元"}, priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@rand_image.handle()
async def handle_function(event: Event = MessageEvent(), args: Message = CommandArg()):
    images = None
    try:
        if tag := args.extract_plain_text():
            image = dell_create_image(cookie, agent_http, tag)
            images = await image.return_images()
        else:
            raise Exception("请输入tag")
    except Exception as e:
        logger.error(e)
        await rand_image.finish(f"图片下载错误{e}")
    mdmsg = MessageMarkdown(
        custom_template_id="102071975_1710337447",
        params=[
            MessageMarkdownParams(key="text_start", values=[f"图片"]),
        ]
    )
    for image in images:
        result = await download(image, imgfile_path)
        if result[0]:
            address = result[1]
            parts = address.split("/")
            image_id = parts[-1]
            mdmsg.params.append(MessageMarkdownParams(key=f"img_dec{images.index(image)}",
                                                      values=[f"img #{result[2]}px #{result[3]}px"]))
            mdmsg.params.append(MessageMarkdownParams(key=f"img_url{images.index(image)}", values=[
                f"http://{config_ip}:{config_port}/api/files/{image_id}"]))
        else:
            await rand_image.finish("图片下载错误")
    await rand_image.finish(MessageSegment.markdown(mdmsg))


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
