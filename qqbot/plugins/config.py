from typing import Optional
from pydantic import BaseModel, Extra

"""
废案
"""


class Config(BaseModel, extra=Extra.ignore):
    ip = "101.34.203.130"
