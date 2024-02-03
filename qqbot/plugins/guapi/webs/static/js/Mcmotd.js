function motdtocolor(originmotd) {
    if (originmotd.search('§') != -1) {
        const reg = /(^)?([^§]+)($)?/g;
        const outputspan = document.createElement('span');// 创建一个span最终输出的
        const len = originmotd.match(reg).length;
        let output = '';
        for (let i = 0; i<len; i++) {
            let aa = originmotd.match(reg)[i];
            const a1 = aa.substring(0,1);
            aa = aa.substr(1);
            const style = functioncolor(a1);
            Object.assign(outputspan.style, {
                color: style.color,
                textDecoration: style.textDecoration,
                fontStyle: style.fontStyle,
                fontFamily: style.fontFamily,
                whiteSpace: 'pre'
            });
            outputspan.innerHTML = aa || '';
            output = `${output}${outputspan.outerHTML}`;
        }
        output = output.replace(/\\n/g, "<br>");
        console.log(output)
        return output;
    }
    else {
        const outputspan = document.createElement('span');// 创建一个span最终输出的
        let output = '';
        outputspan.innerHTML = originmotd
        Object.assign(outputspan.style, {
            whiteSpace: 'pre'
        });
        return `${outputspan.outerHTML}`;
    }
}

function functioncolor(colorcod) {
    switch (colorcod) {
        case 'a':
            return {color: '#55ff55'};
        case 'b':
            return {color: '#55ffff'};
        case 'c':
            return {color: '#ff5555'};
        case 'd':
            return {color: '#ff55ff'};
        case 'e':
            return {color: '#ffff55'};
        case 'f':
            return {color: '#ffffff'};
        case 'g':
            return {color: '#ddd605'};
        case '0':
            return {color: '#000000'};
        case '1':
            return {color: '#0000aa'};
        case '2':
            return {color: '#00aa00'};
        case '3':
            return {color: '#00aaaa'};
        case '4':
            return {color: '#aa0000'};
        case '5':
            return {color: '#aa00aa'};
        case '6':
            return {color: '#ffaa00'};// 返回对应的颜色
        case '7':
            return {color: '#aaaaaa'};
        case '8':
            return {color: '#555555'};
        case '9':
            return {color: '#5555ff'};
        case 'k':
            return {textDecoration: 'R'};
        case 'l':
            return {textDecoration: 'Minecraft'};// 下划线
        case 'm':
            return {textDecoration: 'line-through'};// 删除线
        case 'n':
            return {textDecoration: 'underline'};// 无装饰
        case 'o':
            return {fontStyle: 'italic'};// 斜体
        case 'r':
            return {color: '#000000', textDecoration: 'none', fontStyle: 'normal', fontFamily: 'Minecraft R'};// 重置
        default:
            return {color: 'unknown style'};
    }
}