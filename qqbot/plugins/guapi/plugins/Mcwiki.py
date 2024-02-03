from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup
import urllib.parse
from nonebot import on_command, get_driver
from nonebot.adapters.qq import MessageSegment
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from ..utils.ppeteer import screenshot
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent

config_ip = get_driver().config.dict()["guapi"]["ip"]

mc_wiki = on_command("MC", rule=to_me(), aliases={"我的世界", "McWiki"}, priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))

@mc_wiki.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    if name := args.extract_plain_text():
        url = search_url(name)
        if url is None:
            await mc_wiki.finish("无搜索结果")
        else:
            image = await screenshot(1920, 1080, f"{url}",
                                     imgfile_path, None, True, 1)
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
                    MessageMarkdownParams(key="text_start", values=[f"{name}|搜索结果"]),
                    MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                    MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:8099/api/files/{image_id}"])
                ]
            )
            if group_id is not None:
                await mc_wiki.finish(MessageSegment.markdown(mdmsg))
            else:
                await mc_wiki.finish(MessageSegment.image(f"http://{config_ip}:8099/api/files/{image_id}"))
    else:
        await mc_wiki.finish("请输入搜索项")


def search_url(name: str):
    url_encoded = urllib.parse.quote(name)
    page = requests.get(f"https://search.mcmod.cn/s?key={url_encoded}")
    soup = BeautifulSoup(page.text, "html.parser")
    result_list = soup.select_one(".search-result-list")
    if result_list is None:
        return None
    result_head = result_list.select_one(".head")
    result_url = result_head.find_all("a", target="_blank")
    if result_url is None:
        return None
    for i in result_url:
        url_a = BeautifulSoup(str(i), "html.parser")
        if url_a.find(class_=True) is not None:
            result_url.remove(i)
    if result_url is not None and len(result_url) > 0:
        result = BeautifulSoup(str(result_url[0]), "html.parser").a.get("href")
        return result
    else:
        return None
