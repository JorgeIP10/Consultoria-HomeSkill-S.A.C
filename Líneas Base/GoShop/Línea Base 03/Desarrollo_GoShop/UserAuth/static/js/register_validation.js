const password1 = document.getElementById("password1");
const password2 = document.getElementById("password2");
const inputs = document.querySelectorAll(".form__input");
const eyeIcons = document.querySelectorAll(".imagen-ojo");

const validations = {
    username: /^(?!.*\.\.|.*_\.|.*\._|.*__)(?!\.|_)(?=.*[a-zA-Z])[a-zA-Z0-9._]{5,20}(?<!\.|_)$/,
    email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z])[^\s]{8,}$/
}

const fields = {
    username: false,
    email: false,
    password: false
}

const validateFieldKeyUp = (expression, input, field) => {
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

const validatePasswordKeyUp = (input) => {
    if (validations.password.test(input.value)) {
        input.parentNode.classList.remove("form__div-input-error");
        if (password1.value === password2.value) {
            fields.password = true;
            password1.parentNode.classList.remove("form__div-input-error-match");
            password2.parentNode.classList.remove("form__div-input-error-match");
        } else {
            fields.password = false;
            if (password1.value && password2.value) {
                password1.parentNode.classList.add("form__div-input-error-match");
                password2.parentNode.classList.add("form__div-input-error-match");
            }
        }
    } else {
        fields.password = false;
        input.parentNode.classList.remove("form__div-input-error-match");
        input.parentNode.classList.add("form__div-input-error");
        if (!input.value) {
            input.parentNode.classList.remove("form__div-input-error-match");
            input.parentNode.classList.remove("form__div-input-error");
        }
    }
};

const validateFormKeyUp = (e) => {
    switch (e.target.name) {
        case "username":
            validateFieldKeyUp(validations.username, e.target, "username");
            document.getElementById("error-username-register").style.display = "none";
            break;
        case "email":
            validateFieldKeyUp(validations.email, e.target, "email");
            break;
        case "password1":
            validatePasswordKeyUp(e.target);
            break;
        case "password2":
            validatePasswordKeyUp(e.target);
            break;
    }
};

const clickEyeIcon = (e) => {
    if (e.target.previousElementSibling.type === "text") {
        e.target.previousElementSibling.setAttribute("type", "password");
    } else {
        e.target.previousElementSibling.setAttribute("type", "text");
    }
}

inputs.forEach((input) => {
    input.addEventListener("keyup", validateFormKeyUp);
});

eyeIcons.forEach((icon) => {
    icon.addEventListener("click", clickEyeIcon);
})

document.getElementById("form").addEventListener("submit", function (e) {
    if (!fields.username || !fields.email || !fields.password) {
        e.preventDefault();
        document.getElementById("error-submit").style.display = "flex";
        setTimeout(() => {
            document.getElementById("error-submit").style.display = "none";
        }, 3000);
    }
});