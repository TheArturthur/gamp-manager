function checkProjectSelection() {
    const targets_table_caption = "Targets already present in the Project ";
    if (document.getElementById("new_project").selected) {
        document.getElementById("targets_table").style.display = "none";
        document.getElementById("new_project_box").style.display = "contents";
        document.getElementById("submit_btn").innerHTML = "Add Project";
    } else {
        document.getElementById("new_project_box").style.display = "none";
        document.getElementById("submit_btn").innerHTML = "Add Target";
        document.getElementById("targets_table").style.display = "contents";
        document.getElementById("targets_table_caption").innerHTML = targets_table_caption + document.getElementById("selected_project_name").value + ":";

        let selected_project = document.getElementById("selected_project").value;
        const xhttp = new XMLHttpRequest();
        xhttp.onload = function () {
            document.getElementById("txtHint").innerHTML = this.responseText;
        }
        xhttp.open("GET", "targets.html?selected_project=" + selected_project);
        xhttp.send();
    }
}