

const skinParts = ["head", "body", "rightArm", "leftArm", "rightLeg", "leftLeg"];
const skinLayers = ["innerLayer", "outerLayer"];
const availableAnimations = {
    idle: new skinview3d.IdleAnimation(),
    walk: new skinview3d.WalkingAnimation(),
    run: new skinview3d.RunningAnimation(),
    fly: new skinview3d.FlyingAnimation()
};

function reloadSkin(skinViewer, url) {
    if (url === "") {
        skinViewer.loadSkin(null);
    } else {
        skinViewer.loadSkin(url, {
            model: "auto-detect"//auto-detect,default,slim
        })
            .then(() => {})
            .catch(e => {
                console.error(e);
            });
    }
}
function reloadCape(skinViewer, url) {
    if (url === "") {
        skinViewer.loadCape(null);
    } else {
        skinViewer.loadCape(url, { backEquipment: "cape" })//cape,elytra
            .then(() =>{})
            .catch(e => {
                console.error(e);
            });
    }
}

function reloadPanorama(skinViewer, url) {
    if (url === "") {
        skinViewer.background = null;
    } else {
        skinViewer.loadPanorama(url)
            .then(() => {})
            .catch(e => {
                console.error(e);
            });
    }
}
function reloadNameTag(skinViewer, text) {
    if (text === "") {
        skinViewer.nameTag = null;
    } else {
        skinViewer.nameTag = text;
    }
}
function initializeViewer(skin_url, cape_url, name) {
    skinViewer = new skinview3d.SkinViewer({
        canvas: document.getElementById("skin_container")
    });

    skinViewer_turn = new skinview3d.SkinViewer({
        canvas: document.getElementById("skin_container_turn")
    });
    skinViewer.width = 240
    skinViewer.height = 240
    skinViewer.fov = 70
    skinViewer.zoom = 0.8
    skinViewer.globalLight.intensity = 3
    skinViewer.cameraLight.intensity = 0.8
    skinViewer.playerWrapper.rotateY(0.5)//默认y轴转动
    skinViewer.autoRotate = false //旋转
    skinViewer.autoRotateSpeed = 2//旋转速度
    const animationName = "idle";//"",idle,walk.run,fly
    if (animationName !== "") {
        skinViewer.animation = availableAnimations[animationName];
        skinViewer.animation.speed = 1;//动作速度
    }
    skinViewer.controls.enableRotate = true;//允许鼠标转动
    skinViewer.controls.enableZoom = true;//允许缩放
    skinViewer.controls.enablePan = false;//允许鼠标拖动
    reloadSkin(skinViewer, skin_url);//皮肤加载
    reloadCape(skinViewer, cape_url);//披风加载
    reloadPanorama(skinViewer, "");//背景加载
    reloadNameTag(skinViewer, name);//名字tag加载


    skinViewer_turn.width = 240
    skinViewer_turn.height = 240
    skinViewer_turn.fov = 70
    skinViewer_turn.zoom = 0.8
    skinViewer_turn.globalLight.intensity = 3
    skinViewer_turn.cameraLight.intensity = 0.9
    skinViewer_turn.playerWrapper.rotateY(2.5)//默认y轴转动
    skinViewer_turn.autoRotate = false //旋转
    skinViewer_turn.autoRotateSpeed = 2//旋转速度
    const animationName_turn = "idle";//"",idle,walk.run,fly
    if (animationName_turn !== "") {
        skinViewer_turn.animation = availableAnimations[animationName];
        skinViewer_turn.animation.speed = 1;//动作速度
    }
    skinViewer_turn.controls.enableRotate = true;//允许鼠标转动
    skinViewer_turn.controls.enableZoom = true;//允许缩放
    skinViewer_turn.controls.enablePan = false;//允许鼠标拖动
    reloadSkin(skinViewer_turn, skin_url);//皮肤加载
    reloadCape(skinViewer_turn, cape_url);//披风加载
    reloadPanorama(skinViewer_turn, "");//背景加载
    reloadNameTag(skinViewer_turn, name);//名字tag加载
}

async function get_api_info(api, req) {
    return $.ajax({
        type: "get",
        url: `${api}${req}`,
        async: true,
        success: function (data) {
            console.log(data)
            return data
        }, error: function (data) {
            console.log(`err${data}`)
        }
    });
}

