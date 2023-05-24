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
            validateFieldKeyUp(validations.username, e.target, "username");
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

const changeUsername = async (username) => {
    try {
        const response = await fetch(`/profile/config/${username}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

let currentPassword = window.data.password;
document.getElementById("form-edit-container-username").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    if (validations.username.test(username) && document.getElementById("password-div-username").value === currentPassword) {
        const data = await changeUsername(username);
        if (document.getElementById("error-submit-username").style.display === "flex") {
            document.getElementById("error-submit-username").style.display = "none";
        }
        document.getElementById("span-username").innerHTML = data.username;
        document.getElementById("hello-user-pc").innerHTML = `Hola, ${data.username}`;
        document.getElementById("success-submit-username").style.display = "flex";
        setTimeout(() => {
            document.getElementById("success-submit-username").style.display = "none";
        }, 3000);
    } else {
        document.getElementById("error-submit-username").style.display = "flex";
        setTimeout(() => {
            document.getElementById("error-submit-username").style.display = "none";
        }, 3000);
    }
})

const changePassword = async () => {
    const formData = new FormData(document.getElementById("form-edit-container-password"));
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value; 
    formData.append('csrfmiddlewaretoken', csrf_token);
    try {
        await fetch('/profile/config/change/password', {
        method: 'POST',
        body: formData
        });
    } catch (error) {
        console.log(error);
    }
}

let firstPassword = window.data.password;
let cont = 0;
document.getElementById("form-edit-container-password").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (fields.password && document.getElementById("password-div-password").value === currentPassword){
        await changePassword();
        if (document.getElementById("error-submit-password").style.display === "flex") {
            document.getElementById("error-submit-password").style.display = "none";
        }
        if (document.getElementById("error-submit-password-auth").style.display === "flex") {
            document.getElementById("error-submit-password-auth").style.display = "none";
        }
        document.getElementById("success-submit-password").style.display = "flex";
        setTimeout(() => {
            document.getElementById("success-submit-password").style.display = "none";
        }, 3000);
        if (firstPassword != currentPassword) {
            document.getElementById("success-submit-password").style.display = "none";
            document.getElementById("error-submit-password").style.display = "flex";
            document.getElementById("error-submit-password").innerHTML = "<b>Error al intentar cambiar la contraseña, recargue la página.</b>";
            setTimeout(() => {
                document.getElementById("error-submit-password").style.display = "none";
            }, 3000);
        }
        cont++;
        if (cont <= 1) {
            currentPassword = document.getElementById("new-password").value;
        }
    } else {
        if (!fields.password) {
            document.getElementById("error-submit-password").style.display = "flex";
            setTimeout(() => {
                document.getElementById("error-submit-password").style.display = "none";
            }, 3000);
        } else {
            document.getElementById("error-submit-password-auth").style.display = "flex";
            setTimeout(() => {
                document.getElementById("error-submit-password-auth").style.display = "none";
            }, 3000);
        }
    }
})