// hide all of the input fields 
const updateFields = document.querySelectorAll(".update-field");

updateFields.forEach(field => {
    field.style.display = "none";
});

// logic for toggling the input fields
const editIcons = document.querySelectorAll(".edit");
let formDivElement;

editIcons.forEach(icon => {
    icon.addEventListener('click', () => {
        formDivElement = icon.nextElementSibling;
        
        if (formDivElement.style.display == "none") {
            formDivElement.style.display = "block";
        }
        else {
            formDivElement.style.display = "none";
        }
    });
});