async function reload_hall_info(info){
    function updateProgress(progress, text, value, target, level) {
        let newtarget = Math.floor(target * 100)
        let perimeter = Math.PI * 2 * 75;
        progress.style.strokeDasharray = perimeter * value / 100 + " " + perimeter * (1 - value / 100);
        text.textContent = level;
        if (value != newtarget) {
            if (value < newtarget) {
                value+=1;
            } else {
                value-=1;
            }
            requestAnimationFrame(function() {
                updateProgress(progress, text, value, target, level);
            });
        }
    }
    function need_exp(exp){
        let level = Math.sqrt((exp*0.0008+12.25)-2.5)
        let ceil_level = Math.ceil(level)
        let floor_level = Math.floor(level)
        let max_exp = (ceil_level ** 2 - 14.5) / 0.0008;
        let min_exp = (floor_level ** 2 - 14.5) / 0.0008;
        let need_exp = max_exp - exp
        let need = ceil_level - level
        return [level, need_exp, need, exp]
    }
    function data_time(num){
        console.log(num)
        let date = new Date(num);
        let Y = date.getFullYear() + '-';
        let M = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
        let D = date.getDate() + ' ';
        let h = date.getHours() + ':';
        let m = date.getMinutes() + ':';
        let s = date.getSeconds();
        let datetime = Y + M + D + h + m + s;
        return datetime
    }
    let exp_data = need_exp(info["player"]["networkExp"])
    let achieve_nums = Object.keys(info["player"]["achievementsOneTime"]).length
    let achieve_points = info["player"]["achievementPoints"]
    let first_login = data_time(info["player"]["firstLogin"])
    let last_login = data_time(info["player"]["lastLogin"])
    let hall_quests = Object.keys(info["player"]["quests"]).length
    let hall_challenge = Object.keys(info["player"]["challenges"]["all_time"]).length

    updateProgress($("#levelcircle")[0] ,$("#leveltext")[0] ,0 ,(1 - exp_data[2]).toFixed(2), exp_data[0].toFixed(2))
    $("#hall_level")[0].textContent = exp_data[0].toFixed(2)
    $("#hall_next_exp_need")[0].textContent = exp_data[1]
    $("#hall_quest")[0].textContent = hall_quests
    $("#hall_challenge")[0].textContent = hall_challenge
    $("#hall_exp")[0].textContent = exp_data[3]
    $("#hall_points")[0].textContent = achieve_points
    $("#hall_achieves")[0].textContent = achieve_nums
    $("#first_login")[0].textContent = first_login
    $("#last_login")[0].textContent = last_login
    $("#mc_uuid")[0].textContent = "7a09121923124dc8b1393f2dd782d7fd"
    $("#hyp_id")[0].textContent = info["player"]["_id"]

    let online = info["online"]
    if (online){
        $("#online")[0].style.color = "green"
        $("#online")[0].textContent = "[在线]"
    }else {
        $("#online")[0].style.color = "red"
        $("#online")[0].textContent = "[离线]"
    }
}
async function reload_bedwars_info(info){
    let bedwars = info["player"]["stats"]["Bedwars"]
    let bedwars_li = $("li[data-game='bedwars']")
    if(!bedwars){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        bedwars_li.append(divbox)
        return
    }
    let bedwars_experience = bedwars["Experience"] || 0
    let bedwars_coins = bedwars["coins"] || 0
    let bedwars_games = bedwars["games_played_bedwars"] || 0
    let bedwars_wins = bedwars["wins_bedwars"] || 0
    let bedwars_bed_broken = bedwars["beds_broken_bedwars"] || 0
    let bedwars_kills = bedwars["kills_bedwars"] || 0
    let bedwars_void_kills = bedwars["void_kills_bedwars"] || 0
    let bedwars_deaths = bedwars["deaths_bedwars"] || 0
    let bedwars_void_deaths = bedwars["void_deaths_bedwars"] || 0
    let irons_resources = bedwars["iron_resources_collected_bedwars"] || 0
    let gold_resources = bedwars["gold_resources_collected_bedwars"] || 0
    let diamond_resources = bedwars["diamond_resources_collected_bedwars"] || 0
    let emerald_resources = bedwars["emerald_resources_collected_bedwars"] || 0

    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计经验:</span><span STYLE="color: green">${bedwars_experience}</span>
							</div>
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${bedwars_coins}</span>
							</div>
						</div>
						<div class="divtext">
							<div class="spancolor">
								<span>总游戏场数:</span><span STYLE="color: green">${bedwars_games}</span>
							</div>
							<div class="spancolor">
								<span>总失败场:</span><span STYLE="color: red">${bedwars_games - bedwars_wins}</span>
							</div>
							<div class="spancolor">
								<span>总胜利数:</span><span STYLE="color: green">${bedwars_wins}</span>
							</div>

						</div>
						<div class="divtext">
							<span>总击杀:</span>
							<span STYLE="color: green">${bedwars_kills}</span>
							<span>最终总击杀:</span>
							<span STYLE="color: green">${bedwars_void_kills}</span>
							<span>总拆床数:</span>
							<span STYLE="color: green">${bedwars_bed_broken}</span>

						</div>
						<div class="divtext">
							<span>总死亡:</span>
							<span STYLE="color: red">${bedwars_deaths}</span>
							<span>最终死亡:</span>
							<span STYLE="color: red">${bedwars_void_deaths}</span>
							<span>总床破坏数:</span>
							<span STYLE="color: red">${bedwars_games - bedwars_wins}</span>
						</div>
						<div class="divtext">
							<span>KD:</span>
							<span style="color: #804d00">${(bedwars_kills / bedwars_deaths).toFixed(2)}</span>
							<span>FKD:</span>
							<span style="color: #804d00">${(bedwars_void_kills / bedwars_void_deaths).toFixed(2)}</span>
							<span>BKD:</span>
							<span style="color: #804d00">${(bedwars_bed_broken / (bedwars_games - bedwars_wins)).toFixed(2)}</span>
						</div>
						<div class="divtext">
							<span>收集品概览:</span>
                            <div class="spancolor">
								<span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-112px -560px"></span><span>收集量:</span><span STYLE="color: green">${irons_resources}</span>
							</div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-48px -560px"></span><span>收集量:</span><span STYLE="color: gold">${gold_resources}</span>
                            </div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-192px -544px"></span><span>收集量:</span><span STYLE="color: blue">${diamond_resources}</span>
                            </div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-208px -544px"></span><span>收集量:</span><span STYLE="color: green">${emerald_resources}</span>
                            </div>
						</div>
					</div>
				</div>
            `)
    bedwars_li.append(divbox)
}
async function reload_skywars_info(info){
    let skywars = info["player"]["stats"]["SkyWars"]
    let skywars_li = $("li[data-game='skywars']")
    if(!skywars){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        skywars_li.append(divbox)
        return
    }
    let skywars_exp = skywars["skywars_experience"] || 0
    let skywars_level = skywars["levelFormatted"] || 0
    let skywars_coins = skywars["coins"] || 0
    let skywars_souls = skywars["souls"] || 0
    let skywars_games = skywars["games_played_skywars"] || 0
    let skywars_win_streak = skywars["win_streak"] || 0
    let skywars_kills = skywars["kills"] || 0
    let skywars_deaths = skywars["deaths"] || 0
    let skywars_void_kills = skywars["void_kills"] || 0
    let skywars_kd = (skywars_kills / skywars_deaths).toFixed(2) || 0
    let skywars_fkd = (skywars_kills).toFixed(2) || 0
    let skywars_blocks_broken_lab = skywars["blocks_broken_lab"] || 0
    let skywars_blocks_placed_lab = skywars["blocks_placed_lab"] || 0
    let skywars_chests_opened_lab = skywars["chests_opened_lab"] || 0
    let skywars_enderpearls_thrown_lab = skywars["enderpearls_thrown_lab"] || 0

    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计经验:</span><span STYLE="color: green">${skywars_exp}</span>
							</div>
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${skywars_coins}</span>
							</div>
                            <div class="spancolor">
								<span>等级:</span><span STYLE="color: green">${skywars_level}</span>
							</div>
						</div>
						<div class="divtext">
							<div class="spancolor">
								<span>总游戏场数:</span><span STYLE="color: green">${skywars_games}</span>
							</div>
							<div class="spancolor">
								<span>连胜数:</span><span STYLE="color: red">${skywars_win_streak}</span>
							</div>
						</div>
						<div class="divtext">
							<span>总击杀:</span>
							<span STYLE="color: green">${skywars_kills}</span>
							<span>最终总击杀:</span>
							<span STYLE="color: green">${skywars_void_kills}</span>
							<span>收割灵魂数:</span>
							<span STYLE="color: green">${skywars_souls}</span>

						</div>
						<div class="divtext">
							<span>总死亡:</span>
							<span STYLE="color: red">${skywars_deaths}</span>
						</div>
						<div class="divtext">
							<span>KD:</span>
							<span style="color: #804d00">${skywars_kd}</span>
							<span>FKD:</span>
							<span style="color: #804d00">${skywars_fkd}</span>
						</div>
						<div class="divtext">
							<span>游戏中数据:</span>
                            <div class="spancolor">
								<span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-672px -400px"></span><span>方块放置:</span><span STYLE="color: green">${skywars_blocks_placed_lab}</span>
							</div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-176px -448px"></span><span>方块破坏:</span><span STYLE="color: gold">${skywars_blocks_broken_lab}</span>
                            </div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-720px -32px"></span><span>打开箱子:</span><span STYLE="color: blue">${skywars_chests_opened_lab}</span>
                            </div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-224px -544px"></span><span>末影珍珠使用量:</span><span STYLE="color: green">${skywars_enderpearls_thrown_lab}</span>
                            </div>
						</div>
					</div>
				</div>
            `)
    skywars_li.append(divbox)
}
async function reload_murder_mystery_info(info){
    let murder_mystery = info["player"]["stats"]["MurderMystery"]
    let murder_mystery_li = $("li[data-game='murder-mystery']")
    if(!murder_mystery){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        murder_mystery_li.append(divbox)
        return
    }
    let murder_mystery_coins = murder_mystery["coins"] || 0
    let murder_mystery_wins = murder_mystery["wins"] || 0
    let murder_mystery_games = murder_mystery["games"] || 0
    let murder_mystery_kills = murder_mystery["kills"] || 0
    let murder_mystery_kills_as_murderer = murder_mystery["kills_as_murderer"] || 0
    let murder_mystery_deaths = murder_mystery["deaths"] || 0
    let murder_detective_chance = murder_mystery["detective_chance"] || 0
    let murder_murderer_chance = murder_mystery["murderer_chance"] || 0
    let murder_mystery_coins_pickedup = murder_mystery["coins_pickedup"] || 0
    let murder_mystery_kills_as_survivor = murder_mystery["kills_as_survivor"] || 0

    let murder_mystery_kd = (murder_mystery_kills / murder_mystery_deaths).toFixed(2) || 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${murder_mystery_coins}</span>
							</div>
						</div>
						<div class="divtext">
							<div class="spancolor">
								<span>总游戏场数:</span><span STYLE="color: green">${murder_mystery_games}</span>
							</div>
                            <div class="spancolor">
								<span>警探场数:</span><span STYLE="color: green">${murder_detective_chance}</span>
							</div>
                            <div class="spancolor">
								<span>杀手场数:</span><span STYLE="color: green">${murder_murderer_chance}</span>
                            </div>
							<div class="spancolor">
								<span>胜利场数:</span><span STYLE="color: red">${murder_mystery_wins}</span>
							</div>
						</div>
						<div class="divtext">
                            <span>总击杀:</span>
							<span STYLE="color: green">${murder_mystery_kills}</span>
							<span>狼人击杀:</span>
							<span STYLE="color: green">${murder_mystery_kills_as_murderer}</span>
							<span>平民击杀:</span>
							<span STYLE="color: green">${murder_mystery_kills_as_survivor}</span>

						</div>
						<div class="divtext">
							<span>总死亡:</span>
							<span STYLE="color: red">${murder_mystery_deaths}</span>
						</div>
						<div class="divtext">
							<span>KD:</span>
							<span style="color: #804d00">${murder_mystery_kd}</span>

						</div>
						<div class="divtext">
							<span>游戏中数据:</span>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-48px -560px"></span><span>收集量:</span><span STYLE="color: gold">${murder_mystery_coins_pickedup}</span>
                            </div>
						</div>
					</div>
				</div>
            `)
    murder_mystery_li.append(divbox)
}
async function reload_arcade_info(info){
    let arcade = info["player"]["stats"]["Arcade"]
    let arcade_li = $("li[data-game='arcade-games']")
    if(!arcade){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        arcade_li.append(divbox)
        return
    }
    let arcade_coins = arcade["coins"]? 0 : arcade["coins"]
    let arcade_kills_zombies = arcade["zombie_kills_zombies"]? arcade["zombie_kills_zombies"] : 0//天灾模式
    let arcade_best_round_zombies = arcade["best_round_zombies"]? arcade["best_round_zombies"] : 0//天灾模式最佳通关回合
    let arcade_deaths_zombies_deadend = arcade["deaths_zombies_deadend"]? arcade["deaths_zombies_deadend"] : 0//天灾模式死亡
    let arcade_bullets_shot_zombies = arcade["bullets_shot_zombies"]? arcade["bullets_shot_zombies"] : 0//射出子弹
    let arcade_players_revived_zombies = arcade["players_revived_zombies"]? arcade["players_revived_zombies"] : 0//救援
    let arcade_wins_zombies = arcade["wins_zombies"]? arcade["wins_zombies"] : 0//天灾模式胜利次数
    let arcade_woolhunt_kills = arcade["woolhunt_kills"] || 0
    let arcade_woolhunt_deaths = arcade["woolhunt_deaths"] || 0
    let arcade_woolhunt_most_gold_earned = arcade["woolhunt_most_gold_earned"] || 0
    let arcade_woolhunt_kills_with_wool = arcade["woolhunt_kills_with_wool"] || 0
    let arcade_woolhunt_deaths_with_wool = arcade["woolhunt_deaths_with_wool"] || 0
    let arcade_dropper_games = arcade["dropper"]["games_played"] || 0
    let arcade_dropper_flawless_games = arcade["dropper"]["flawless_games"] || 0
    let arcade_dropper_fastest_game = arcade["dropper"]["fastest_game"] || 0
    let arcade_dropper_maps_completed = arcade["dropper"]["maps_completed"] || 0
    let arcade_dropper_fails = arcade["dropper"]["fails"] || 0
    let arcade_dropper_wins = arcade["dropper"]["wins"] || 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${arcade_coins}</span>
							</div>
						</div>
						<div class="divtext">
                            <span>天灾模式(末日生存)</span>
							<div class="spancolor">
								<span>总胜利场数:</span><span STYLE="color: green">${arcade_wins_zombies}</span>
							</div>
                            <div class="spancolor">
								<span>最佳通关回合:</span><span STYLE="color: green">${arcade_best_round_zombies}</span>
							</div>
							<div class="spancolor">
								<span>总计杀死僵尸:</span><span STYLE="color: green">${arcade_kills_zombies}</span><span class="sprite" style="background-image:url('../static/img/EntityCSS.png');background-position:-32px -448px"></span>
							</div>
                            <div class="spancolor">
								<span>总计射出子弹:</span><span STYLE="color: green">${arcade_bullets_shot_zombies}</span>
							</div>
                            <div class="spancolor">
								<span>总计救援:</span><span STYLE="color: green">${arcade_players_revived_zombies}</span>
							</div>
                            <div class="spancolor">
								<span>总死亡数:</span><span STYLE="color: red">${arcade_deaths_zombies_deadend}</span>
							</div>
						</div>
						<div class="divtext">
                            <div class="spancolor">
                                <span>羊毛战争</span><span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-624px -352px"></span>
                            </div>
                            <span>总击杀:</span>
							<span STYLE="color: green">${arcade_woolhunt_kills}</span>
							<span>击杀羊毛携带者:</span>
							<span STYLE="color: green">${arcade_woolhunt_kills_with_wool}</span>
						</div>
						<div class="divtext">
                            <div class="spancolor">
                                <span>羊毛战争</span><span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-624px -352px"></span>
                            </div>
							<span>总死亡:</span>
							<span STYLE="color: red">${arcade_woolhunt_deaths}</span>
                            <span>携带羊毛死亡:</span>
							<span STYLE="color: red">${arcade_woolhunt_deaths_with_wool}</span>
						</div>
						<div class="divtext">
                            <div class="spancolor">
                                <span>羊毛战争</span><span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-624px -352px"></span>
                            </div>
							<span>KD:</span>
							<span style="color: #804d00">${(arcade_woolhunt_kills / arcade_woolhunt_deaths).toFixed(2)}</span>
                            <span>WKD:</span>
							<span style="color: #804d00">${(arcade_woolhunt_kills_with_wool / arcade_woolhunt_deaths_with_wool).toFixed(2)}</span>

						</div>
						<div class="divtext">
                            <div class="spancolor">
							    <span>羊毛战争</span><span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-624px -352px"></span>
                            </div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-48px -560px"></span><span>收集量:</span><span STYLE="color: gold">${arcade_woolhunt_most_gold_earned}</span>
                            </div>
						</div>
                        <div class="divtext">
                            <div class="spancolor">
                                <span>心跳水立方</span><span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-736px -16px"></span>
                            </div>
                            <div class="spancolor">
                                <span>总游戏场数:</span>
                                <span STYLE="color: green">${arcade_dropper_games}</span>
                            </div>
                            <div class="spancolor">
                                <span>完美游戏场数:</span>
                                <span STYLE="color: green">${arcade_dropper_flawless_games}</span>
                            </div>
                            <div class="spancolor">
                                <span>最快通关时间:</span>
                                <span STYLE="color: green">${(arcade_dropper_fastest_game / 1000).toFixed(2)}s</span>
                            </div>
                            <div class="spancolor">
                                <span>完成地图数:</span>
                                <span STYLE="color: green">${arcade_dropper_maps_completed}</span>
                            </div>
                            <div class="spancolor">
                                <span>失败次数:</span>
                                <span STYLE="color: red">${arcade_dropper_fails}</span>
                            </div>
                            <div class="spancolor">
                                <span>胜利场数:</span>
                                <span STYLE="color: green">${arcade_dropper_wins}</span>
                            </div>
                        </div>
					</div>
				</div>
            `)

    arcade_li.append(divbox)
}
async function reload_uhc_info(info){
    let uhc = info["player"]["stats"]["UHC"]
    let uhc_li = $("li[data-game='uhc-champions']")
    if(!uhc){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        uhc_li.append(divbox)
        return
    }
    let uhc_coins = uhc["coins"] ? uhc["coins"] : 0
    let uhc_packages = uhc["packages"]? uhc["packages"].length : 0
    let uhc_equippedKit = uhc["equippedKit"]  || 0//装备套件
    let uhc_score = uhc["score"] || 0
    let uhc_kills = uhc["kills"] || 0
    let uhc_deaths = uhc["deaths"] || 0
    let uhc_ultimates_crafted = uhc["ultimates_crafted"] || 0
    let uhc_heads_eaten = uhc["heads_eaten"] || 0
    let uhc_deaths_solo = uhc["deaths_solo"]? uhc["deaths_solo"] : 0
    let uhc_kills_solo = uhc["kills_solo"]? uhc["kills_solo"] : 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${uhc_coins}</span>
							</div>
                            <div class="spancolor">
								<span>工具包数:</span><span STYLE="color: green">${uhc_packages}</span>
							</div>
                            <div class="spancolor">
								<span>使用装备套件:</span><span STYLE="color: green">${uhc_equippedKit}</span>
							</div>
                            <div class="spancolor">
								<span>UHC成绩:</span><span STYLE="color: green">${uhc_score}</span>
							</div>
						</div>
						<div class="divtext">
							<span>总击杀:</span><span STYLE="color: green">${uhc_kills}</span>
							<span>单挑击杀:</span><span STYLE="color: green">${uhc_kills_solo}</span>
						</div>
						<div class="divtext">
							<span>总死亡:</span>
							<span STYLE="color: red">${uhc_deaths}</span>
                            <span>单挑死亡:</span>
							<span STYLE="color: red">${uhc_deaths_solo}</span>
						</div>
						<div class="divtext">
							<span>KD:</span>
							<span style="color: #804d00">${(uhc_kills / uhc_deaths).toFixed(2)}</span>
                            <span>WKD:</span>
							<span style="color: #804d00">${(uhc_kills_solo / uhc_deaths_solo).toFixed(2)}</span>

						</div>
                        <div class="divtext">
                            <span>游戏中数据:</span>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-0px -512px"></span><span>制作物品:</span><span>${uhc_ultimates_crafted}</span>
                            </div>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/EntityCSS.png');background-position:-32px -448px"></span><span>食用玩家头颅:</span><span>${uhc_heads_eaten}</span>
                            </div>
                        </div>
					</div>
				</div>
            `)

    uhc_li.append(divbox)
}
async function reload_Arena_info(info){
    let arena = info["player"]["stats"]["Arena"]
    let arena_li = $("li[data-game='arena-brawl']")
    if(!arena){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        arena_li.append(divbox)
        return
    }
    let arena_coins = arena["coins"] || 0
    let arena_wins = arena["wins"] || 0
    let arena_games_1v1 = arena["games_1v1"] || 0
    let arena_damage_1v1 = arena["damage_1v1"] || 0
    let arena_healed_1v1 = arena["healed_1v1"] || 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${arena_coins}</span>
							</div>
						</div>
                        <div class="divtext">
                            <div class="spancolor">
							    <span>1v1总游戏场数:</span><span STYLE="color: green">${arena_games_1v1}</span>
                            </div>
                            <div class="spancolor">
							    <span>总胜利:</span><span STYLE="color: green">${arena_wins}</span>
                            </div>
						</div>
						<div class="divtext">
							<span>1v1总击杀:</span><span STYLE="color: green">${arena_wins}</span>
						</div>
						<div class="divtext">
							<span>总死亡:</span>
							<span STYLE="color: red">${arena_games_1v1 - arena_wins}</span>
						</div>
						<div class="divtext">
							<span>KD:</span>
							<span style="color: #804d00">${(arena_wins) - (arena_games_1v1 - arena_wins).toFixed(2)}</span>
						</div>
                        <div class="divtext">
                            <span>游戏中数据:</span>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-224px -432px"></span><span>总伤害:</span><span>${arena_damage_1v1}</span>
                            </div>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-176px -416px"></span><span>总治疗量:</span><span>${arena_healed_1v1}</span>
                            </div>
                        </div>
					</div>
				</div>
            `)

    arena_li.append(divbox)
}
async function reload_BuildBattle_info(info){
    let BuildBattle = info["player"]["stats"]["BuildBattle"]
    let BuildBattle_li = $("li[data-game='build-battle']")
    if(!BuildBattle){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        BuildBattle_li.append(divbox)
        return
    }
    let BuildBattle_coins = BuildBattle["coins"] || 0
    let BuildBattle_games = BuildBattle["games_played"] || 0
    let BuildBattle_score = BuildBattle["score"] || 0
    let BuildBattle_wins = BuildBattle["wins"] || 0
    let BuildBattle_total_votes = BuildBattle["total_votes"] || 0
    let BuildBattle_packages = BuildBattle["packages"]?  BuildBattle["packages"].length : 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${BuildBattle_coins}</span>
							</div>
                            <div class="spancolor">
								<span>工具包数:</span><span STYLE="color: green">${BuildBattle_packages}</span>
							</div>
                            <div class="spancolor">
								<span>总成绩:</span><span STYLE="color: green">${BuildBattle_score}</span>
							</div>
						</div>
                        <div class="divtext">
                            <div class="spancolor">
							    <span>总游戏数:</span><span STYLE="color: green">${BuildBattle_games}</span>
                            </div>
                            <div class="spancolor">
							    <span>总胜利:</span><span STYLE="color: green">${BuildBattle_wins}</span>
                            </div>
						</div>
                        <div class="divtext">
                            <span>游戏中数据:</span>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-96px -512px"></span><span>总票数:</span><span>${BuildBattle_total_votes}</span>
                            </div>
                        </div>
					</div>
				</div>
            `)

    BuildBattle_li.append(divbox)
}
async function reload_msgo_info(info){
    let msgo = info["player"]["stats"]["MCGO"]
    let msgo_li = $("li[data-game='cops-and-crims']")
    if(!msgo){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        msgo_li.append(divbox)
        return
    }
    let msgo_coins = msgo["coins"] || 0
    let msgo_packages = msgo["packages"] ?  msgo["packages"].length : 0
    let msgo_game_plays = msgo["game_plays"] || 0
    let msgo_wins = msgo["game_wins"] || 0
    let msgo_kills = msgo["kills"] || 0
    let msgo_deaths = msgo["deaths"] || 0
    let msgo_game_plays_deathmatch = msgo["game_plays_deathmatch"] || 0
    let msgo_game_wins_deathmatch = msgo["game_wins_deathmatch"] || 0
    let msgo_shots_fired = msgo["shots_fired"] || 0
    let msgo_round_wins = msgo["round_wins"] || 0
    let msgo_assists = msgo["assists"] || 0
    let msgo_bombs_defused = msgo["bombs_defused"] || 0
    let msgo_headshot_kills = msgo["headshot_kills"] || 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${msgo_coins}</span>
							</div>
                            <div class="spancolor">
								<span>工具包数:</span><span STYLE="color: green">${msgo_packages}</span>
							</div>

						</div>
                        <div class="divtext">
                            <div class="spancolor">
							    <span>总游戏场数:</span><span STYLE="color: green">${msgo_game_plays}</span>
                            </div>
                            <div class="spancolor">
							    <span>死亡竞赛场数:</span><span STYLE="color: red">${msgo_game_plays_deathmatch}</span>
                            </div>
                            <div class="spancolor">
							    <span>死亡竞赛场数:</span><span STYLE="color: red">${msgo_game_wins_deathmatch}</span>
                            </div>
                            <div class="spancolor">
							    <span>总胜利:</span><span STYLE="color: green">${msgo_wins}</span>
                            </div>
                            <div class="spancolor">
							    <span>总回合胜利:</span><span STYLE="color: green">${msgo_round_wins}</span>
                            </div>
						</div>
                        <div class="divtext">

							    <span>总击杀:</span><span STYLE="color: green">${msgo_kills}</span>


							    <span>爆头击杀:</span><span STYLE="color: green">${msgo_headshot_kills}</span>

                        </div>
                        <div class="divtext">

						    <span>死亡:</span><span STYLE="color: red">${msgo_deaths}</span>

                        </div>
                        <div class="divtext">
							<span>KD:</span>
							<span style="color: #804d00">${(msgo_kills / msgo_deaths).toFixed(2)}</span>
						</div>
                        <div class="divtext">
                            <span>游戏中数据:</span>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-32px -368px"></span><span>总计射出子弹:</span><span>${msgo_shots_fired}</span>
                            </div>
                            <div class="spancolor">
                                <span class="sprite" style="background-image:url('../static/img/Heart.png')"></span><span>救援次数:</span><span>${msgo_assists}</span>
                            </div>
                            <div class="spancolor">
							    <span>拆除炸弹次数:</span><span>${msgo_bombs_defused}</span>
                            </div>
                        </div>
					</div>
				</div>
            `)

    msgo_li.append(divbox)
}
async function reload_duels_info(info){
    let duels = info["player"]["stats"]["Duels"]
    let duels_li = $("li[data-game='duels']")
    if(!duels){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        duels_li.append(divbox)
        return
    }
    let duels_games = duels["games_played_duels"] || 0
    let duels_rounds_played = duels["rounds_played"] || 0
    let duels_wins = duels["wins"] || 0
    let duels_kills = duels["kills"] || 0
    let duels_coins = duels["coins"] || 0
    let duels_blocks_placed = duels["blocks_placed"] || 0
    let duels_damage_dealt = duels["damage_dealt"] || 0
    let duels_health_regenerated = duels["health_regenerated"] || 0
    let duels_deaths = duels["deaths"] || 0
    let duels_melee_hits = duels["melee_hits"] || 0
    let duels_goals = duels["goals"] || 0
    let duels_bridge_duel_rounds_played = duels["bridge_duel_rounds_played"] || 0
    let duels_bridge_kills = duels["bridge_kills"] || 0
    let duels_bridge_deaths = duels["bridge_deaths"] || 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${duels_coins}</span>
							</div>
						</div>
                        <div class="divtext">
                            <span>总数据:</span>
                            <div class="spancolor">
							    <span>总游戏场数:</span><span STYLE="color: green">${duels_games}</span>
                            </div>
                            <div class="spancolor">
							    <span>总游戏回合数:</span><span STYLE="color: red">${duels_rounds_played}</span>
                            </div>
                            <div class="spancolor">
							    <span>总胜利:</span><span STYLE="color: green">${duels_wins}</span>
                            </div>
						</div>
                        <div class="divtext">
                            <span>总数据:</span>
						    <span>总击杀:</span><span STYLE="color: green">${duels_kills}</span>
						    <span>总死亡:</span><span STYLE="color: red">${duels_deaths}</span>
                            <span>KD:</span><span style="color: #804d00">${(duels_kills / duels_deaths).toFixed(2)}</span>
                        </div>
                        <div class="divtext">
                            <span>独木桥决斗(单挑):</span>
                            <div class="spancolor">
							    <span>总游戏回合数:</span><span STYLE="color: green">${duels_bridge_duel_rounds_played}</span>
                            </div>
                            <div class="spancolor">
							    <span>总得分:</span><span STYLE="color: green">${duels_goals}</span>
                            </div>
						</div>
                        <div class="divtext">
                            <span>独木桥决斗(单挑):</span>
						    <span>总击杀:</span><span STYLE="color: green">${duels_bridge_kills}</span>
						    <span>总死亡:</span><span STYLE="color: red">${duels_bridge_deaths}</span>
                            <span>KD:</span><span style="color: #804d00">${(duels_bridge_kills / duels_bridge_deaths).toFixed(2)}</span>
                        </div>
                        <div class="divtext">
                            <span>游戏中数据:</span>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-224px -432px"></span><span>总伤害:</span><span>${duels_damage_dealt}</span>
                            </div>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-224px -432px"></span><span>近战命中:</span><span>${duels_melee_hits}</span>
                            </div>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-176px -416px"></span><span>总治疗量:</span><span>${duels_health_regenerated}</span>
                            </div>
                            <div class="spancolor">
								<span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-672px -400px"></span><span>方块放置:</span><span STYLE="color: green">${duels_blocks_placed}</span>
							</div>
                        </div>
					</div>
				</div>
            `)

    duels_li.append(divbox)
}
async function reload_megawalls_info(info){
    let megawalls = info["player"]["stats"]["Walls3"]
    let megawalls_li = $("li[data-game='megawalls']")
    if(!megawalls){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        megawalls_li.append(divbox)
        return
    }
    let megawalls_coins = megawalls["coins"] || 0
    let megawalls_classes = megawalls["classes"] || "无"
    let megawalls_games_played = megawalls["games_played"] || 0
    let megawalls_wins = megawalls["wins"] || 0
    let megawalls_chosen_class = megawalls["chosen_class"] || 0
    let megawalls_kills = megawalls["kills"] || 0
    let megawalls_final_kills = megawalls["final_kills"] || 0
    let megawalls_deaths = megawalls["deaths"] || 0
    let megawalls_final_deaths = megawalls["final_deaths"] || 0
    let megawalls_iron_ore_broken = megawalls["iron_ore_broken"] || 0
    let megawalls_golden_apples_eaten = megawalls["golden_apples_eaten"] || 0
    let megawalls_food_eaten = megawalls["food_eaten"] || 0
    let megawalls_assists = megawalls["assists"] || 0
    let megawslls_wither_damage = megawalls["wither_damage"] || 0
    let megawalls_packages = megawalls["packages"] ? megawalls["packages"].length : 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${megawalls_coins}</span>
							</div>
                            <div class="spancolor">
								<span>工具包数:</span><span STYLE="color: green">${megawalls_packages}</span>
							</div>
                            <span>当前职业:</span><span STYLE="color: green">${megawalls_chosen_class}</span>
						</div>
                        <div class="divtext">
                            <div class="spancolor">
							    <span>总游戏场数:</span><span STYLE="color: green">${megawalls_games_played}</span>
                            </div>
                            <div class="spancolor">
							    <span>总胜利:</span><span STYLE="color: green">${megawalls_wins}</span>
                            </div>
                            <div class="spancolor">
							    <span>总失败场数:</span><span STYLE="color: green">${megawalls_games_played - megawalls_wins}</span>
                            </div>
						</div>
                        <div class="divtext">
						    <span>总击杀:</span><span STYLE="color: green">${megawalls_kills}</span>
                            <span>总最终击杀:</span><span STYLE="color: green">${megawalls_final_kills}</span>

                        </div>
                        <div class="divtext">
						    <span>总死亡:</span><span STYLE="color: red">${megawalls_deaths}</span>
                            <span>总最终击杀:</span><span STYLE="color: red">${megawalls_final_deaths}</span>

                        </div>
                        <div class="divtext">
                            <span>KD:</span><span style="color: #804d00">${(megawalls_kills / megawalls_deaths).toFixed(2)}</span>
                            <span>FKD:</span><span style="color: #804d00">${(megawalls_final_kills / megawalls_final_deaths).toFixed(2)}</span>
						</div>
                        <div class="divtext">
                            <span>游戏中数据:</span>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-0px -464px"></span><span>挖掘铁矿:</span><span>${megawalls_iron_ore_broken}</span>
                            </div>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-176px -416px"></span><span>总治疗量:</span><span STYLE="color: red">${megawalls_assists}</span>
                            </div>
                            <div class="spancolor">
								<span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-80px -496px"></span><span>食用金苹果:</span><span STYLE="color: gold">${megawalls_golden_apples_eaten}</span>
							</div>
                            <div class="spancolor">
								<span class="sprite" style="background-image:url('../static/img/BlockCSS.webp');background-position:-128px -480px"></span><span>食用食物:</span><span STYLE="color: green">${megawalls_food_eaten}</span>
							</div>
                            <div class="spancolor">
							    <span class="sprite" style="background-image:url('../static/img/ItemCSS.png');background-position:-224px -432px"></span><span>对凋零造成伤害:</span><span>${megawslls_wither_damage}</span>
                            </div>
                        </div>
					</div>
				</div>
            `)
    megawalls_li.append(divbox)
}
async function reload_tntgames_info(info){
    let tntgames = info["player"]["stats"]["TNTGames"]
    let tntgames_li = $("li[data-game='tnt-games']")
    if(!tntgames){
        let divbox = $(`
                    <div class="divbox">
					    <div class="container">
						    <div class="divtext">
                            <span>无数据</span>
                            </div>
                        </div>
                    </div>

                `)
        tntgames_li.append(divbox)
        return
    }
    let tntgames_coins = tntgames["coins"] || 0
    let tntgames_packages = tntgames["packages"] ? tntgames["packages"].length : 0
    let tntgames_wins = tntgames["wins"] || 0
    let tntgames_record_tntrun = tntgames["record_tntrun"] || 0
    let tntgames_record_pvprun = tntgames["record_pvprun"] || 0
    let tntgames_deaths_tntrun = tntgames["deaths_tntrun"] || 0
    let tntgames_deaths_pvprun = tntgames["deaths_pvprun"] || 0
    let tntgames_kills_pvprun = tntgames["kills_pvprun"] || 0
    let divbox = $(`
                <div class="divbox">
					<div class="container">
						<div class="divtext">
							<div class="spancolor">
								<span>总计硬币:</span><span STYLE="color: green">${tntgames_coins}</span>
							</div>
                            <div class="spancolor">
								<span>工具包数:</span><span STYLE="color: green">${tntgames_packages}</span>
							</div>
						</div>
                        <div class="divtext">
                            <div class="spancolor">
							    <span>总胜利:</span><span STYLE="color: green">${tntgames_wins}</span>
                            </div>
                            <div class="spancolor">
							    <span>TNT-run成绩:</span><span STYLE="color: green">${tntgames_record_tntrun}</span>
                            </div>
                            <div class="spancolor">
							    <span>PVP-run成绩:</span><span STYLE="color: green">${tntgames_record_pvprun}</span>
                            </div>
						</div>
                        <div class="divtext">
						    <span>PVP-run击杀:</span><span STYLE="color: green">${tntgames_kills_pvprun}</span>
                        </div>
                        <div class="divtext">
						    <span>TNT-run死亡:</span><span STYLE="color: red">${tntgames_deaths_tntrun}</span>
                            <span>PVP-run死亡:</span><span STYLE="color: red">${tntgames_deaths_pvprun}</span>

                        </div>
                        <div class="divtext">
                            <span>PVP-run KD:</span><span style="color: #804d00">${(tntgames_kills_pvprun / tntgames_deaths_pvprun).toFixed(2)}</span>
						</div>
					</div>
				</div>
            `)
    tntgames_li.append(divbox)
}
function load_all(name){
    get_api_info("http://127.0.0.1:8099/api/hypinfo", `?name=${name}`).then(function(playerinfo) {
        let skin_url = playerinfo["skin_url"]
        let cape_url = playerinfo["cape_url"]
        let player_name = playerinfo["player"]["playername"]
        initializeViewer(skin_url, cape_url, player_name);
        reload_hall_info(playerinfo);
        reload_bedwars_info(playerinfo);
        reload_skywars_info(playerinfo);
        reload_murder_mystery_info(playerinfo);
        reload_arcade_info(playerinfo);
        reload_uhc_info(playerinfo);
        reload_Arena_info(playerinfo);
        reload_BuildBattle_info(playerinfo);
        reload_msgo_info(playerinfo);
        reload_duels_info(playerinfo);
        reload_megawalls_info(playerinfo);
        reload_tntgames_info(playerinfo);
    });
}
let web_url = window.location.href;
const url = new URL(web_url);
const params = new URLSearchParams(url.search);
const name = params.get('name');
load_all(name)