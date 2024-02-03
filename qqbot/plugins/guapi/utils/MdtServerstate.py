import asyncio
import socket
from ..libs.MDTDataStream import DataStream
import struct
import threading


async def mdt_ping_host(ip, port, callback):
    async def handle_response(msg, info):
        client.close()
        bbuf = DataStream(msg)

        await callback({
            "name": bbuf.get(bbuf.get()).decode(),
            "map": bbuf.get(bbuf.get()).decode(),
            "players": bbuf.getInt(),
            "wave": bbuf.getInt(),
            "version": bbuf.getInt(),
            "vertype": bbuf.get(bbuf.get()).decode(),
            "gamemode": bbuf.get(),
            "limit": bbuf.getInt(),
            "description": bbuf.get(bbuf.get()).decode(),
            "modeName": bbuf.get(bbuf.get()),
            "ip": info[0],
            "port": info[1]
        }, None)

    def send_request():
        nonlocal client
        client.sendto(struct.pack('!BB', 254, 1), (ip, port))

    def timeout_handler():
        nonlocal client, callback
        if not connected[0]:
            client.close()
            callback(None, Exception("Timed out"))

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(2.0)

    connected = [False]

    try:
        client.connect((ip, port))
        connected[0] = True

        threading.Thread(target=send_request).start()
        threading.Timer(2.0, timeout_handler).start()

        while True:
            data, addr = client.recvfrom(1024)
            await handle_response(data, addr)
            break

    finally:
        client.close()


"""
async def callback(result, error):
    if result:
        print("Ping result:", result)
    elif error:
        print("Error:", error)


asyncio.run(ping_host('cn.mindustry.top', 6567, callback))
"""
