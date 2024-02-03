from pathlib import Path
from typing import Optional

import mcstatus
from nonebot import on_command, logger, get_driver
from nonebot.adapters.qq import MessageSegment
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import CommandArg
from ..libs import Mcserver, server_list
from ..utils.ppeteer import screenshot
from nonebot.adapters.qq.models import MessageArk, MessageArkKv, MessageKeyboard, MessageMarkdown, MessageMarkdownParams
from ..utils.redisdata import redis_storage, get_redis_data, redis_storage_cover, remove_redis_data
from ..utils.sqlite import update_server_list, get_server_list, update_mcserver_info, get_mcserver_info, remove_server
from nonebot.adapters.qq import MessageSegment, Event, Message, MessageEvent, permission

config_ip = get_driver().config.dict()["guapi"]["ip"]


add_mc_server_list = on_command("MC添加服务器", rule=to_me(), aliases={"MC添加"},
                                priority=10, block=True)
set_mc_server = on_command("设置群MC服务器", rule=to_me(),
                           priority=10, block=True)
remove_mc_server_list = on_command("MC移除服务器", rule=to_me(), aliases={"MC移除"},
                                   priority=10, block=True)
add_mdt_server_list = on_command("MDT添加服务器", rule=to_me(), aliases={"MDT添加"},
                                 priority=10, block=True)
look_server_state = on_command("服务器状态", rule=to_me(), priority=10)
imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


@set_mc_server.handle()
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
        redis_storage_cover(group_id, server_ip)
        await set_mc_server.finish(f"设置成功")


@add_mc_server_list.handle()
async def handle_function(args: Message = CommandArg()):
    if server_ip := args.extract_plain_text():
        add_server_list([server_ip], [])
        logger.info(f"添加MC服务器列表")
    await add_mc_server_list.finish("添加成功")


@remove_mc_server_list.handle()
async def handle_function(args: Message = CommandArg()):
    if server_ip := args.extract_plain_text():
        num = remove_server(server_ip)
        logger.info(f"移除MC服务器列表")
        redis_del_result = remove_redis_data("mc_server_list", server_ip)
        if num:
            await remove_mc_server_list.finish(f"移除成功共计移除了{num}个元素|redis移除{redis_del_result}")
        else:
            await remove_mc_server_list.finish(f"没有可移除的元素|redis移除{redis_del_result}")


@add_mdt_server_list.handle()
async def handle_function(args: Message = CommandArg()):
    if server_ip := args.extract_plain_text().strip():
        add_server_list([], [server_ip])
        logger.info(f"添加MDT服务器列表")
    await add_mc_server_list.finish("添加成功")


@look_server_state.handle()
async def handle_function(args: Message = CommandArg(), event: Event = MessageEvent()):
    guild_id: Optional = None
    group_id: Optional = None
    dict_event = event.dict()
    if "group_id" in dict_event:
        group_id = dict_event["group_id"]
    if "guild_id" in dict_event:
        guild_id = dict_event["guild_id"]
    server_ip = get_redis_data(group_id)
    command = args.extract_plain_text().strip()

    if command == "all" or server_ip is None:
        image = await screenshot(1220, 1080, f"http://127.0.0.1:8099/serverstate",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"服务器状态信息"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:8099/api/files/{image_id}"]),
                MessageMarkdownParams(key="text_end", values=[f"需要添加看help加群"]),
            ]
        )
        if group_id is not None:
            await look_server_state.finish(MessageSegment.markdown(mdmsg))
        else:
            await look_server_state.finish(MessageSegment.image(f"http://{config_ip}:8099/api/files/{image_id}"))
    else:
        if command != "":
            server_ip = command
        image = await screenshot(1260, 1080, f"http://127.0.0.1:8099/Mcserver?ip={server_ip}",
                                 imgfile_path, None, True, 5)
        address = image[1]
        parts = address.split("/")
        image_id = parts[-1]
        mdmsg = MessageMarkdown(
            custom_template_id="102071975_1702460123",
            params=[
                MessageMarkdownParams(key="text_start", values=[f"服务器状态信息"]),
                MessageMarkdownParams(key="img_dec", values=[f"img #{image[2]}px #{image[3]}px"]),
                MessageMarkdownParams(key="img_url", values=[f"http://{config_ip}:8099/api/files/{image_id}"]),
            ]
        )
        kbmsg = MessageKeyboard(
            content={
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "10",
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
            await look_server_state.finish(MessageSegment.image(f"http://{config_ip}:8099/api/files/{image_id}"))


async def get_mcserver_state(ip: str):
    try:
        servers = await mcstatus.JavaServer.lookup(ip, 5).async_status()
    except Exception as e:
        logger.error(e)
        servers = None
    if servers is not None:
        player_list = []
        if servers.players.sample is not None:
            if len(servers.players.sample) != 0:
                for player in servers.players.sample:
                    player_list.append(player.name)
        if "extra" in servers.motd.raw:
            raw_text = servers.motd.raw["extra"]
        elif "text" in servers.motd.raw:
            raw_text = [{"raw": servers.motd.raw["text"]}]
        elif servers.motd.raw is not None:
            raw_text = [{"raw": servers.motd.raw}]
        else:
            raw_text = [{"raw": ''}]
        logger.info(raw_text)
        server_state = Mcserver(
            server_ip=ip,
            server_ping=servers.latency,
            player_online=servers.players.online,
            player_max=servers.players.max,
            player_list=player_list,
            server_version=servers.version.name,
            server_motd=raw_text,
            server_favicon=servers.icon,
            server_online=1,
        )
        return server_state
    else:
        server_state = Mcserver(
            server_ip=ip,
            server_ping=-1,
            server_online=0,
        )
        return server_state


def add_server_list(mc_server_list: list, mdt_server_list: list):
    data = server_list(
        mc_server_list=mc_server_list,
        mdt_server_list=mdt_server_list
    )
    update_server_list(data)
    redis_storage("mc_server_list", mc_server_list)
    redis_storage("mdt_server_list", mdt_server_list)
    logger.info(f"add_data{data}")


async def get_all_mcserver_state():
    servers_list = get_server_list()
    if servers_list is not None:
        mcserver_list = servers_list.mc_server_list
        mcserver_state_list: Optional[list] = []
        for server in mcserver_list:
            server_state = await get_mcserver_state(server)
            if server_state.server_online:
                mcserver_state_list.append(server_state.dict())
                update_mcserver_info(server_state)
            else:
                mcserver_info = get_mcserver_info(server)
                mcserver_info.server_online = 0
                mcserver_state_list.append(mcserver_info.dict())

        return mcserver_state_list
    else:
        return None


async def get_mcserver_state_from_redis():
    mc_servers_list = get_redis_data("mc_server_list")
    logger.info(mc_servers_list)
    if mc_servers_list is not None:
        mcserver_state_list: Optional[list] = []
        for server in mc_servers_list:
            server_state = await get_mcserver_state(server)
            if server_state.server_online:
                mcserver_state_list.append(server_state.dict())
            else:
                mcserver_state_list.append(server_state.dict())
        redis_storage_cover("mcserver_state_list", mcserver_state_list)
    return list(get_redis_data("mcserver_state_list"))


async def only_get_mcserver_state_from_redis():
    mcserver_state_list = get_redis_data("mcserver_state_list")
    if mcserver_state_list is not None:
        return list(get_redis_data("mcserver_state_list"))
    else:
        return await get_mcserver_state_from_redis()
