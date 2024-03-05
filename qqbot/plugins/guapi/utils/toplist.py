from datetime import datetime
import psutil
import subprocess
import sys
from nonebot import logger


async def get_top_list(pids: list):
    if sys.platform.startswith('linux'):
        top_list = []
        p = subprocess.Popen(['top', '-b', '-n', '1'], stdout=subprocess.PIPE)
        # 等待子进程结束，并获取其输出
        result, error = p.communicate()
        result = result.decode()
        lineno = 0
        for line in result.splitlines():
            lineno += 1
            if lineno > 7:
                parts = line.split()
                pid = parts[0]
                user = parts[1]
                cpu = parts[8]
                command = parts[11]
                mem = parts[9]
                time = parts[10]
                top_list.append({"PID": pid, "User": user, "Name": command, "Cpu": cpu, "MeM": mem, "time": time})
        return top_list

    else:
        top_list = []
        for pid in pids:
            try:
                process = psutil.Process(pid)
                cpu = process.cpu_percent()
                mem = process.memory_percent()
                user = process.username()
                name = process.name()
                time = process.create_time()
                datatime = datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M')
                top_list.append({"PID": pid, "User": user, "Name": name, "Cpu": cpu, "MeM": mem, "time": datatime})
            except Exception as e:
                pass
        top_list.sort(key=lambda x: (-x["Cpu"], -x["MeM"]))
        return top_list
