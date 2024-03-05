let dinfo = "http://127.0.0.1:8099/api/dinfo"
let bot_dau = "http://127.0.0.1:8099/api/dau"
let server_state = load_server_state()
let bot_state = load_bot_state()
let time
let cpuChart
let memChart
let netChart
let diskChart
function createChart(element, config) {
    return new Chart(element, config);
}
async function load_server_state() {
    return await $.ajax({
        type: "get",
        url: dinfo,
        async: true,
        success: function (data) {
            console.log(JSON.parse(data))
            return JSON.parse(data)
        }, error: function (data) {
            console.log(`err${data}`)
        }
    });
}

async function load_bot_state() {
    return await $.ajax({
        type: "get",
        url: bot_dau,
        async: true,
        success: function (data) {
            console.log(data)
            return data
        }, error: function (data) {
            console.log(`err${data}`)
        }
    });
}

function update_cpu_box(cpu_percent, cpu_count, cpu_current, cpumodel){
    let num = ((cpu_percent/100) * 360).toFixed(0)
    console.log(num)
    let color = 'var(--low-color)'
    if (cpu_percent/100 >= 0.9) {
        color = 'var(--high-color)'
    } else if (cpu_percent/100 >= 0.8) {
        color = 'var(--medium-color)'
    }
    let leftCircle = `style="transform:rotate(-180deg);background:${color};"`
    let rightCircle = `style="transform:rotate(360deg);background:${color};"`
    if (num > 180) {
        leftCircle = `style="transform:rotate(${num}deg);background:${color};"`
    } else {
        rightCircle = `style="transform:rotate(-${180 - num}deg);background:${color};"`
    }
    let cpubox =
        `<li class="li">
            <div class="cpu">
                <div class="left" >
                    <div class="left-circle" ${leftCircle}>
                    </div>
                </div>
                <div class="right">
                    <div class="right-circle" ${rightCircle}>
                    </div>
                </div>
                <div class="inner">
                    ${cpu_percent.toFixed(0)}%
                </div>
            </div>
            <article>
                <summary>CPU</summary>
                <p>cpu基准频率:${cpu_current.toFixed(2)}Ghz</p>
                <p>占用:${cpu_percent.toFixed(2)}%</p>
                <p>cpu线程数:${cpu_count}</p>
            </article>
        </li>`
    return cpubox
}
function update_cores_cpu_box(cpu_cores_percent, mem_total, cpu_count){
    let cpu_list = ``
    for (let cpu in cpu_cores_percent){
        if (cpu > 4){
            break
        }
        let color = 'var(--low-color)'
        if (cpu_cores_percent[cpu]["Cpu"]/(100*cpu_count) >= 0.75) {
            color = 'var(--high-color)'
        } else if (cpu_cores_percent[cpu]["Cpu"]/(100*cpu_count) >= 0.5) {
            color = 'var(--medium-color)'
        }
        let cpu_percent
        if (cpu_cores_percent[cpu]["Cpu"] > 100){
            cpu_percent = cpu_cores_percent[cpu]["Cpu"]
        }else {
            cpu_percent = cpu_cores_percent[cpu]["Cpu"]
        }
        cpu_list +=
        `
            <li class="HardDisk_li">
                <div class="word mount">${cpu_cores_percent[cpu]["PID"]}</div>
                <div class="percentage">CPU</div>
                <div class="progress">
                    <div class="word center">${Number(cpu_cores_percent[cpu]["Cpu"]).toFixed(2)}%</div>
                    <div class="current" style="width:${(Number(cpu_percent)/cpu_count).toFixed(2)}%;background:${color}"></div>
                </div>
                <div class="percentage">内存</div>
                <div class="progress">
                    <div class="word center">${Number(cpu_cores_percent[cpu]["MeM"]).toFixed(2)}% | ${(mem_total * (Number(cpu_cores_percent[cpu]["MeM"]))/100).toFixed(2)}GB</div>
                    <div class="current" style="width:${Number(cpu_cores_percent[cpu]["MeM"]).toFixed(2)}%;background:var(--medium-color)"></div>
                </div>
                <div class="mount">${cpu_cores_percent[cpu]["Name"]}</div>
            </li>
        `
    }
    let cpu_core_box = `
                        <ul>
                            <div class="speed">
                                <p>PID</p>
                                <p>程序名</p>
                            </div>
                            ${cpu_list}
                        </ul>
                        `
    return cpu_core_box

}
function update_ram_box(mem_total, mem_percent, mem_available){
    let num = ((mem_percent/100) * 360).toFixed(0)
    console.log(num)
    let color = 'var(--low-color)'
    if (mem_percent/100 >= 0.9) {
        color = 'var(--high-color)'
    } else if (mem_percent/100 >= 0.8) {
        color = 'var(--medium-color)'
    }
    let leftCircle = `style="transform:rotate(-180deg);background:${color};"`
    let rightCircle = `style="transform:rotate(360deg);background:${color};"`
    if (num > 180) {
        leftCircle = `style="transform:rotate(${num}deg);background:${color};"`
    } else {
        rightCircle = `style="transform:rotate(-${180 - num}deg);background:${color};"`
    }
    let rambox = `
        <li class="li">
            <div class="cpu">
                <div class="left">
                    <div class="left-circle" ${leftCircle}>
                    </div>
                </div>
                <div class="right">
                    <div class="right-circle" ${rightCircle}>
                    </div>
                </div>
                <div class="inner">
                    ${mem_percent.toFixed(0)}%
                </div>
            </div>
            <article>
                <summary>RAM</summary>
                <p>内存总量:${mem_total.toFixed(2)}GB</p>
                <p>内存占用:${mem_percent.toFixed(2)}%</p>
                <p>可用内存:${mem_available.toFixed(2)}GB</p>
            </article>
        </li>`
    return rambox
}
function update_disk_box(disk_total, disk_free, disk_percent){
   let diskbox = `
        <li class="li">
            <div style="height: 100px; width: 100px">
                <canvas id="diskChart" style="display: block; box-sizing: border-box; height: 100px; width: 100px;"></canvas>
            </div>
            <article>
                <summary>存储</summary>
                <p>存储占用:${disk_percent.toFixed(2)}%</p>
                <p>剩余可用:${disk_free.toFixed(2)}GB</p>
                <p>存储总量:${disk_total.toFixed(2)}GB</p>
            </article>
        </li>`
    return diskbox
}
function update_header(Avatar, dau, messages){
    let botinfo = `
    <div class="tb">
        <div class="avatar">
            <img src="${Avatar}"
                 onerror="this.src= '${Avatar}'; this.onerror = null;">
        </div>
        <div class="header">
            <h1>LILIES</h1>
            <hr noshade>
            <p>简介:mindustry，MC，github</p>
            <p>今日DAU:${dau}</p>
            <p>今日接收消息数:${messages},发送消息数:${messages}</p>
        </div>
    </div>`
    return botinfo
}

