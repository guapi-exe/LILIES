import asyncio
from typing import Optional
import uuid
from pyppeteer import launch
from pyppeteer.browser import Browser
from nonebot.log import logger
from PIL import Image
_browser: Optional[Browser] = None


async def init_brower() -> Browser:
    global _browser, browser
    try:
        browser = await launch(headless=True,
                               ignoreHTTPSErrors=True,
                               args=['--disable-infobars', '--no-sandbox', '--process-per-tab'])
    except Exception as e:
        logger.error(f"inin_brower{e}")
    _browser = browser
    return _browser


async def screenshot(Width, Height, Url, Output, JSexec, FullPage, Waittime):
    # 连接浏览器
    global _browser
    if not _browser:
        _browser = await init_brower()
    page = await _browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/66.0.3359.181 Safari/537.36")
    await page.setViewport(viewport={'width': Width, 'height': Height})
    await page.setJavaScriptEnabled(enabled=True)
    page.setDefaultNavigationTimeout(60000)
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => false})')
    try:
        await page.goto(Url)

        if Waittime:
            await asyncio.sleep(Waittime)
        if JSexec:
            await page.evaluate(JSexec)

        Saveput = Output + '/' + str(uuid.uuid4())
        Output = Saveput + '-cache.png'
        if FullPage:
            image = await page.screenshot({'path': Output, 'fullPage': True})
        else:
            image = await page.screenshot({'path': Output})
        logger.info(f'[browser] 生成图片完成{Output}')
        width, height = get_image_size(Output)
        await page.close()
        return [image, Output, width, height]
    except Exception as e:
        logger.error(e)
        return False


async def close_brower():
    global _browser
    await _browser.close()


def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height