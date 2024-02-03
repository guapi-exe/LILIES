let server_state
async function load_server_state() {
    return $.ajax({
        type: "get",
        url: "http://127.0.0.1:8099/api/mcserver_state",
        async: true,
        success: function (data) {
            console.log(JSON.parse(data))
            return JSON.parse(data)
        }, error: function (data) {
            console.log(`err${data}`)
        }
    });
}
function CreateMcserverbox(imgdata, motd, ip, version, player, playerlist, ping){
    let column = document.createElement("div")
    column.setAttribute("class", "column");
    column.setAttribute("id", ip);
    let divtext = document.createElement("div")
    divtext.setAttribute("class", "divtext");
    let img = document.createElement("img");
    img.setAttribute("src", imgdata);
    img.setAttribute("class", "icon");
    let divdata = document.createElement("div")
    divdata.setAttribute("class", "data");
    let ipdata = document.createElement("span")
    let playerlistdata = document.createElement("span")
    let signal = document.createElement("div")
    signal.setAttribute("class", "signal");
    let pingms = document.createElement("span")
    pingms.textContent = `[${player}]${ping}ms`
    let green = document.createElement("div")
    green.setAttribute("class", "block green")
    let lime = document.createElement("div")
    lime.setAttribute("class", "block lime")
    let yellow = document.createElement("div")
    yellow.setAttribute("class", "block yellow")
    let orange = document.createElement("div")
    orange.setAttribute("class", "block orange")
    let red = document.createElement("div")
    red.setAttribute("class", "block red")
    let mtoddiv = document.createElement("div")
    let server = document.createElement("div")
    server.setAttribute("class", "server")
    mtoddiv.setAttribute("class", "motd")
    ipdata.textContent = `服务器:${ip}[${version}]`

    let newplayerlist = ""
    for (player in playerlist){
        newplayerlist += `[${playerlist[player]}]`
    }
    if(newplayerlist != undefined){
        console.log(newplayerlist)
        playerlistdata.textContent = newplayerlist
    }
    if (ping == -1){
        green.setAttribute("style", "background-color: red")
        lime.setAttribute("style", "background-color: red")
        yellow.setAttribute("style", "background-color: red")
        orange.setAttribute("style", "background-color: red")
        red.setAttribute("style", "background-color: red")
    } else if(ping <= 60){

    } else if(ping <= 120){
        green.setAttribute("style", "background-color: red")
    } else if(ping <= 180){
        green.setAttribute("style", "background-color: red")
        lime.setAttribute("style", "background-color: red")
    } else if(ping <= 240){
        green.setAttribute("style", "background-color: red")
        lime.setAttribute("style", "background-color: red")
        yellow.setAttribute("style", "background-color: red")
    } else{
        green.setAttribute("style", "background-color: red")
        lime.setAttribute("style", "background-color: red")
        yellow.setAttribute("style", "background-color: red")
        orange.setAttribute("style", "background-color: red")
    }
    console.log(typeof motd)
    if(!motd[0].hasOwnProperty("raw") && typeof motd == "object"){
        for(let motds in motd){
            let txt = motd[motds]["text"].replace("\n", "<br>")
            let color = undefined
            if (!motd[motds]["color"]){
                color = undefined
            }else {
                color = motd[motds]["color"].replace(/dark_([a-z]+)/g, "dark$1")
            }
            let span = document.createElement('span')
            Object.assign(span.style, {
                color: color
            });
            span.innerHTML = txt
            mtoddiv.appendChild(span)
        }
    }else{
        if (typeof motd == "object"){
            mtoddiv.innerHTML = motdtocolor(motd[0]["raw"])
        }else {
            mtoddiv.innerHTML = ''
        }
    }
    server.appendChild(ipdata)

    signal.appendChild(pingms)
    signal.appendChild(green)
    signal.appendChild(lime)
    signal.appendChild(yellow)
    signal.appendChild(orange)
    signal.appendChild(red)

    divdata.appendChild(server)
    divdata.appendChild(mtoddiv)
    divdata.appendChild(playerlistdata)

    divtext.appendChild(img)
    divtext.appendChild(divdata)
    divtext.appendChild(signal)

    column.appendChild(divtext);
    let container = document.getElementById("Mclist");
    if (document.getElementById(`${ip}`)) {
        let element = document.getElementById(`${ip}`);
        element.parentNode.removeChild(element);
        container.appendChild(column);
    } else {
        container.appendChild(column);
    }


}
async function update_mcstate(){
    server_state = await load_server_state()
    server_state = JSON.parse(server_state)
    for (let server in server_state){
        if(server_state[server]["server_online"]) {
            let base64
            if (!server_state[server]["server_favicon"]) base64 = "data:image/png;base64,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"
            else base64 = server_state[server]["server_favicon"]
            CreateMcserverbox(base64, server_state[server]["server_motd"], server_state[server]["server_ip"], server_state[server]["server_version"],
                `${server_state[server]["player_online"]}/${server_state[server]["player_max"]}`, server_state[server]["player_list"], server_state[server]["server_ping"]
            )
        }else {
            let base64 = "data:image/png;base64,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"
            CreateMcserverbox(base64, "无法连接至服务器", server_state[server]["server_ip"], "离线",
                ``, [], server_state[server]["server_ping"]
            )
        }
    }


}
setInterval(update_mcstate, 1000*60*5);
update_mcstate()