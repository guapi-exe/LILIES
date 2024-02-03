from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    OwnerID = "D347AB1C065CFBCF50760953E1549156"
