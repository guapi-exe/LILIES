import datetime
from typing import Optional
from pydantic import BaseModel


class Mcserver(BaseModel):
    server_ip: Optional[str]
    server_ping: Optional[int]
    player_online: Optional[int]
    player_max: Optional[int]
    player_list: Optional[list]
    server_version: Optional[str]
    server_motd: Optional[list]
    server_favicon: Optional[str]
    server_online: Optional[int]


class User(BaseModel):
    id: Optional[str]
    exp: Optional[float]
    coins: Optional[int]
    last_signin_date: Optional[datetime.date]


class server_list(BaseModel):
    mc_server_list: Optional[list]
    mdt_server_list: Optional[list]


class DeviceInformation(BaseModel):
    cpumodel: Optional[str]
    cpu_percent: Optional[float]
    cpu_percent_list: Optional[list]
    cpu_count: Optional[int]
    cpu_current: Optional[float]
    mem_total: Optional[float]
    mem_percent: Optional[float]
    mem_available: Optional[float]
    mem_percent_list: Optional[list]
    disk_total: Optional[float]
    disk_percent: Optional[float]
    disk_free: Optional[float]
    net_send: Optional[float]
    net_send_list: Optional[list]
    net_recv: Optional[float]
    net_recv_list: Optional[list]
    time_list: Optional[list]
