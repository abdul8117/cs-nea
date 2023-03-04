// // const link = document.querySelectorAll('a');
// // console.log(link)
// // link[0].textContent = "This Is A Link.";
// // link[1].target = "_blank";
// // link[0].href = "https://www.google.com";

// // link.forEach(a => {
// //     a.href = "https://www.google.com";
// //     a.target = "_blank"
// // });

// const confirmPasswordField = document.querySelector("#confirm-password");

// const registerTab = document.querySelector("#register-tab");
// const logInTab = document.querySelector("#log-in-tab")

// const usernameField = document.querySelector("#username-field");
// const nameFields = document.querySelector("#name-fields");

// const logInButton = document.querySelector("#log-in-button");
// const registerButton = document.querySelector("#register-button");
// // const forgotPasswordButton = document.querySelector("#forgot-password");


// logInTab.onclick = function logInForm() {
//     logInTab.className = "is-active";
//     registerTab.className = "";

//     confirmPasswordField.style.display = "none";
//     // forgotPasswordButton.style.display = "inline-flex";

//     usernameField.style.display = "block";
//     nameFields.style.display = "none";

//     logInButton.style.display = "inline-flex";
//     registerButton.style.display = "none";
// }

// registerTab.onclick = function registerForm() {
//     logInTab.className = "";
//     registerTab.className = "is-active";

//     confirmPasswordField.style.display = "block";
//     // forgotPasswordButton.style.display = "none";

//     usernameField.style.display = "none";
//     nameFields.style.display = "block"

//     logInButton.style.display = "none";
//     registerButton.style.display = "inline-flex";
// }


// const studentRadio = document.querySelector("#student-radio");
// const teacherRadio = document.querySelector("#teacher-radio");
// const yearGroupDropdown = document.querySelector("#year-group-dropdown");

// function showYearGroups() {
//     // show the year group dropdown list
//     yearGroupDropdown.style.display = "block";
// }

// function hideYearGroups() {
//     // hide the year groups dropdown list
//     yearGroupDropdown.style.display = "none";
// }


// const studentButton = document.querySelector("#student-button")
// const teacherButton = document.querySelector("#teacher-button")

// studentButton.onclick = function toggleStudentButton() {
//     // add the is-dark class to the button's class list and display the year group dropdown
//     studentButton.classList.toggle("is-dark");

//     if (yearGroupDropdown.style.display == "none") {
//         yearGroupDropdown.style.display = "block";
//     } else {
//         yearGroupDropdown.style.display == "none";
//     }

//     if (teacherButton.classList.contains("is-dark")) {
//         teacherButton.classList.toggle("is-dark");
//     }
// }

// teacherButton.onclick = function toggleteacherButton() {
//     teacherButton.classList.toggle("is-dark");
//     yearGroupDropdown.style.display = "none";

//     if (studentButton.classList.contains("is-dark")) {
//         studentButton.classList.toggle("is-dark");
//     }
// }


const studentFormTab = document.querySelector("#student-form-tab");
const studentForm = document.querySelector("#student-form");
const teacherFormTab = document.querySelector("#teacher-form-tab");
const teacherForm = document.querySelector("#teacher-form");


studentFormTab.onclick = function toggleStudentForm() {
  if (studentForm.style.display == "none") {
    studentForm.style.display = "block";
    teacherForm.style.display = "none";
    studentFormTab.classList.add("is-active");
    teacherFormTab.classList.remove("is-active");
  }
}

teacherFormTab.onclick = function toggleTeacherForm() {
  if (teacherForm.style.display == "none") {
    studentForm.style.display = "none";
    teacherForm.style.display = "block";
    teacherFormTab.classList.add("is-active");
    studentFormTab.classList.remove("is-active");
  }
}