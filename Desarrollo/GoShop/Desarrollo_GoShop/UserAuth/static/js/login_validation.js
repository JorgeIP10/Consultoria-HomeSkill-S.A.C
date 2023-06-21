const error_login = document.getElementById("error-login");
const eyeIcon = document.getElementById("eye-icon");
const inputs = document.querySelectorAll(".form__input");

const validations = {
    username: /^(?!.*\.\.|.*_\.|.*\._|.*__)(?!\.|_)(?=.*[a-zA-Z])[a-zA-Z0-9._]{5,20}(?<!\.|_)$/,
    password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z])[^\s]{8,}$/,
};

const fields = {
    username: false,
    password: false,
};

const validateFieldKeyUp = (expression, input, field) => {
    document.getElementById("error-login").style.display = "none";
    if (expression.test(input.value)) {
        input.parentNode.classList.remove("form__div-input-error");
        fields[field] = true;
    } else {
        fields[field] = false;
        input.parentNode.classList.add("form__div-input-error");
        if (!input.value) {
            input.parentNode.classList.remove("form__div-input-error");
        }
    }
};

const validateFormKeyUp = (e) => {
    switch (e.target.name) {
        case "username":
            validateFieldKeyUp(validations.username, e.target, "username");
            break;
        case "password":
            validateFieldKeyUp(validations.password, e.target, "password");
            break;
    }
};

inputs.forEach((input) => {
    input.addEventListener("keyup", validateFormKeyUp);
});

eyeIcon.addEventListener("click", (e) => {
    if (e.target.previousElementSibling.type === "text") {
        e.target.previousElementSibling.setAttribute("type", "password");
    } else {
        e.target.previousElementSibling.setAttribute("type", "text");
    }
})

document.getElementById("form").addEventListener("submit", function (e) {
    if (!fields.username || !fields.password) {
        e.preventDefault();
        document.getElementById("error-submit").style.display = "flex";
        setTimeout(() => {
            document.getElementById("error-submit").style.display = "none";
        }, 3000);
    }
});