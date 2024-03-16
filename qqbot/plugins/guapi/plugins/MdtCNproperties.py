import json
from pathlib import Path
from typing import Optional
from nonebot import on_command, get_driver
from nonebot.adapters.qq import MessageSegment
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from ..utils.ppeteer import screenshot
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams

config_ip = get_driver().config.dict()["guapi"]["ip"]
config_port = get_driver().config.dict()["guapi"]["port"]

MdtCNDict: Optional[dict] = None
wikidata: Optional[dict] = None
mdtmsg = on_command("MDT", rule=to_me(), aliases={"像素工厂"}, priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@mdtmsg.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    global MdtCNDict, wikidata
    if name := args.extract_plain_text():
        if MdtCNDict is None or wikidata is None:
            data_init()
        if name in MdtCNDict:
            dictdata = MdtCNDict[f"{name}"].replace("-", " ").split(".")
            dictdata[0] = getname(dictdata[0])
            if dictdata[0] in wikidata:
                if dictdata[1].title() in wikidata[dictdata[0]]:
                    urldata = wikidata[dictdata[0]][dictdata[1].title()]
                    image = await screenshot(1920, 1080, f"{urldata}",
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
                    if image is not None:
                        mdmsg = MessageMarkdown(
                            custom_template_id="102071975_1702460123",
                            params=[
                                MessageMarkdownParams(key="text_start", values=[f"{name}|搜索结果"]),
                                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                                MessageMarkdownParams(key="img_url",
                                                      values=[f"http://{config_ip}:{config_port}/api/files/{image_id}"])
                            ]
                        )
                        if group_id is not None:
                            await mdtmsg.finish(MessageSegment.markdown(mdmsg))
                        else:
                            await mdtmsg.finish(MessageSegment.image(f"http://{config_ip}:{config_port}/api/files/{image_id}"))
                    else:
                        await mdtmsg.finish("访问超时")
                else:
                    await mdtmsg.finish("错误的数据")
            else:
                await mdtmsg.finish("错误的数据")
        else:
            await mdtmsg.finish("错误的数据")
    else:
        await mdtmsg.finish("请输入搜索项")


class config:
    def __init__(self, file_path):
        self.file = open(file_path, "r", encoding="utf-8")
        self.dict = {}
        for line in self.file:
            line = line.strip()
            if line and "=" in line:
                key, value = line.split(" = ")
                self.dict[value] = key
        self.file.close()

    def get_value(self, key):
        return self.dict.get(key)

    def set_value(self, key, value):
        self.dict[key] = value

    value = property(get_value, set_value)


def data_init():
    global wikidata, MdtCNDict
    with open("./data/wikilist.json", "r") as f:
        wikidata = json.load(f)
    file_path = "./data/bundle_zh_CN.properties"
    MdtCNDict = config(file_path).dict


def getname(name: str):
    if name == "block":
        return "Blocks"
    elif name == "item":
        return "Items"
    elif name == "liquid":
        return "Liquids"
    elif name == "unit":
        return "Units"
    else:
        return name
