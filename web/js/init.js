// init
window.onload = function () {
    try {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            //将QWebChannel的实例挂载到window.PyHandler，后面在javascript中通过window.PyHandler即可调用
            window.PyHandler = channel.objects.PyHandler;
            window.PyHandler.init_home("initializing...");
        });
        window.change_pose = (modelPath) => {
            // 变换角色动作模型
            document.getElementById('model').src = modelPath;
            setTimeout(() => { document.getElementById('model').play(); }, 150);
            // document.getElementById('model').play();
        };
    } catch (e) {
        window.console.log(e)
    }
};
