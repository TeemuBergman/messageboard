const textarea = document.getElementById("content");

textarea.addEventListener("input", event => {
    const target = event.currentTarget;
    const maxLength = target.getAttribute("maxlength");
    const currentLength = target.value.length;

    let countRemaining = document.getElementById("charactersRemaining");
    countRemaining.textContent = currentLength + "/" + (maxLength) + " characters";
});