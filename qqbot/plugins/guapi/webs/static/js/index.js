let server_state = load_server_state()
let time
let cpuChart
let memChart
let netChart
let diskChart
async function load_server_state() {
    return await $.ajax({
        type: "get",
        url: "http://101.34.203.130:8099/api/dinfo",
        async: true,
        success: function (data) {
            console.log(JSON.parse(data))
            return JSON.parse(data)
        }, error: function (data) {
            console.log(`err${data}`)
        }
    });
}


function createChart(element, config) {
    return new Chart(element, config);
}
function updateProgress(progress, text, value, target) {
    var perimeter = Math.PI * 2 * 75;
    progress.style.strokeDasharray = perimeter * value / 100 + " " + perimeter * (1 - value / 100);
    text.textContent = value + "%";
    if (value != target) {
        if (value < target) {
            value+=1;
        } else {
            value-=1;
        }
        requestAnimationFrame(function() {
            updateProgress(progress, text, value, target);
        });
    }
}


async function updateChartData() {

    server_state = await load_server_state()
    server_state = JSON.parse(server_state)
    console.log(server_state)
    let cpumodel= server_state["cpumodel"]
    let cpu_percent= server_state["cpu_percent"]
    let cpu_percent_list= server_state["cpu_percent_list"]
    let cpu_count= server_state["cpu_count"]
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


    let Diskchartconfig = {
        type: 'pie',
        data: {
            labels: [
                '剩余',
                '占用',
            ],
            datasets: [{
                label: '存储',
                data: [disk_free, disk_total-disk_free ],
                backgroundColor: [
                    'rgb(255, 99, 132)',
                    'rgb(54, 162, 235)'
                ],
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left:1000,
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
                    left: 850,
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
                    left: 850,
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
                data: net_recv_list,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },{
                label: '网络下载',
                data: net_send_list,
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
    diskChart.data.datasets[0].data = Diskchartconfig.data.datasets[0].data
    cpuChart.data.labels = CpuchartConfig.data.labels
    cpuChart.data.datasets[0].data = CpuchartConfig.data.datasets[0].data
    memChart.data.labels = MemchartConfig.data.labels
    memChart.data.datasets[0].data = MemchartConfig.data.datasets[0].data
    netChart.data.labels = NetchartConfig.data.labels
    netChart.data.datasets[0].data = NetchartConfig.data.datasets[0].data
    netChart.data.datasets[1].data = NetchartConfig.data.datasets[1].data
    cpuChart.update()
    memChart.update()
    netChart.update()
    diskChart.update()
    console.log(`${cpu_percent}|${mem_percent}`)
    updateProgress(document.getElementById("memcircle"), document.getElementById("memtext"), 0, Number.parseInt(mem_percent));
    updateProgress(document.getElementById("cpucircle"), document.getElementById("cputext"), 0, Number.parseInt(cpu_percent));
     document.getElementById('disk_total').textContent = "内存总量:" + disk_total.toFixed(2) + "GB"
     document.getElementById("disk_free").textContent = "剩余可用:" + disk_free.toFixed(2)+ "GB"
     document.getElementById("disk_percent").textContent = "已存储占比:" + disk_percent.toFixed(2)+ "%"
     document.getElementById("cpu_percent").textContent = "cpu占用:" + cpu_percent.toFixed(2)+ "%"
     document.getElementById("cpu_count").textContent = "cpu线程数:" + cpu_count
     document.getElementById("cpu_current").textContent = "cpu基准:" + cpu_current.toFixed(2)+ "Ghz"
     document.getElementById("mem_percent").textContent = "内存占用:" + mem_percent.toFixed(2)+ "%"
     document.getElementById("mem_total").textContent = "内存总量:" + mem_total.toFixed(2)+ "GB"
     document.getElementById("mem_available").textContent = "可用内存:" + mem_available.toFixed(2)+ "GB"
}

setInterval(updateChartData, 1000*65);
updateChartData();
