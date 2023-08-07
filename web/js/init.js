// init
window.onload = function () {
    try {
        new QWebChannel(qt.webChannelTransport, function (channel) {
            //将QWebChannel的实例挂载到window.PyHandler，后面在javascript中通过window.PyHandler即可调用
            window.PyHandler = channel.objects.PyHandler;
            window.PyHandler.init_home("initializing...");
        });
        window.change_pose = (modelPath, pose=undefined, direct=1) => {
            /**
             * 设置角色动作API
             * 
             * modelPath: 角色动作模型路径
             * pose: 角色动作名称
             * direct=1: 角色朝向
             */
            // 变换角色动作模型
            var webmModel = document.getElementById("webm-model");
            var gifModel = document.getElementById("gif-model");
            var nextDirect = "scaleX(" + direct + ")";

            var type = modelPath.split(".");
            type = type[type.length - 1];
            if(type === "webm"){
                if(gifModel.style.display != "none") gifModel.style.display = "none";
                if(webmModel.style.display != "block") webmModel.style.display = "block";

                var webmModelPreloader = document.getElementById("webm-model-preloader"); // 预加载视频
                webmModelPreloader.src = modelPath;
                webmModelPreloader.load();

                webmModel.src = modelPath;
                if(Boolean(direct) && webmModel.style.transform != nextDirect) webmModel.style.transform = nextDirect;
                setTimeout(() => { webmModel.play(); }, 150); // 不设置150ms延迟会导致重复开启play问题
            }else if(type === "gif"){
                webmModel.style.display = "none";
                gifModel.style.display = "block";
                gifModel.src = modelPath;
                if(Boolean(direct) && gifModel.style.transform != nextDirect) gifModel.style.transform = nextDirect;
            }else{
                alert("Unrecognized file type: " + type);
            }
            // document.getElementById('model').play();
        };
    } catch (e) {
        window.console.log(e)
    }
};
