import asyncio
import requests
from PIL import Image
from io import BytesIO
from nonebot import logger


async def download_image(download_url):
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        return response.content
    except Exception as err:
        logger.error(err)
        return None


class McskinHead:
    async def getimage(self, image_url: str, image_size):
        try:
            crop_params = [
                {"left": 8, "top": 8, "width": 8, "height": 8},
                {"left": 40, "top": 8, "width": 8, "height": 8}
            ]
            resize_params = [
                {"width": image_size, "height": image_size},
                {"width": int(image_size * (9 / 8)), "height": int(image_size * (9 / 8))}
            ]
            downimage = await download_image(image_url)
            buffers = []

            for i in range(len(crop_params)):
                # 创建一个PIL Image对象
                image = Image.open(BytesIO(downimage))
                image = image.convert("RGBA")
                image = image.crop((crop_params[i]["left"], crop_params[i]["top"],
                                    crop_params[i]["left"] + crop_params[i]["width"],
                                    crop_params[i]["top"] + crop_params[i]["height"]))
                image = image.resize((resize_params[i]["width"], resize_params[i]["height"]), Image.NEAREST)

                # 获取图片的numpy array并添加到数组中
                buffer = BytesIO()
                image.save(buffer, format="PNG")
                buffer.seek(0)
                buffers.append(buffer.read())
                logger.info(f"图片截取成功")

            composite_buffer = await self.composite_images(buffers[0], buffers[1], image_size)
            return [buffers[0], buffers[1], composite_buffer]
        except Exception as err:
            logger.error(err)
            return None

    async def composite_images(self, buffer1, buffer2, output_size):  # 最终输出尺寸为outsize的9/8
        try:
            image1 = Image.open(BytesIO(buffer1)).convert("RGBA")
            image2 = Image.open(BytesIO(buffer2)).convert("RGBA")
            composite_image = Image.new("RGBA", (int(output_size * (9 / 8)), int(output_size * (9 / 8))))
            composite_image.alpha_composite(image1, (int(output_size / 16), int(output_size / 16)))
            temp_image = composite_image.copy()
            temp_image.alpha_composite(image2, (0, 0))
            temp_image = temp_image.resize((output_size, output_size), Image.NEAREST)
            composite_buffer = BytesIO()
            temp_image.save(composite_buffer, format="PNG")
            composite_buffer.seek(0)
            logger.info(f"图片合成完毕")
            return composite_buffer.read()
        except Exception as err:
            logger.error(f"[图片合成err]{err}")
            return None


# 示例用法
"""
url = "http://textures.minecraft.net/texture/9775f2e1641b5c6bed4764b3b3b4ad392e4f15a780155dc201c766fdee4ce35f"
size = 256

mc_skin_head = McskinHead()
mcskin = asyncio.run(mc_skin_head.getimage(url, size))
composite_img = Image.open(BytesIO(mcskin[2]))
composite_img.save("./skinheadimage.png", format="PNG")
print(mcskin[2])
"""
