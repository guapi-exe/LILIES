import asyncio
import json
from typing import Optional
import uuid
from pyppeteer import launch
from pyppeteer.network_manager import Response
from pyppeteer.browser import Browser
from nonebot.log import logger
from PIL import Image

_browser: Optional[Browser] = None


def intercept_response(response: Response):
    logger.info(response.status)
    if not response.ok:
        logger.info(response.url)
        response.request.abort()


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


async def headerless_get(url: str):
    global _browser
    if not _browser:
        _browser = await init_brower()
    page = await _browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/66.0.3359.181 Safari/537.36")
    await page.setViewport(viewport={'width': 1000, 'height': 1000})
    page.setDefaultNavigationTimeout(60000)
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => false})')
    try:
        await page.goto(url, {'waitUntil': ['domcontentloaded', 'networkidle1']})
        logger.info(page)
        await page.waitForSelector('body')
        content = await page.content()

        data = json.loads(content)
        return data

    except Exception as e:
        logger.error(e)
        return False


async def screenshot(Width, Height, Url, Output, JSexec, FullPage, Waittime):
    # 连接浏览器
    global _browser
    if not _browser:
        _browser = await init_brower()
    page = await _browser.newPage()
    page.on('response', intercept_response)
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/66.0.3359.181 Safari/537.36")
    await page.setViewport(viewport={'width': Width, 'height': Height})
    await page.setJavaScriptEnabled(enabled=True)
    page.setDefaultNavigationTimeout(60000)
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => false})')
    try:
        try:
            await page.goto(Url, {'waitUntil': ['domcontentloaded', 'networkidle0'], 'timeout': 60000})
            if Waittime:
                await asyncio.sleep(Waittime)
            if JSexec:
                await page.evaluate(JSexec)
            await page.waitForSelector('body')
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
        except asyncio.TimeoutError:
            if Waittime:
                await asyncio.sleep(Waittime)
            if JSexec:
                await page.evaluate(JSexec)
            await page.waitForSelector('body')
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


async def screenshot_elements(Width, Height, Url, Output, JSexec, FullPage, Waittime, elements_class):
    global _browser, Saveput
    if not _browser:
        _browser = await init_brower()
    page = await _browser.newPage()
    page.on('response', intercept_response)
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/66.0.3359.181 Safari/537.36")
    await page.setViewport(viewport={'width': Width, 'height': Height})
    await page.setJavaScriptEnabled(enabled=True)
    page.setDefaultNavigationTimeout(60000)
    await page.evaluateOnNewDocument('Object.defineProperty(navigator, "webdriver", {get: () => false})')
    try:
        try:
            await page.goto(Url, {'waitUntil': ['domcontentloaded', 'networkidle0'], 'timeout': 60000})
            result = []
            if Waittime:
                await asyncio.sleep(Waittime)
            if JSexec:
                await page.evaluate(JSexec)
            elements = await page.JJ(f".{elements_class}")
            if len(elements) <= 0:
                return False
            logger.info(elements)
            for element in elements:
                Saveput = Output + '/' + str(uuid.uuid4()) + '-cache.png'

                if FullPage:
                    image = await element.screenshot({'path': Saveput, 'fullPage': True})
                else:
                    image = await element.screenshot({'path': Saveput})
                width, height = get_image_size(Saveput)
                result.append([image, Saveput, width, height])

            logger.info(f'[browser] 生成图片完成{Saveput}')
            await page.close()
            return result
        except asyncio.TimeoutError:
            result = []
            if Waittime:
                await asyncio.sleep(Waittime)
            if JSexec:
                await page.evaluate(JSexec)
            elements = await page.JJ(f".{elements_class}")
            if len(elements) <= 0:
                return False
            logger.info(elements)
            for element in elements:
                Saveput = Output + '/' + str(uuid.uuid4()) + '-cache.png'

                if FullPage:
                    image = await element.screenshot({'path': Saveput, 'fullPage': True})
                else:
                    image = await element.screenshot({'path': Saveput})
                width, height = get_image_size(Saveput)
                result.append([image, Saveput, width, height])

            logger.info(f'[browser] 生成图片完成{Saveput}')
            await page.close()
            return result
    except Exception as e:
        await page.close()
        logger.error(e)
        return False


async def close_brower():
    global _browser
    await _browser.close()


def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height
