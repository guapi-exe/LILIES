import base64
import json
import requests
from nonebot import logger


def uuid_get(name: str):
    try:
        request = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
        if "id" in request.json():
            logger.debug(request.json()["id"])
            return request.json()["id"]
    except Exception as e:
        logger.error(e)
        return None


def get_skin(uuid):
    try:
        response = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}")
        data = response.json()
        base64_value = data["properties"][0]["value"]
        buff = base64.b64decode(base64_value)
        str_value = buff.decode('utf-8')
        json_skin = json.loads(str_value)
        skin_cape_list = []
        if "SKIN" in json_skin["textures"]:
            skin_url = json_skin["textures"]["SKIN"]["url"]
            skin_cape_list.append(skin_url)
        if "CAPE" in json_skin["textures"]:
            cape_url = json_skin["textures"]["CAPE"]["url"]
            skin_cape_list.append(cape_url)
        return skin_cape_list
    except Exception as e:
        logger.error(e)
        return None


def hyp_info_get(key: str, uuid: str):
    try:
        request_info = requests.get(f"https://api.hypixel.net/v2/player?key={key}&uuid={uuid}")
        request_status = requests.get(f"https://api.hypixel.net/v2/status?key={key}&uuid={uuid}")
        skin_cape_url = get_skin(uuid)
        json_data = request_info.json()
        json_data_status = request_status.json()
        # logger.debug(request_info.json())
        if json_data["success"]:
            if json_data_status["success"]:
                online = json_data_status["session"]["online"]
                json_data["online"] = online
            else:
                json_data["online"] = False
            if skin_cape_url is not None:
                json_data["skin_url"] = skin_cape_url[0]
                if len(skin_cape_url) > 1:
                    json_data["cape_url"] = skin_cape_url[1]
                else:
                    json_data["cape_url"] = ""
            return json_data
        else:
            logger.error(json_data)
            return None
    except Exception as e:
        logger.error(e)
        return None


# print(hyp_info_get("1fce387f-12f1-4ccd-95ab-b168a616414d", uuid_get("_blac_")))



