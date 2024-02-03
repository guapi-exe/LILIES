import ast
import asyncio
import json
import mcstatus
from nonebot import on_command, logger


async def get_mcserver_state_original(ip: str):
    try:
        servers = await mcstatus.JavaServer.lookup(ip, 5).async_status()
    except Exception as e:
        logger.error(e)
        return [None, e.__str__()]
    if servers is not None:
        state_dict = servers.__dict__
        for key in state_dict:
            if "mcstatus" in str(type(state_dict[key])):
                state_dict[key] = state_dict[key].__dict__
            else:
                state_dict[key] = state_dict[key]
            if type(state_dict[key]) is dict or type(state_dict[key]) is list:
                for new_key in state_dict[key]:
                    if "mcstatus" in str(type(state_dict[key][new_key])):
                        state_dict[key][new_key] = state_dict[key][new_key].__dict__
                    else:
                        state_dict[key][new_key] = state_dict[key][new_key]
                    if type(state_dict[key][new_key]) is dict or type(state_dict[key][new_key]) is list:
                        for new_key2 in state_dict[key][new_key]:
                            logger.info(state_dict[key][new_key])
                            if type(state_dict[key][new_key]) is list:
                                if "mcstatus" in str(type(new_key2)):
                                    state_dict[key][new_key].remove(new_key2)
                                    state_dict[key][new_key].insert(0, new_key2.__dict__)
                                elif "MinecraftColor" in str(type(new_key2)) \
                                        or "Formatting" in str(type(new_key2)) \
                                        or "WebColor" in str(type(new_key2))\
                                        or "TranslationTag" in str(type(new_key2)):
                                    state_dict[key][new_key].remove(new_key2)
                                    state_dict[key][new_key].insert(0, str(new_key2))
                            else:
                                if "mcstatus" in str(type(state_dict[key][new_key][new_key2])):
                                    state_dict[key][new_key][new_key2] = state_dict[key][new_key][new_key2].__dict__
                                else:
                                    state_dict[key][new_key][new_key2] = state_dict[key][new_key][new_key2]
        logger.info(state_dict)
        json_state = json.dumps(state_dict)
        logger.info(json_state)
        return json_state
    else:
        return [None, False]


"""
server = asyncio.run(get_mcserver_state_original("new.xem8k5.top:1090"))
print(server)
if type(server) is not list:
    print(server)
else:
    print(f"err{server[1]}")
"""

