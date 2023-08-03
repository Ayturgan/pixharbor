const wrapper = document.querySelector(".wrapper_upload");
const fileName = document.querySelector(".file-name");
const defaultBtn = document.querySelector("#default-btn");
const customBtn = document.querySelector("#custom-btn");
const cancelBtn = document.querySelector("#cancel-btn ion-icon");
const img = document.querySelector("#img_upl");
let regExp = /[0-9a-zA-Z\^\&\'\@\{\}\[\]\,\$\=\!\-\#\(\)\.\%\+\~\_ ]+$/;

function defaultBtnActive() {
    defaultBtn.click();
}

if (!img.src) {
    img.classList.add("hidden");
}

defaultBtn.addEventListener("change", function () {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function () {
            const result = reader.result;
            img.src = result;
            img.classList.remove("hidden"); // Удалить класс hidden, чтобы показать изображение
            wrapper.classList.add("active");
        };
        cancelBtn.addEventListener("click", function () {
            img.src = "";
            img.classList.add("hidden"); // Добавить класс hidden, чтобы скрыть изображение
            wrapper.classList.remove("active");
        });
        reader.readAsDataURL(file);
    }
    if (this.value) {
        let valueStore = this.value.match(regExp);
        fileName.textContent = valueStore;
    }
});
