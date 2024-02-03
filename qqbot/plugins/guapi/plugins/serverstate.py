import threading
import time
from asyncio import AbstractEventLoop
from threading import Timer
import psutil
import platform
import asyncio
from typing import Optional
from nonebot import logger
from pydantic import BaseModel

from .Mcserverstate import get_mcserver_state_from_redis
from ..libs import DeviceInformation

server_state: Optional[DeviceInformation] = None
loop: Optional[AbstractEventLoop] = None
loop_mc: Optional[AbstractEventLoop] = None


async def getnet():
    s1 = psutil.net_io_counters()
    await asyncio.sleep(1)
    s2 = psutil.net_io_counters()
    net_send = ((s2[0] - s1[0]) * 8) / (10 ** 6)
    net_recv = ((s2[1] - s1[1]) * 8) / (10 ** 6)
    logger.info(f"net_send{net_send}Mbps|net_recv{net_recv}Mbps")
    return [net_send, net_recv]


async def DInfo():
    cpu_percent = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    mem_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")
    net = await getnet()
    net_send = net[0]
    net_recv = net[1]

    device_info = DeviceInformation(
        cpumodel=platform.processor(),
        cpu_percent=cpu_percent,
        cpu_count=cpu_count,
        cpu_current=cpu_freq.current / 1000,
        mem_total=mem_info.total / 1024 ** 3,
        mem_available=mem_info.available / 1024 ** 3,
        mem_percent=mem_info.percent,
        disk_total=disk_info.total / 1024 ** 3,
        disk_free=disk_info.free / 1024 ** 3,
        disk_percent=disk_info.percent,
        net_send=net_send,
        net_recv=net_recv
    )
    logger.info("dinfo:" + str(device_info))
    return device_info


async def Update_DInfo_list(dinfolist: DeviceInformation):
    dinfo = await DInfo()
    cpu_percent = dinfo.cpu_percent
    mem_percent = dinfo.mem_percent
    net_send = dinfo.net_send
    net_recv = dinfo.net_recv
    if dinfolist is None or dinfolist.cpu_percent_list is None:
        dinfolist = DeviceInformation(
            cpumodel=dinfo.cpumodel,
            cpu_percent=cpu_percent,
            cpu_percent_list=[],
            cpu_count=dinfo.cpu_count,
            cpu_current=dinfo.cpu_current,
            mem_percent=mem_percent,
            mem_available=dinfo.mem_available,
            mem_total=dinfo.mem_total,
            mem_percent_list=[],
            disk_total=dinfo.disk_total,
            disk_free=dinfo.disk_free,
            disk_percent=dinfo.disk_percent,
            net_send=net_send,
            net_recv=net_recv,
            net_send_list=[],
            net_recv_list=[],
            time_list=[]
        )
    else:
        if len(dinfolist.cpu_percent_list) >= 60:
            del dinfolist.cpu_percent_list[0]
            del dinfolist.mem_percent_list[0]
            del dinfolist.net_send_list[0]
            del dinfolist.net_recv_list[0]
            del dinfolist.time_list[0]
        dinfolist.cpumodel = dinfo.cpumodel
        dinfolist.cpu_percent = dinfo.cpu_percent
        dinfolist.cpu_count = dinfo.cpu_count
        dinfolist.mem_total = dinfo.mem_total
        dinfolist.mem_percent = dinfo.mem_percent
        dinfolist.mem_available = dinfo.mem_available
        dinfolist.disk_percent = dinfo.disk_percent
        dinfolist.disk_total = dinfo.disk_total
        dinfolist.disk_free = dinfo.disk_free
        dinfolist.net_recv = dinfo.net_recv
        dinfolist.net_send = dinfo.net_send
    dinfolist.cpu_percent_list.append(cpu_percent)
    dinfolist.mem_percent_list.append(mem_percent)
    dinfolist.net_send_list.append(net_send)
    dinfolist.net_recv_list.append(net_recv)
    dinfolist.time_list.append(time.strftime('%m-%d %H:%M:%S'))
    # logger.info(dinfolist)
    return dinfolist


async def job():
    global server_state
    if not server_state:
        server_state = await Update_DInfo_list(None)
    else:
        server_state = await Update_DInfo_list(server_state)
    # logger.info(server_state)
    await asyncio.sleep(60)
    global loop
    loop = asyncio.get_running_loop()
    loop.call_later(1, lambda: asyncio.run_coroutine_threadsafe(job(), loop))


async def job_mc():
    await get_mcserver_state_from_redis()
    await asyncio.sleep(60 * 5)
    global loop_mc
    loop_mc = asyncio.get_running_loop()
    loop_mc.call_later(1, lambda: asyncio.run_coroutine_threadsafe(job_mc(), loop_mc))


async def get_server_state():
    global server_state
    if server_state is None:
        server_state = await Update_DInfo_list(None)
    logger.info(f"服务器状态{server_state}")
    return server_state


def run_in_thread(func):
    loop = asyncio.new_event_loop()  # 创建一个新的事件循环
    asyncio.set_event_loop(loop)  # 设置事件循环
    func()


def run_in_thread_mc(func):
    loop = asyncio.new_event_loop()  # 创建一个新的事件循环
    asyncio.set_event_loop(loop)  # 设置事件循环
    func()


def start_server_state():
    logger.info("定时服务器状态获取开始")
    global loop
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(lambda: asyncio.run_coroutine_threadsafe(job(), loop))
    loop.run_forever()


def start_mcserver_state():
    logger.info("定时MC服务器状态获取开始")
    global loop_mc
    loop_mc = asyncio.get_event_loop()
    loop_mc.call_soon_threadsafe(lambda: asyncio.run_coroutine_threadsafe(job_mc(), loop_mc))
    loop_mc.run_forever()


def stop_server_state():
    logger.info("定时服务器状态获取关闭")
    global loop
    loop.stop()


thread = threading.Thread(target=run_in_thread, args=(start_server_state,))
thread.start()

thread_mc = threading.Thread(target=run_in_thread_mc, args=(start_mcserver_state,))
thread_mc.start()
