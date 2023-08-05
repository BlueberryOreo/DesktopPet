let isMouseDown = false;
const container = document.getElementById("videoContainer");
const model = document.getElementById("model");

// tap
container.addEventListener("click", (event) => {
    // alert(model.autoplay);
    if(!model.paused){
        model.pause();
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
    // window.PyHandler.dragging("mouse up");
});

container.addEventListener("mousemove", (event) => {
    if(isMouseDown){
        const mouseX = event.screenX;
        const mouseY = event.screenY;
        window.PyHandler.dragging(mouseX, mouseY);
    }
});