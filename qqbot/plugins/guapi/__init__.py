from pathlib import Path
import nonebot
from nonebot import get_driver
from nonebot.plugin import PluginMetadata
from .config import Config
from nonebot.plugin.manager import PluginLoader

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("libs").resolve()),
    str(Path(__file__).parent.joinpath("utils").resolve()),
    str(Path(__file__).parent.joinpath("plugins").resolve()),
    str(Path(__file__).parent.joinpath("webs").resolve()),
)
__plugin_meta__ = PluginMetadata(
    name="guapi",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config
config = Config.parse_obj(global_config)

