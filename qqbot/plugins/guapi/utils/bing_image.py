import asyncio
import requests
from urllib.parse import urlencode
import re
from time import sleep
from nonebot.log import logger
import uuid
from PIL import Image


def create_image(tag, cookie, agent_http=None):
    url_encoded_prompt = urlencode({'q': tag})
    power = 3  # power = 4 时候默认消耗用户加速币来生成图片
    url = f"https://edgeservices.bing.com/images/create?{url_encoded_prompt}&rt={power}&FORM=GENCRE"

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://edgeservices.bing.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
        'Cookie': f'_U={cookie}',
        'X-Forwarded-For': '1.1.1.1'
    }

    session = requests.Session()
    if agent_http:
        session.proxies = {'https': agent_http}

    data = {'q': tag, 'qs': 'ds'}

    try:
        response = session.post(url, headers=headers, data=data, allow_redirects=False)
        if 'this prompt has been blocked' in response.text.lower():
            raise ValueError('你的绘画中有被bing所阻止违禁词')
        if response.status_code != 302:
            response = session.post(url, headers=headers, data=data, allow_redirects=False)
            if response.status_code != 302:
                raise ValueError('绘图失败，请检查Bing token和代理/反代配置')

        redirect_url = response.headers['Location'].replace('&nfy=1', '')
        request_id = redirect_url.split('id=')[1]
        logger.info(f'https://edgeservices.bing.com/images/create/async/results/{request_id}?q={url_encoded_prompt}')
        return f'https://edgeservices.bing.com/images/create/async/results/{request_id}?q={url_encoded_prompt}'
    except Exception as e:
        raise Exception(e)


def extract_image_links(html_content):
    image_links = re.findall(r'src="([^"]+)"', html_content)
    if not image_links:
        return None
    image_links = [link.split('?w=')[0] for link in image_links]
    return list(set(image_links))


def filter_bad_images(image_links, bad_images):
    return [link for link in image_links if link not in bad_images]


async def get_image_url(url, cookie, agent_http=None):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://edgeservices.bing.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50',
        'Cookie': f'_U={cookie}',
        'X-Forwarded-For': '1.1.1.1'
    }

    session = requests.Session()
    if agent_http:
        session.proxies = {'https': agent_http}

    timeout_times = 80
    while timeout_times > 0:
        response = session.post(url, headers=headers)
        response_text = response.text
        if 'we can\'t create your images right now' in response_text.lower():
            raise RuntimeError('Bing无法处理你的图像请求')
        image_links = extract_image_links(response_text)
        if image_links is not None:
            filtered_links = filter_bad_images(image_links, [
                'https://r.bing.com/rp/gmZtdJVd-klWl3XWpa6-ni1FU3M.svg',
                'https://tse4.mm.bing.net/th/id/OIG2.JEZMLCatGlHCSm3dKFz.'
            ])
            if filtered_links:
                return filtered_links
        logger.info(f'绘画等等待中: {timeout_times}')
        timeout_times -= 1
        sleep(1)

    raise TimeoutError('绘图超时')


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


class dell_create_image:
    def __init__(self, cookie, agent_http, tag):
        self.images = None
        self.cookie = cookie
        self.agent_http = agent_http
        try:
            self.create_url = create_image(tag, cookie, agent_http)
        except Exception as e:
            logger.error(e)
            self.create_url = None

    async def return_images(self):
        try:
            self.images = await get_image_url(self.create_url, self.cookie, self.agent_http)
            return self.images
        except Exception as e:
            logger.error(e)
            raise Exception(f"意外错误{e}")


# 简单示范
"""async def image_test():
    cookie = ""
    agent_http = "http://127.0.0.1:10809"
    image = dell_create_image(cookie, agent_http, "猫娘")
    images = await image.return_images()
    print(images)

asyncio.run(image_test())"""
