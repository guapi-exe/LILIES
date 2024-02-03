import io

import requests
from nonebot import get_driver
from nonebot.log import logger
from PIL import Image
import uuid
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from nonebot.adapters.qq import Bot
from nonebot.adapters.qq.event import MessageEvent
from nonebot.adapters.qq.message import MessageSegment
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from pathlib import Path
from .data_updater import updateCache
from .data_source import getTeam, getPanel
from .__utils__ import GSPANEL_ALIAS, uidHelper, formatTeam, formatInput, fetchInitRes
config_ip = get_driver().config.dict()["guapi"]["ip"]
driver = get_driver()
driver.on_startup(fetchInitRes)
driver.on_bot_connect(updateCache)
showPanel = on_command("panel", aliases=GSPANEL_ALIAS, priority=13, block=True)
showTeam = on_command("teamdmg", aliases={"队伍伤害"}, priority=13, block=True)

uidStart = ["1", "2", "5", "6", "7", "8", "9"]
imgfile_path = str(Path(__file__).parent.parent.joinpath("guapi").joinpath("webs").joinpath("webfiles"))


@showPanel.handle()
async def panel_handle(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    qq = event.dict()["author"]["id"]
    argsMsg = " ".join(seg.data["text"] for seg in arg["text"])
    # 提取消息中的 at 作为操作目标 QQ
    opqq = event.dict()["author"]["id"]
    # 输入以「绑定」开头，识别为绑定操作
    if argsMsg.startswith("绑定"):
        args = [a for a in argsMsg[2:].split() if a.isdigit()]
        if len(args) == 1:
            uid, opqq = args[0], opqq or qq
        elif len(args) == 2:
            uid, opqq = args[0], (opqq or args[1])
        else:
            await showPanel.finish("绑定参数格式错误！", at_sender=True)
        if opqq != qq and qq not in bot.config.superusers:
            await showPanel.finish(f"没有权限操作 QQ{qq} 的绑定状态！", at_sender=True)
        elif uid[0] not in uidStart or len(uid) != 9:
            await showPanel.finish(f"UID 是「{uid}」吗？好像不对劲呢..", at_sender=True)
        await showPanel.finish(await uidHelper(opqq, uid))
    # 尝试从输入中理解 UID、角色名
    uid, char = await formatInput(argsMsg, qq, opqq)
    if not uid:
        await showPanel.finish("要查询角色面板的 UID 捏？\n 使用/面板 绑定[uuid]绑定账号", at_sender=True)
    elif not uid.isdigit() or uid[0] not in uidStart or len(uid) != 9:
        await showPanel.finish(f"UID 是「{uid}」吗？好像不对劲呢..", at_sender=True)
    logger.info(f"正在查找 UID{uid} 的「{char}」角色面板..")
    rt = await getPanel(uid, char)
    if isinstance(rt, str):
        await showPanel.finish(MessageSegment.text(rt))
    elif isinstance(rt, bytes):
        image_id = str(uuid.uuid4()) + '-cache.png'
        image_path = imgfile_path + '/' + image_id
        image = Image.open(io.BytesIO(rt))
        image.save(image_path, 'PNG')
        width, height = image.size
        kbmsg = MessageKeyboard(
            content={
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "13",
                                "render_data": {
                                    "label": "查询全部",
                                    "visited_label": "查询全部"
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
                                    "data": "/面板"
                                }
                            }, {
                                "id": "14",
                                "render_data": {
                                    "label": "绑定uuid",
                                    "visited_label": "绑定uuid"
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
                                    "data": "/面板 绑定"
                                }
                            }

                        ]
                    }, {
                        "buttons": [
                            {
                                "id": "15",
                                "render_data": {
                                    "label": "队伍伤害",
                                    "visited_label": "队伍伤害"
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
                                    "data": "/队伍伤害"
                                }
                            }
                        ]
                    }
                ]
            }
        )
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{char}的角色面板"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{width}px #{height}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}/api/files/{image_id}"]),
            ]
        )
        await showPanel.finish(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))


@showTeam.handle()
async def team_handle(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    qq = event.dict()["author"]["id"]
    argsMsg = " ".join(seg.data["text"] for seg in arg["text"])
    # 提取消息中的 at 作为操作目标 QQ
    opqq = event.dict()["author"]["id"]
    # 是否展示伤害过程，默认不显示
    showDetail, keywords = False, ["详情", "过程", "全部", "全图"]
    if any(argsMsg.startswith(word) for word in keywords):
        showDetail = True
        for word in keywords:
            argsMsg = argsMsg.lstrip(word).strip()
    # 尝试从输入中理解 UID、角色名
    uid, chars = await formatTeam(argsMsg, qq, opqq)
    if not uid:
        await showTeam.finish("要查询队伍伤害的 UID 捏？", at_sender=True)
    elif not uid.isdigit() or uid[0] not in uidStart or len(uid) != 9:
        await showTeam.finish(f"UID 是「{uid}」吗？好像不对劲呢..", at_sender=True)
    if not chars:
        logger.info(f"QQ{qq} 的输入「{argsMsg}」似乎未指定队伍角色！")
    logger.info(f"正在查找 UID{uid} 的「{'/'.join(chars) or '展柜前 4 角色'}」队伍伤害面板..")
    rt = await getTeam(uid, chars, showDetail)
    if isinstance(rt, str):
        await showTeam.finish(MessageSegment.text(rt))
    elif isinstance(rt, bytes):
        image_id = str(uuid.uuid4()) + '-cache.png'
        image_path = imgfile_path + '/' + image_id
        image = await Image.open(io.BytesIO(rt))
        await image.save(image_path, 'PNG')
        width, height = image.size
        kbmsg = MessageKeyboard(
            content={
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "16",
                                "render_data": {
                                    "label": "队伍伤害详细",
                                    "visited_label": "队伍伤害详细"
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
                                    "data": "/队伍伤害 详细"
                                }
                            }
                        ]
                    }
                ]
            }
        )
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"{uid}的队伍伤害面板"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{width}px #{height}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}/api/files/{image_id}"]),
            ]
        )
        await showTeam.finish(Message([MessageSegment.markdown(mdmsg), MessageSegment.keyboard(kbmsg)]))


"""
原项目地址来自https://github.com/monsterxcn/nonebot-plugin-gspanel
此为搬运适配协议
"""