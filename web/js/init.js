// init
window.onload = function () {
    try {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            //将QWebChannel的实例挂载到window.PyHandler，后面在javascript中通过window.PyHandler即可调用
            window.PyHandler = channel.objects.PyHandler;
            window.PyHandler.init_home("initializing...");
        });
        window.change_pose = (pose, modelPath) => {
            // 变换角色动作模型
            var webmModel = document.getElementById("webm-model");
            var gifModel = document.getElementById("gif-model");

            var type = modelPath.split(".");
            type = type[type.length - 1];
            if(type === "webm"){
                if(gifModel.style.display != "none") gifModel.style.display = "none";
                if(webmModel.style.display != "block") webmModel.style.display = "block";
                webmModel.src = modelPath;
                setTimeout(() => { webmModel.play(); }, 150);
            }else if(type === "gif"){
                webmModel.style.display = "none";
                gifModel.style.display = "block";
                gifModel.src = modelPath;
            }else{
                alert("Unrecognized file type: " + type);
            }
            // document.getElementById('model').play();
        };
    } catch (e) {
        window.console.log(e)
    }
};
