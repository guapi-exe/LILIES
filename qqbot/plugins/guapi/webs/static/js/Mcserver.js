async function load_server_state(ip) {
    return $.ajax({
        type: "get",
        url: `http://101.34.203.130:8099/api/mcserver_state_original/${ip}`,
        async: true,
        success: function (data) {
            console.log(JSON.parse(data))
            return JSON.parse(data)
        }, error: function (data) {
            console.log(`err${data}`)
        }
    });
}
function load_all(ip){
    load_server_state(ip).then(server=>{
        server = JSON.parse(server)
        let serverping
        let latency = server["latency"] || -1
        let version = server["version"]
        let version_name = version["name"]
        let version_protocol = version["protocol"]
        let motd = ''
        let icon
        if (server["icon"] == null){
            icon = "data:image/png;base64,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"
        }else {
            icon = server["icon"]
        }

        if(server["motd"]["raw"].hasOwnProperty("extra")){
            for(let motds in server["motd"]["raw"]["extra"]){
                let txt = server["motd"]["raw"]["extra"][motds]["text"].replace("\n", "<br>")
                let color = undefined
                if (!server["motd"]["raw"]["extra"][motds]["color"]){
                    color = undefined
                }else {
                    color = server["motd"]["raw"]["extra"][motds]["color"].replace(/dark_([a-z]+)/g, "dark$1")
                }
                motd +=(`<span style="color: ${color}">${txt}`)
            }
        }else if (server["motd"]["raw"].hasOwnProperty("text")){
            motd = motdtocolor(server["motd"]["raw"]["text"])
        }else  if (server["motd"]["raw"].hasOwnProperty("translate")){
            motd = motdtocolor(server["motd"]["raw"]["translate"])
        }
        else {
            motd = motdtocolor(server["motd"]["raw"])
        }
        let mods
        let mod_type
        if(server["raw"].hasOwnProperty("modinfo")){
            mods = server["raw"]["modinfo"]["modList"] ? server["raw"]["modinfo"]["modList"].length : 0
            mod_type = server["raw"]["modinfo"]["type"] || "未知"
        }else {
            mods = 0
            mod_type = "无mod加载器"
        }
        let online_players = server["players"]["online"]
        let online_max = server["players"]["max"]
        if (latency == -1){
            serverping = `
                <div class="signal">
                    <span>-1ms</span>
                    <div class="block red" style="background-color: red"></div>
                    <div class="block orange" style="background-color: red"></div>
                    <div class="block yellow" style="background-color: red"></div>
                    <div class="block lime" style="background-color: red"></div>
                    <div class="block green" style="background-color: red"></div>
                </div>
                `
        } else if(latency <= 60){
            serverping = `
                <div class="signal">
                    <span>${Math.ceil(latency)}ms</span>
                    <div class="block red" style="background-color: green"></div>
                    <div class="block orange" style="background-color: green"></div>
                    <div class="block yellow" style="background-color: green"></div>
                    <div class="block lime" style="background-color: green"></div>
                    <div class="block green" style="background-color: green"></div>
                </div>
                `
        } else if(latency <= 120){
            serverping = `
                <div class="signal">
                    <span>${Math.ceil(latency)}ms</span>
                    <div class="block red" style="background-color: green"></div>
                    <div class="block orange" style="background-color: green"></div>
                    <div class="block yellow" style="background-color: green"></div>
                    <div class="block lime" style="background-color: green"></div>
                    <div class="block green" style="background-color: red"></div>
                </div>
                `
        } else if(latency <= 180){
            serverping = `
                <div class="signal">
                    <span>${Math.ceil(latency)}ms</span>
                    <div class="block red" style="background-color: green"></div>
                    <div class="block orange" style="background-color: green"></div>
                    <div class="block yellow" style="background-color: green"></div>
                    <div class="block lime" style="background-color: red"></div>
                    <div class="block green" style="background-color: red"></div>
                </div>
                `
        } else if(latency <= 240){
            serverping = `
                <div class="signal">
                    <span>${Math.ceil(latency)}ms</span>
                    <div class="block red" style="background-color: green"></div>
                    <div class="block orange" style="background-color: green"></div>
                    <div class="block yellow" style="background-color: red"></div>
                    <div class="block lime" style="background-color: red"></div>
                    <div class="block green" style="background-color: red"></div>
                </div>
                `
        } else{
            serverping = `
                <div class="signal">
                    <span>${Math.ceil(latency)}ms</span>
                    <div class="block red" style="background-color: green"></div>
                    <div class="block orange" style="background-color: red"></div>
                    <div class="block yellow" style="background-color: red"></div>
                    <div class="block lime" style="background-color: red"></div>
                    <div class="block green" style="background-color: red"></div>
                </div>
                `
        }
        let box = $('#main')
        let serverbox = $(`
            <div class="divbox">
        <div class="container">
            <img src="${icon}">
            <div class="divtitle">
                <span>服务器:${ip}</span>
            </div>
            ${serverping}
        </div>

    </div>
    <div class="divbox">
        <div class="container">
            <div class="motd">
                ${motd}
            </div>
        </div>
    </div>
    <div class="divbox">
        <div class="container">
            <div class="divtitle">
                <span>版本:${version_name} protocol:${version_protocol}</span>
                <span>模组加载方式:${mod_type}</span>
                <span>共计加载mod:${mods}</span>
            </div>
        </div>
    </div>
    <div class="divbox">
        <div class="container">
            <div class="divtitle">
                <span>当前在线${online_players}/${online_max}</span>
            </div>
        </div>
        <ul id="players">
        </ul>
    </div>
    <div class="divbox">
        <div class="container">
            <div class="divtitle">
                <span>Plugins by guapi</span>
            </div>
        </div>
    </div>
        `)
        box.append(serverbox)
        if(server["players"]["sample"] != null){
            if(server["players"]["sample"].length > 0){
                let player_ul = $(`#players`)
                for(let player in server["players"]["sample"]){
                    let player_li = $(`
                            <li>
                                <img src="http://101.34.203.130:8099/api/skinhead/${server["players"]["sample"][player]["name"]}?size=1024" alt="">
                                <div class="divtext">
                                    <span>name:${server["players"]["sample"][player]["name"]}</span>
                                    <span>uuid:${server["players"]["sample"][player]["id"]}</span>
                                </div>
                            </li>
                        `)
                    player_ul.append(player_li)
                }
            }
        }
    })
}

let web_url = window.location.href;
const url = new URL(web_url);
const params = new URLSearchParams(url.search);
const ip = params.get('ip');
load_all(ip)