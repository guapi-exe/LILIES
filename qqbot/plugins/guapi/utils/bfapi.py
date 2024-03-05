from typing import Optional
from nonebot import on_command, logger, get_driver
import requests


async def get_bfv_weapons_list(name: str):
    url = f"https://api.gametools.network/bfv/weapons/?format_values=false&name={name}&lang=zh-cn"
    request = requests.get(url)
    content = request.json()

    if "weapons" in content:
        weapons = content["weapons"]
        weapons.sort(key=lambda x: (-x["timeEquipped"]))
        return weapons
    else:
        return None


async def get_bfv_vehicles_list(name: str):
    url = f"https://api.gametools.network/bfv/vehicles/?format_values=false&name={name}&lang=zh-cn"
    request = requests.get(url)
    content = request.json()

    if "vehicles" in content:
        vehicles = content["vehicles"]
        vehicles.sort(key=lambda x: (-x["timeIn"]))
        return vehicles
    else:
        return None


async def get_bfv_classes_list(name: str):
    url = f"https://api.gametools.network/bfv/classes/?format_values=false&name={name}&lang=zh-cn"
    request = requests.get(url)
    content = request.json()
    if "classes" in content:
        classes: list = content["classes"]
        for classe in classes:
            logger.info(classe)
            if "image" in classe:
                if "突击兵" in classe["image"]:
                    classes[classes.index(classe)]["image"] = "https://cdn.gametools.network/classes/bf5/white" \
                                                              "/Assault.png"
                if "医疗兵" in classe["image"]:
                    classes[classes.index(classe)]["image"] = "https://cdn.gametools.network/classes/bf5/white" \
                                                              "/Medic.png"
                if "侦察兵" in classe["image"]:
                    classes[classes.index(classe)]["image"] = "https://cdn.gametools.network/classes/bf5/white" \
                                                              "/Recon.png"
                if "支援兵" in classe["image"]:
                    classes[classes.index(classe)]["image"] = "https://cdn.gametools.network/classes/bf5/white" \
                                                              "/Support.png"
        classes.sort(key=lambda x: (-x["secondsPlayed"]))
        logger.info(classes)
        return classes
    else:
        return None


async def get_bf2042_info(name: str):
    url = f"https://api.gametools.network/bf2042/stats/?raw=false&format_values=true&name={name}&lang=zh-cn"
    request = requests.get(url)
    content = request.json()
    logger.info(content)
    vehicles: Optional[list]
    weapons: Optional[list]
    classes: Optional[list]
    if "vehicles" in content:
        vehicles = content["vehicles"]
        vehicles.sort(key=lambda x: (-x["timeIn"]))
    if "weapons" in content:
        weapons = content["weapons"]
        weapons.sort(key=lambda x: (-x["timeEquipped"]))
    if "classes" in content:
        classes = content["classes"]
        classes.sort(key=lambda x: (-x["secondsPlayed"]))
    return {"vehicles": vehicles, "weapons": weapons, "classes": classes, "row": content}


async def get_bf1_weapons_list(name: str):
    url = f"https://api.gametools.network/bf1/weapons/?format_values=false&name={name}&lang=zh-cn"
    request = requests.get(url)
    content = request.json()

    if "weapons" in content:
        weapons = content["weapons"]
        weapons.sort(key=lambda x: (-x["timeEquipped"]))
        return weapons
    else:
        return None


async def get_bf1_vehicles_list(name: str):
    url = f"https://api.gametools.network/bf1/vehicles/?format_values=false&name={name}&lang=zh-cn"
    request = requests.get(url)
    content = request.json()

    if "vehicles" in content:
        vehicles = content["vehicles"]
        vehicles.sort(key=lambda x: (-x["timeIn"]))
        return vehicles
    else:
        return None


async def get_bf1_classes_list(name: str):
    url = f"https://api.gametools.network/bf1/classes/?format_values=false&name={name}&lang=zh-cn"
    request = requests.get(url)
    content = request.json()

    if "classes" in content:
        classes = content["classes"]
        classes.sort(key=lambda x: (-x["secondsPlayed"]))
        return classes
    else:
        return None
