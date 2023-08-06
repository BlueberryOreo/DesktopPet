let isMouseDown = false;
let isTapping = false;
let mouseMoved = false;
const container = document.getElementById("videoContainer");
const model = document.getElementById("model");

// tap
// 问题：drag由于存在鼠标点击的动作也会被判断成click从而触发戳一戳
container.addEventListener("click", (event) => {
    // alert(model.autoplay);
    if(!model.paused && !isTapping && !mouseMoved){
        isTapping = true;
        // model.pause();
        model.loop = false;
        window.PyHandler.tapped();
        model.addEventListener("ended", (event) => {
            window.PyHandler.reverse_to_default();
            model.loop = true;
            isTapping = false;
        });
    }
});

// drag
container.addEventListener("mousedown", (event) => {
    isMouseDown = true;
    const mouseX = event.screenX;
    const mouseY = event.screenY;
    window.PyHandler.drag_start(mouseX, mouseY);
    // window.PyHandler.dragging("mouse down");
});

container.addEventListener("mouseup", (event) => {
    isMouseDown = false;
    mouseMoved = false;
    // window.PyHandler.dragging("mouse up");
});

container.addEventListener("mousemove", (event) => {
    if(isMouseDown){
        mouseMoved = true;
        const mouseX = event.screenX;
        const mouseY = event.screenY;
        window.PyHandler.dragging(mouseX, mouseY);
    }
});
