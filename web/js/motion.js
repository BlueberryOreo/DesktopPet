let isMouseDown = false;
let isTapping = false;
const container = document.getElementById("videoContainer");
const model = document.getElementById("model");

// tap
container.addEventListener("click", (event) => {
    // alert(model.autoplay);
    if(!model.paused && !isTapping){
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
    // window.PyHandler.dragging("mouse up");
});

container.addEventListener("mousemove", (event) => {
    if(isMouseDown){
        const mouseX = event.screenX;
        const mouseY = event.screenY;
        window.PyHandler.dragging(mouseX, mouseY);
    }
});