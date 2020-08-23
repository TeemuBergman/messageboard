function toggle_visibility(message_id) {
    let selector = document.querySelector(".visibility-" + message_id);

    if (selector.style.display === "none") {
        selector.style.display = "block"
    } else {
        selector.style.display = "none"
    }
}

/*
function toggle_visibility() {
    let selector = document.querySelectorAll(".visibility");

    selector.forEach(function (changeVisibility) {
        if (changeVisibility.style.display === "none") {
            changeVisibility.style.display = "table-cell"
        } else {
            changeVisibility.style.display = "none"
        }
    })
}
*/