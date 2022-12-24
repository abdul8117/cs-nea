const button = document.querySelector("#btn-js");
const form = document.querySelector("#form-js");

console.log(button);

button.onclick = function toggleForm() {
    if (form.style.display == "none"){
        form.style.display = "block";
    } else {
        form.style.display = "none";
    }
}