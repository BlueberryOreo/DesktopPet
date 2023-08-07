let isMouseDown = false;
let isTapping = false;
let mouseMoved = false;
let mouseDownTimeStart;
const container = document.getElementById("modelContainer");
const webmModel = document.getElementById("webm-model");
const gifModel = document.getElementById("gif-model");

const threshold = 100; // 鼠标按下的时间阈值

// tap
// 问题：drag由于存在鼠标点击的动作也会被判断成click从而触发戳一戳
// 20230806_23_10 上述问题已解决，方法：添加变量mouseMoved，判断鼠标是否移动过
//      如果移动过，则设为true，并在drag结束后1ms以后将其恢复为false
//      根据猜测，click会在鼠标抬起时触发，在鼠标抬起后经过一点延迟再将mouseMove恢复为false可以做到触发click但是不会执行内部的if语句的效果。
container.addEventListener("click", (event) => {
    // alert(model.autoplay);
    if(!isTapping && !mouseMoved){
        isTapping = true;
        // model.pause();
        if(webmModel.style.display === "block") tapWebm(webmModel);
        else if(gifModel.style.display == "block") tapGif(gifModel);
        else alert("No model active");
    }
});

// drag
container.addEventListener("mousedown", (event) => {
    isMouseDown = true;
    mouseDownTimeStart = Date.now();
    const mouseX = event.screenX;
    const mouseY = event.screenY;
    window.PyHandler.drag_start(mouseX, mouseY);
    // window.PyHandler.dragging("mouse down");
});

container.addEventListener("mouseup", (event) => {
    isMouseDown = false;
    setTimeout(() => {
        mouseMoved = false;
    }, 1); // 添加延时1ms
    // window.PyHandler.dragging("mouse up");
});

container.addEventListener("mousemove", (event) => {
    var deltaTime = Date.now() - mouseDownTimeStart;
    if(isMouseDown && deltaTime >= threshold){
        // 改进想法：更合理的判断鼠标是否移动，因为如果鼠标在点击的时候出现了微小偏移，那么根据这种方法会被判断成拖动
        // 建议设为判断鼠标移动的时间或者根据一次移动的位置是否在一定阈值内判断是否为点击操作
        // 20230807 已改进完成
        mouseMoved = true;
        const mouseX = event.screenX;
        const mouseY = event.screenY;
        window.PyHandler.dragging(mouseX, mouseY);
    }
});

// functions
function tapWebm(model){
    model.loop = false;
    window.PyHandler.tapped();
    model.addEventListener("ended", (event) => {
        window.PyHandler.reverse_to_default();
        model.loop = true;
        isTapping = false;
    });
}

function tapGif(model){
    // 待完善
}
