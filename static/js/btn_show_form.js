// Wherever there are forms that need to be shown or hidden with a button, this JavaScript is used.

const button = document.querySelector("#btn-js");
const form = document.querySelector("#form-js");

button.onclick = function toggleForm() {
    if (form.style.display == "none"){
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}