const pendingTab = document.querySelector("#pending-tab");
const pendingAssignments = document.querySelector("#pending-assignments");
const overdueTab = document.querySelector("#overdue-tab");
const overdueAssignments = document.querySelector("#overdue-assignments");

pendingTab.onclick = function showPendingAssignments() {
    if (pendingAssignments.style.display == "none") {
        pendingTab.classList.add("is-active");
        overdueTab.classList.remove("is-active");
        pendingAssignments.style.display = "block";
        overdueAssignments.style.display = "none";
    }
}

overdueTab.onclick = function showOverdueAssignments() {
    if (overdueAssignments.style.display == "none") {
        overdueTab.classList.add("is-active");
        pendingTab.classList.remove("is-active");
        overdueAssignments.style.display = "block";
        pendingAssignments.style.display = "none";
    }
}