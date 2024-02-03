import datetime
import random
import uuid
from pathlib import Path
from typing import Optional
from PIL import Image
import requests
from nonebot import on_command, logger, get_driver
from nonebot.rule import to_me
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot.adapters.qq.models import MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from ..libs import User
from ..utils.sqlite import get_user_data, update_user_data
config_ip = get_driver().config.dict()["guapi"]["ip"]

sign = on_command("签到", rule=to_me(), aliases={"sign"}, priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@sign.handle()
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
        user_id = dict_event["author"]["id"]
        rand_coins = random.Random().randint(0, 100)
        rand_exp = random.random()*50
        user_data = get_user_data(User(id=user_id))
        logger.info(user_data)
        if user_data is None or user_data.id is None:
            user = User(
                id=user_id,
                coins=100 + rand_coins,
                exp=0 + rand_exp,
                last_signin_date=datetime.date.today(),
            )
            update_user_data(user)
        else:
            logger.info(user_data)
            if user_data.last_signin_date == datetime.date.today():
                await sign.finish("今日已签")
            else:
                user_data.last_signin_date = datetime.date.today()
                user_data.exp = user_data.exp + rand_exp
                user_data.coins = user_data.coins + rand_coins
                update_user_data(user_data)
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"签到(测试)获得:{round(rand_exp, 2)}经验|{rand_coins}硬币"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{result[2]}px #{result[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:8099/api/files/{image_id}"]),
                MessageMarkdownParams(key="text_end", values=[f"{get_hitokoto()}"])
            ]
        )
        kbmsg = MessageKeyboard(
            content={
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "3",
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
                            }
                        ]
                    }
                ]
            }
        )
        if group_id is not None:
            await sign.send(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))
        else:
            await sign.finish(MessageSegment.image(f"http://{config_ip}:8099/api/files/{image_id}"))
    else:
        await sign.finish("图片下载错误")


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


def get_hitokoto():
    url = "https://v1.hitokoto.cn/"
    request = requests.get(url)
    content = request.json()
    if "hitokoto" in content:
        hitokoto = content["hitokoto"]
    else:
        hitokoto = None
    return hitokoto

