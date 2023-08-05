let isMouseDown = false;
const source = document.getElementById("videoContainer");

source.addEventListener("mousedown", (event) => {
    isMouseDown = true;
    const mouseX = event.screenX;
    const mouseY = event.screenY;
    window.PyHandler.drag_start(mouseX, mouseY);
    // window.PyHandler.dragging("mouse down");
});

source.addEventListener("mouseup", (event) => {
    isMouseDown = false;
    // window.PyHandler.dragging("mouse up");
});

source.addEventListener("mousemove", (event) => {
    if(isMouseDown){
        const mouseX = event.screenX;
        const mouseY = event.screenY;
        window.PyHandler.dragging(mouseX, mouseY);
    }
});