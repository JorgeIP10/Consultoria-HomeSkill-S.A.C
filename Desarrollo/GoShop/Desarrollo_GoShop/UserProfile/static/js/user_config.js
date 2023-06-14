document.getElementById("edit-username").addEventListener("click", (e) => {
    document.getElementById("div-edit").style.display = "grid";
    document.getElementById("form-edit-container-username").style.display = "grid";
    document.getElementById("form-edit-container-password").style.display = "none";
})

document.getElementById("edit-password").addEventListener("click", (e) => {
    document.getElementById("div-edit").style.display = "grid";
    document.getElementById("form-edit-container-password").style.display = "grid";
    document.getElementById("form-edit-container-username").style.display = "none";
})

const validations = {
    username: /^(?!.*\.\.|.*_\.|.*\._|.*__)(?!\.|_)(?=.*[a-zA-Z])[a-zA-Z0-9._]{5,20}(?<!\.|_)$/,
    password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z])[^\s]{8,}$/
}

const fields = {
    username: false,
    password: false
};

const validateFieldKeyUp = (expression, input, field) => {
    if (expression.test(input.value)) {
        input.classList.remove("div__input-error");
        fields[field] = true;
    } else {
        fields[field] = false;
        input.classList.add("div__input-error");
        if (!input.value) {
            input.classList.remove("div__input-error");
        }
    }
};

const validatePasswordKeyUp = (input) => {
    const newPassword = document.getElementById("new-password");
    const repeatPassword = document.getElementById("repeat-password");
    if (validations.password.test(input.value)) {
        input.classList.remove("div__input-error");
        if (newPassword.value === repeatPassword.value) {
            fields.password = true;
            newPassword.classList.remove("div__input-error-match");
            repeatPassword.classList.remove("div__input-error-match");
        } else {
            fields.password = false;
            if (newPassword.value && repeatPassword.value) {
                newPassword.classList.add("div__input-error-match");
                repeatPassword.classList.add("div__input-error-match");
            }
        }
    } else {
        fields.password = false;
        input.classList.remove("div__input-error-match");
        input.classList.add("div__input-error");
        if (!input.value) {
            input.classList.remove("div__input-error-match");
            input.classList.remove("div__input-error");
        }
    }
};

const validateFormKeyUp = (e) => {
    switch (e.target.name) {
        case "username":
            if (document.getElementById("error-submit-username-auth")) {
                document.getElementById("error-submit-username-auth").style.display = "none";
            }
            validateFieldKeyUp(validations.username, e.target, "username");
            break;
        case "password":
            if (document.getElementById("error-submit-username-auth")) {
                document.getElementById("error-submit-username-auth").style.display = "none";
            }
            break;
        case "current-password":
            if (document.getElementById("error-submit-password-auth")) {
                document.getElementById("error-submit-password-auth").style.display = "none";
            }
            break;
        case "new-password":
            validatePasswordKeyUp(e.target);
            break;
        case "repeat-password":
            validatePasswordKeyUp(e.target);
            break;
    }
};

document.querySelectorAll(".div__input").forEach((input) => {
    input.addEventListener("keyup", validateFormKeyUp);
});

document.getElementById("form-edit-container-username").addEventListener("submit", (e) => {
    const username = document.getElementById("username").value;
    if (!validations.username.test(username)) {
        e.preventDefault();
        document.getElementById("error-submit-username").style.display = "flex";
        setTimeout(() => {
            document.getElementById("error-submit-username").style.display = "none";
        }, 3000);
    }
});

document.getElementById("form-edit-container-password").addEventListener("submit", (e) => {
    if (!fields.password){
        e.preventDefault();
        document.getElementById("error-submit-password").style.display = "flex";
        setTimeout(() => {
            document.getElementById("error-submit-password").style.display = "none";
        }, 3000);
    }
});