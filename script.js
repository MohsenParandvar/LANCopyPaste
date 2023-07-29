fetch("message.txt")
    .then((res) => res.text())
    .then((text) => {
        document.getElementById("clipboard").value = text
    })
    .catch((e) => console.error(e));

function copyToClipboard() {
    var textarea = document.getElementById("clipboard");

    var tempInput = document.createElement("input");
    tempInput.value = textarea.value;
    document.body.appendChild(tempInput);
    tempInput.select();

    document.execCommand("copy");

    document.body.removeChild(tempInput);

    alert("The text has been copied to the clipboard.");
}