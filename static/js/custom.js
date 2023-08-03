// const gallery = document.getElementById("gallery");
// const classes = ["", "horizontal", "vertical"];

// for (let i = 0; i < 65; i++) {
//     const idx = Math.floor(Math.random() * classes.length);
//     const div = document.createElement("div");
//     div.className = `image ${classes[idx]}`;
//     div.style.backgroundImage = `url(https://source.unsplash.com/featured/?natural&${i})`;
//     gallery.appendChild(div);
// }

/* Когда пользователь нажимает на кнопку,
переключение между скрытием и отображением раскрывающегося содержимого */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Закройте выпадающее меню, если пользователь щелкает за его пределами
window.onclick = function (event) {
    if (!event.target.closest(".dropbtn")) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains("show")) {
                openDropdown.classList.remove("show");
            }
        }
    }
};

document.getElementById("active").addEventListener("change", function () {
    var icon = document.getElementById("menu-icon");
    if (this.checked) {
        icon.textContent = "close"; // Иконка закрытия
    } else {
        icon.textContent = "menu"; // Иконка меню
    }
});

function confirmDelete() {
    return confirm("Are you sure you want to delete this post?");
}
