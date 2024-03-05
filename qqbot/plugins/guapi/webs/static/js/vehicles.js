async function load_info(url) {
    return $.ajax({
        type: "get",
        url: url,
        async: true,
        success: function (data) {
            console.log(data)
            return data
        }, error: function (data) {
            console.log(`err${data}`)
        }
    });
}
function reload_header(name, type){
    let url
    if(type == "bfv" || type == "bf1"){
        url = `https://api.gametools.network/${type}/stats/?format_values=true&name=${name}&lang=zh-cn`
    }else {
        url = `http://127.0.0.1:8099/api/bf2042info?name=${name}`
    }
    load_info(url).then(data=>{
        if(type == "bf2042"){
            data = data["row"]
        }
        let avatar = data["avatar"]
        let rank
        if(type == "bf2042"){
            rank = 0
        }else {
            rank = data["rank"]
        }
        let rankImg = data["rankImg"]
        let header =
            `<div data-v="" class="flex">
        <div data-v="" class="title" >
            <div data-v="" class="flex flex-col">
                <div data-v="" class="details">
                    <img src=${avatar} alt="Profile image">
                    <div>
                        <div data-v="" class="flex">
                            <div data-v="" class="title">
                                <div data-v="" class="flex flex-col">
                                    <div data-v="" class="details hasControls hasIcon">
                                        <div  class="platform-status" data-v-tooltip="">
                                            <svg data-v-15460bde="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 32" class="background">
                                                <circle cx="16" cy="16" r="16" style="opacity: 0.15;"></circle>
                                            </svg>
                                            <svg data-v-15460bde="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 36 32" class="background">
                                                <circle cx="16" cy="16" r="16" style="opacity: 0.15;"></circle>
                                            </svg>
                                            <svg  xmlns="http://www.w3.org/2000/svg" viewBox="0 0 190.377 255.763" class="platform-icon platform-origin icon">
                                                <path d="M89.961 91.054a37.345 37.345 0 0 0-25.682 16.123 36.564 36.564 0 0 0-6.25 20.158 36.6 36.6 0 0 0 10.145 26.078 37.169 37.169 0 0 0 62.566-14.685c4.721-14.55-.938-31.594-13.265-40.584a37.072 37.072 0 0 0-27.514-7.09m.976-90.71a2.781 2.781 0 0 1 3.966 1.421c.521 1.34-.38 2.566-1.118 3.6a63.112 63.112 0 0 0-10.329 24.913 1.9 1.9 0 0 0-.971 2.447c.488.179.982.337 1.481.488a102.673 102.673 0 0 1 30.407 1.427 94.74 94.74 0 0 1 48.188 25.985 95.214 95.214 0 0 1 25.829 47.881 95.626 95.626 0 0 1-6.385 58.475 197.822 197.822 0 0 1-82.486 88.426c-1.156.538-2.821.559-3.612-.591a3.264 3.264 0 0 1 .374-4.015 62.558 62.558 0 0 0 10.041-22.579 17.706 17.706 0 0 0 .689-5.1c-.592-.77-1.568-.537-2.4-.509a95.261 95.261 0 0 1-51.005-9.049 95.371 95.371 0 0 1-40.56-37.486A94.19 94.19 0 0 1 .016 126.76a95.517 95.517 0 0 1 11.966-45.325A197.216 197.216 0 0 1 90.937.344"></path>
                                            </svg>
                                        </div>
                                        <h2>Rank ${rank}</h2>
                                        <img data-v-3="" class="img" src=${rankImg} alt="">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <h2>${name}</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>`
        let header_box = $(`#header`)
        header_box.append(header)
    })

}
function reload_weapons(url, type){
    load_info(url).then(data=>{
        console.log(data)
        if(type == "bf2042"){
            data = data["vehicles"]
        }
        let weapons_html = ``
        let weapons_best_html = ``
        for(let weapon in data){
            let name = data[weapon]["vehicleName"]
            let type = data[weapon]["type"]
            let kills = data[weapon]["kills"]
            let kpm = data[weapon]["killsPerMinute"]
            let image = data[weapon]["image"]
            let destroyed = data[weapon]["destroyed"]
            let timeIn = data[weapon]["timeIn"]
            if (weapon == 0 ){
                weapons_best_html =
                    `<div data-v="" class="flex">
        <div data-v="" class="title">
            <div data-v="" class="flex flex-col">
                <div data-v="" class="details hasControls hasIcon">
                    <h2 data-v="">常用载具</h2>
                    <div data-v="" class="title-stats">
                        <span data-v="" class="playtime">
                            <svg data-v="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 19.949 19.97">
                                <path d="M10.95 0v2.02a8 8 0 0 1 0 15.88v2a10 10 0 0 0 0-19.9m-2 .03a9.827 9.827 0 0 0-5.33 2.2l1.43 1.48a8 8 0 0 1 3.9-1.68v-2M2.21 3.64A9.885 9.885 0 0 0 0 8.97h2a8.017 8.017 0 0 1 1.64-3.9L2.21 3.64m-2.2 7.33a10.039 10.039 0 0 0 2.21 5.33l1.42-1.43a8 8 0 0 1-1.63-3.9h-2m5.04 5.37-1.43 1.37a9.994 9.994 0 0 0 5.33 2.26v-2a8 8 0 0 1-3.9-1.63m5.4-11.37v5.25l4.5 2.67-.75 1.23-5.25-3.15v-6Z">
                                </path>
                            </svg>
                            ${(timeIn/3600).toFixed(0)}h 游玩时长
                        </span><!----><!---->
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div data-v-2="" class="segment-used__top" style="--hero-image-url: url(https://trackercdn.com/cdn/tracker.gg/bfv/weapon-bg.jpg);">
        <div data-v-2="" class="segment-used__top-details">
            <img data-v-2="" class="segment-used__top-image" src=${image}>
            <span data-v-2="" class="name">${name}</span>
        </div>
        <div data-v="" class="main">
            <div data-v-1="" data-v="" class="stat align-left expandable">
                <div data-v-1="" class="wrapper">
                    <div data-v-1="" class="numbers">
                        <span data-v-1="" class="name" title="Score/Min">KPM</span>
                        <span data-v-1="" class="flex items-center gap-2">
                        <span data-v-1="" class="value">${kpm}</span>
                    </span>
                    </div>
                </div>
            </div>
            <div data-v-1="" data-v="" class="stat align-left expandable">
                <div data-v-1="" class="wrapper">
                    <div data-v-1="" class="numbers">
                        <span data-v-1="" class="name" title="Score/Min">击杀</span>
                        <span data-v-1="" class="flex items-center gap-2">
                        <span data-v-1="" class="value">${kills}</span>
                    </span>
                    </div>
                </div>
            </div>
            <div data-v-1="" data-v="" class="stat align-left expandable">
                <div data-v-1="" class="wrapper">
                    <div data-v-1="" class="numbers">
                        <span data-v-1="" class="name" title="Score/Min">种类</span>
                        <span data-v-1="" class="flex items-center gap-2">
                        <span data-v-1="" class="value">${type}</span>
                    </span>
                    </div>
                </div>
            </div>
            <div data-v-1="" data-v="" class="stat align-left expandable">
                <div data-v-1="" class="wrapper">
                    <div data-v-1="" class="numbers">
                        <span data-v-1="" class="name" title="Score/Min">摧毁</span>
                        <span data-v-1="" class="flex items-center gap-2">
                        <span data-v-1="" class="value">${destroyed}</span>
                    </span>
                    </div>
                </div>
            </div>
        </div>
    </div>`
            }
            weapons_html +=
                `<div class="column">
                        <div class="row">
                            <h4 class="name">${name}</h4>
                            <img src=${image} loading="lazy" alt="">
                        </div>

                        <div class="row">
                            <p class="name">击杀</p>
                            <h4 class="value">${kills}</h4>

                        </div>
                        <div class="row">
                            <p class="name">KPM</p>
                            <h4 class="value">${kpm}</h4>

                        </div>
                        <div class="row">
                            <p class="name">摧毁数量</p>
                            <h4 class="value">${destroyed}</h4>

                        </div>
                        <div class="row">
                            <p class="name">使用时间</p>
                            <h4 class="value">${(timeIn/3600).toFixed(2)}h</h4>

                        </div>
                    </div>`
        }
        let weapons_body =
            `<div data-v="" class="flex">
        <div data-v="" class="title">
            <div data-v="" class="flex flex-col">
                <div data-v="" class="details hasControls hasIcon">
                    <h2 data-v="">载具</h2>
                    <div data-v="" class="title-stats">
                        <span data-v="" class="playtime">
                            <svg data-v-46905b7a="" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 21.977 32" class="icon">
                                <path d="m19.877 19.593 1.975-.311a11.017 11.017 0 0 0-.557-2.126l-1.874.7a8.986 8.986 0 0 1 .456 1.737ZM19.978 21.389a9.068 9.068 0 0 1-.254 1.778l1.941.479a11.081 11.081 0 0 0 .311-2.173Z"></path>
                                <path d="M10.987 30a9 9 0 1 1 7.639-13.757l1.7-1.058a11.167 11.167 0 0 0-1.339-1.709V0h-16v13.474a10.993 10.993 0 1 0 17.942 12.24l-1.806-.858A9.049 9.049 0 0 1 10.987 30Zm4-28h2v9.8a10.869 10.869 0 0 0-2-1.044Zm-6 0h4v8.2a10.328 10.328 0 0 0-4-.009Zm-4 0h2v8.764a10.975 10.975 0 0 0-2 1.028Z"></path>
                                <path d="m13.195 18.461-2.209-4.475-2.209 4.475-4.94.718 3.574 3.484-.843 4.92 4.418-2.322 4.418 2.322-.843-4.92 3.574-3.484Zm-.447 5.466L10.986 23l-1.762.926.337-1.961-1.426-1.391 1.97-.286.881-1.783.881 1.784 1.97.286-1.426 1.391Z"></path>
                            </svg>
                            全部载具
                        </span><!----><!---->
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="list">
        <div class="box-list">
            <div class="wrap ">
                <div class="inner" style="align-items: stretch;">
                ${weapons_html}
                </div>
            </div>
        </div>
    </div>`
        let weapons_box = $(`#weapons`)
        let weapons_best_box = $(`#weapons_best_one`)
        weapons_best_box.append(weapons_best_html)
        weapons_box.append(weapons_body)


    })
}
let web_url = window.location.href;
const url = new URL(web_url);
const params = new URLSearchParams(url.search);
const name = params.get('name');
const type = params.get('type')

function reload_all(name,type){
    console.log(name,type)
    let weapons_url
    if(type == "bfv"){
        weapons_url = `http://127.0.0.1:8099/api/bfvvehicles?name=${name}`
    }else if (type == "bf1"){
        weapons_url = `http://127.0.0.1:8099/api/bf1vehicles?name=${name}`
    }else if (type == "bf2042"){
        weapons_url = `http://127.0.0.1:8099/api/bf2042info?name=${name}`
    }
    reload_weapons(weapons_url,type)
    reload_header(name,type)
}
reload_all(name,type)