import asyncio
import os
import threading
import datetime
from pathlib import Path
from nonebot import logger

imgfile_path = str(Path(__file__).parent.parent.joinpath("webs").joinpath("webfiles"))


def clear_folder(folder):
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=3)
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        file_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path)).date()
        if file_time < seven_days_ago:
            logger.info(f"图片文件清理{file_path}")
            os.remove(file_path)


async def run_clear_files():
    while True:
        today = datetime.date.today()
        logger.info(f"清理开始{today}")
        clear_folder(imgfile_path)
        await asyncio.sleep(60 * 60 * 24)


def start_thread():
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(lambda: asyncio.run_coroutine_threadsafe(run_clear_files(), loop))
    loop.run_forever()


def run_in_thread(func):
    loop = asyncio.new_event_loop()  # 创建一个新的事件循环
    asyncio.set_event_loop(loop)  # 设置事件循环
    func()


thread = threading.Thread(target=run_in_thread, args=(start_thread,))
thread.start()