function update_end(net_send, net_recv, cpumodel){
    let endbox = `
        <div class="speed">
            <p>平台</p>
            <p>Linux</p>
        </div>
        <div class="speed">
            <p>作者</p>
            <p>guapi</p>
        </div>
        <div class="speed">
            <p>NetIO</p>
            <p>上传${net_send.toFixed(2)}Mbps↑下载${net_recv.toFixed(2)}Mbps↓</p>
        </div>
        <div class="speed">
            <p>CPU</p>
            <p>${cpumodel}</p>
        </div>
    `
    return endbox
}

function update_charts(disk_free, disk_total,time_list,cpu_percent_list,mem_percent_list,net_recv_list,net_send_list){
    let Diskchartconfig = {
        type: 'pie',
        data: {
            datasets: [{
                label: '存储',
                data: [disk_free, disk_total-disk_free ],
                backgroundColor: [
                    'rgb(54, 162, 235)',
                    'rgb(255, 99, 132)'
                ],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left:0,
                    right: 0
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    };
    let CpuchartConfig = {
        type: 'line',
        data: {
            labels: time_list, // 设置X轴的标签，初始为空
            datasets: [{
                label: '', // 设置图表的标签，初始为空
                data: cpu_percent_list,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            maintainAspectRatio: true,
            responsive: true,
            layout: {
                padding: {
                    left: 0,
                    right: 0
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        //display:false
                    },
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: false,
                        text: '时间'
                    }
                },
                y: {
                    //display: false,
                    beginAtZero: true,
                    grid: {
                        //display:false
                    },
                    title: {
                        display: true,
                        text: '百分比'
                    }
                }
            }
        }
    };
    let MemchartConfig = {
        type: 'line',
        data: {
            labels: time_list, // 设置X轴的标签，初始为空
            datasets: [{
                label: '', // 设置图表的标签，初始为空
                data: mem_percent_list,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            maintainAspectRatio: true,
            responsive: true,
            layout: {
                padding: {
                    left: 0,
                    right: 0
                }
            },
            scales: {
                x: {
                    display: true,
                    grid: {
                        //display:false
                    },
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: false,
                        text: '时间'
                    }
                },
                y: {
                    //display: false,
                    beginAtZero: true,
                    grid: {
                        //display:false
                    },
                    title: {
                        display: true,
                        text: '百分比'
                    }
                }
            }
        }
    };
    let NetchartConfig = {
        type: 'line',
        data: {
            labels: time_list, // 设置X轴的标签，初始为空
            datasets: [{
                label: '网络上传',
                data: net_send_list,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },{
                label: '网络下载',
                data: net_recv_list,
                fill: false,
                borderColor: 'rgb(192,75,79)',
                tension: 0.1
            }]
        } ,
        options: {
            naintainAspectRatio: true,
            responsive: true,
            layout: {
                padding: {
                    right: 0
                }
            },
            scales: {
                x: {
                    display: true,
                    time: {
                        unit: 'second'
                    },
                    title: {
                        display: false,
                        text: '时间'
                    }
                },
                y: {
                    //display: true,
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Mbps'
                    }
                }
            }
        }
    };
    CpuchartConfig.data.datasets[0].label = 'CPU占用率'; // 设置图表的标签
    MemchartConfig.data.datasets[0].label = '内存占用率'; // 设置图表的标签

    if (!cpuChart || !memChart || !netChart || !diskChart){
        cpuChart = createChart(document.getElementById('cpuChart'), CpuchartConfig);
        memChart = createChart(document.getElementById('memChart'), MemchartConfig);
        netChart = createChart(document.getElementById('netChart'), NetchartConfig);
        diskChart = createChart(document.getElementById('diskChart'), Diskchartconfig);
    }

}
async function update_all(){
    server_state = await load_server_state()
    server_state = JSON.parse(server_state)
    bot_state = await load_bot_state()
    let defaultAvatar = "https://bot-resource-1251316161.file.myqcloud.com/avatar/b1c84c84-2f88-496a-bd54-2c781b6c0c9f3666422688431467466?ts=1699511422"
    let cpumodel= server_state["cpumodel"]
    let cpu_percent= server_state["cpu_percent"]
    let cpu_cores_percent = server_state["cpu_core_percent"]
    let cpu_percent_list= server_state["cpu_percent_list"]
    let cpu_count= server_state["cpu_count"]
    let top_list = server_state["top_list"]
    let cpu_current= server_state["cpu_current"]
    let mem_percent= server_state["mem_percent"]
    let mem_available= server_state["mem_available"]
    let mem_total= server_state["mem_total"]
    let mem_percent_list= server_state["mem_percent_list"]
    let disk_total= server_state["disk_total"]
    let disk_free= server_state["disk_free"]
    let disk_percent= server_state["disk_percent"]
    let net_send= server_state["net_send"]
    let net_recv= server_state["net_recv"]
    let net_send_list= server_state["net_send_list"]
    let net_recv_list= server_state["net_recv_list"]
    let time_list= server_state["time_list"]
    let dau = bot_state["dau"]
    let messages = bot_state["day_messages"]
    let header = update_header(defaultAvatar,dau,messages)
    let cpu = update_cpu_box(cpu_percent,cpu_count,cpu_current)
    let ram = update_ram_box(mem_total,mem_percent,mem_available)
    let disk = update_disk_box(disk_total,disk_free,disk_percent)
    let end = update_end(net_send,net_recv,cpumodel)
    let cpu_list = update_cores_cpu_box(top_list, mem_total, cpu_count)
    let header_box = $("#BotInfo")
    let end_box = $("#end")
    let cpu_list_box = $("#cpulist")
    header_box.append($(header))
    let ul_box = $("#info")
    ul_box.append(cpu)
    ul_box.append(ram)
    ul_box.append(disk)
    end_box.append(end)
    cpu_list_box.append(cpu_list)
    update_charts(disk_free, disk_total, time_list, cpu_percent_list, mem_percent_list, net_recv_list, net_send_list)
}

update_all()

