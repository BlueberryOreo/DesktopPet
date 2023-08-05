let isMouseDown = false;
const source = document.getElementById("videoContainer");

source.addEventListener("mousedown", (event) => {
    isMouseDown = true;
    window.PyHandler.dragging("mouse down");
});

source.addEventListener("mouseup", (event) => {
    isMouseDown = false;
    window.PyHandler.dragging("mouse up");
});

source.addEventListener("mousemove", (event) => {
    if(isMouseDown){
        const mouseX = event.clientX;
        const mouseY = event.clientY;
        window.PyHandler.dragging(mouseX, mouseY);
    }
});