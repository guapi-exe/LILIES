import ast
import json
import mimetypes
import os
import time
import uuid
from io import BytesIO
from pathlib import Path
from sqlite3 import Cursor
from typing import Optional
from nonebot import on_command, logger, get_driver
from flask import Flask, request, send_file, jsonify, render_template, send_from_directory
from wsgiref.simple_server import make_server
import threading
from ..plugins.Mcserverstate import get_all_mcserver_state, get_mcserver_state_from_redis, \
    only_get_mcserver_state_from_redis
from ..plugins.serverstate import get_server_state
from ..utils.Mcapi import uuid_get, hyp_info_get, get_skin
from ..utils.Mcserverstate import get_mcserver_state_original
from ..utils.McskinHead import McskinHead
from ..utils.bfapi import get_bfv_weapons_list, get_bf1_weapons_list, get_bf2042_info, get_bf1_vehicles_list, \
    get_bfv_vehicles_list, get_bf1_classes_list, get_bfv_classes_list
from ..utils.redisdata import get_redis_data

config_port = get_driver().config.dict()["guapi"]["port"]
cur: Optional[Cursor] = None
app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}  # 允许上传的文件类型
imgfile_path = str(Path(__file__).parent.joinpath("webfiles"))


@app.errorhandler(Exception)
def err(error):
    logger.error(f"[web]{error}")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/<htmlname>")
def html(htmlname):
    mimetype = mimetypes.guess_type(htmlname)[0]
    if mimetype is None:
        htmlname = htmlname + ".html"
    return render_template(htmlname)


@app.route('/favicon.ico')
def favicon():
    return send_file(os.path.join("static/img", "favicon.ico"))


@app.route("/api/files/<filename>", methods=["GET"])
def get_file(filename):
    mimetype = mimetypes.guess_type(filename)[0]
    logger.info(f"{request.remote_addr}请求文件{filename}类型:{mimetype}")
    file_path = f"{imgfile_path}/{filename}"
    logger.info(file_path)
    flask_file_path = os.path.join("webfiles", filename)
    if os.path.exists(file_path):
        try:
            response = jsonify({
                "filename": filename,
                "size": os.path.getsize(file_path),
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            })
            response.headers.set("Content-Type", "application/json")
            response.headers.set("Access-Control-Allow-Origin", "*")
            file = send_file(flask_file_path, mimetype=mimetype, as_attachment=True)
            return file

        except Exception as e:
            return jsonify({"error": str(e)})
    else:
        return jsonify({"error": "File not found"})


@app.route("/api/dinfo", methods=["GET"])
async def get_server_info():
    ip = request.remote_addr
    device = await get_server_state()
    json_str = json.dumps(device, default=lambda obj: obj.__dict__)
    logger.info(f"api/dinfo来自{ip}的请求发送{json_str}")
    response = jsonify(json_str)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/api/dau", methods=["GET"])
async def get_bot_dau():
    ip = request.remote_addr
    device = get_redis_data("chat_recorder")
    json_str = json.loads(device)
    logger.info(f"api/dau来自{ip}的请求发送{json_str}")
    response = jsonify(json_str)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/api/hypinfo", methods=["GET"])
async def get_hypinfo_info():
    name = request.args.get('name')
    if name is not None:
        uuid = uuid_get(name)
        if uuid is not None:
            ip = request.remote_addr
            key = get_redis_data("hyp_api_key")
            logger.info(key)
            device = hyp_info_get(key, uuid)
            logger.info(f"api/dinfo来自{ip}的请求发送{device}")
            response = jsonify(device)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


@app.route("/api/mcserver_state", methods=["GET"])
async def get_mcserver_state_web():
    ip = request.remote_addr
    device = await only_get_mcserver_state_from_redis()
    dic = [ast.literal_eval(x) for x in device]  # 使用列表推导式遍历列表并转换为字典
    logger.info(dic)
    json_str = json.dumps(dic, default=lambda obj: obj.__dict__)
    logger.info(f"api/mcserver_state来自{ip}的请求发送{json_str}")
    response = jsonify(json_str)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/api/skinhead/<name>", methods=["GET"])
async def get_skinhead(name):
    if name is not None:
        uuid = uuid_get(name)
        if uuid is not None:
            size = request.args.get('size')
            skins = get_skin(uuid)
            skin_url = skins[0]
            mc_skin_head = McskinHead()
            if size is None:
                size = 256
            elif int(size) > 1024:
                size = 1024
            buffer_img = await mc_skin_head.getimage(skin_url, int(size))
            if buffer_img is not None:
                return send_file(BytesIO(buffer_img[2]), mimetype='image/png', as_attachment=True,
                                 download_name=f"{uuid}.png")
            else:
                return None


@app.route("/api/mcserver_state_original/<ip>", methods=["GET"])
async def mcserver_state_original(ip):
    request_ip = request.remote_addr
    server_state = await get_mcserver_state_original(ip)
    if type(server_state) is not list:
        logger.info(server_state)
        response = jsonify(server_state)
        response.headers['Access-Control-Allow-Origin'] = '*'
        logger.info(f"api/mcserver_state_original来自{request_ip}的请求发送{ip}服务器信息")
        return response
    else:
        response = jsonify({
            "success": False,
            "reason": server_state[1],
            "server": ip,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        })
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = f"{imgfile_path}/{str(uuid.uuid4())}-cache.png"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'uploaded_file', filename, 201
    else:
        return 'Invalid file', 400


@app.route('/api/bf1weapons', methods=['GET'])
async def get_bf1weapons():
    name = request.args.get('name')
    weapons = await get_bf1_weapons_list(name)
    return jsonify(weapons)


@app.route('/api/bfvweapons', methods=['GET'])
async def get_bfvweapons():
    name = request.args.get('name')
    weapons = await get_bfv_weapons_list(name)
    return jsonify(weapons)


@app.route('/api/bf1vehicles', methods=['GET'])
async def get_bf1vehicles():
    name = request.args.get('name')
    weapons = await get_bf1_vehicles_list(name)
    return jsonify(weapons)


@app.route('/api/bfvvehicles', methods=['GET'])
async def get_bfvvehicles():
    name = request.args.get('name')
    weapons = await get_bfv_vehicles_list(name)
    return jsonify(weapons)


@app.route('/api/bf1classes', methods=['GET'])
async def get_bf1classes():
    name = request.args.get('name')
    weapons = await get_bf1_classes_list(name)
    return jsonify(weapons)


@app.route('/api/bfvclasses', methods=['GET'])
async def get_bfvclasses():
    name = request.args.get('name')
    weapons = await get_bfv_classes_list(name)
    return jsonify(weapons)


@app.route('/api/bf2042info', methods=['GET'])
async def get_bf2042info():
    name = request.args.get('name')
    weapons = await get_bf2042_info(name)
    return jsonify(weapons)


def run_flask():
    port = config_port
    app.run('0.0.0.0', port)
    logger.info(f"web服务器已经再0.0.0.0:{port}开放")
    flask_thread.join()
    if not flask_thread.isAlive():
        flask_thread.start()


flask_thread = threading.Thread(target=run_flask)
flask_thread.start()
