const inputs = document.querySelectorAll(".form__input");
const formSelects = document.querySelectorAll(".form__select");

window.addEventListener("load", () => {
    const quantity = document.getElementById("total-quantity").innerText.split(" artículos")[0];
    document.getElementById("total-delivery").innerText = `$${parseInt(quantity) * 10}`;
    document.getElementById("total-to-pay").innerText = `$${(parseInt(quantity) * 10) + parseFloat(document.getElementById("total-price-all").innerText.split("$")[1])}`;
});

const validations = {
    name: /^[A-Za-zÁÉÍÓÚáéíóúñÑ\s]+$/,
    dni: /^\d{8}$/
};

const fields = {
    name: false,
    lastName: false,
    dni: false
};

const validateFieldKeyUp = (expression, input, field) => {
    if (expression.test(input.value)) {
        input.classList.remove("form__input-error");
        fields[field] = true;
    } else {
        fields[field] = false;
        input.classList.add("form__input-error");
        if (!input.value) {
            input.classList.remove("form__input-error");
        }
    }
};

const validateFormKeyUp = (e) => {
    switch (e.target.name) {
        case "name":
            validateFieldKeyUp(validations.name, e.target, "name");
            break;
        case "last_name":
            validateFieldKeyUp(validations.name, e.target, "lastName");
            break;
        case "dni":
            validateFieldKeyUp(validations.dni, e.target, "dni");
            break;
    }
};

inputs.forEach((input) => {
    input.addEventListener("keyup", validateFormKeyUp);
});

const saveUserInfo = async (names, surnames, dni, address) => {
    try {
        const response = await fetch(`../../../shopping_cart/buy/${names}/${surnames}/${dni}/${address}`);
        if (!response.ok) {
            console.log('Error en la operación');
        }
    } catch (error) {
        console.log(error);
    }
};

document.getElementById("form-personal_info").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!validations.name.test(document.getElementById("name").value) || !validations.name.test(document.getElementById("last_name").value) || !fields.dni) {
        document.getElementById("span-error-personal-info").style.display = "flex";
        setTimeout(() => {
            document.getElementById("span-error-personal-info").style.display = "none";
        }, 3000);
    } else {
        await saveUserInfo(document.getElementById("name").value, document.getElementById("last_name").value, document.getElementById("dni").value, document.getElementById("address").value);
        document.getElementById("loag-image").style.display = "initial";
        document.querySelectorAll(".form__input-personal_info").forEach((input) => {
            input.style.pointerEvents = "none";
            input.style.opacity = "0.5";
        });
        document.querySelectorAll(".form__label-personal_info").forEach((input) => {
            input.style.opacity = "0.5";
        });
        setTimeout(() => {
            document.getElementById("form-personal_info").style.display = "none";
            document.getElementById("titles-container-personal-info").style.borderBottom = "none";
            document.getElementById("personal-info-title-number").style.display = "none";
            document.getElementById("personal-info-title-check").style.display = "flex";
            document.getElementById("div-edit-personal-info").style.display = "flex";
            document.getElementById("payment-info").style.display = "grid";
            document.getElementById("loag-image").style.display = "none";
        }, 3000);
    }
});

document.getElementById("div-edit-personal-info").addEventListener("click", () => {
    document.getElementById("form-personal_info").style.display = "grid";
    document.getElementById("titles-container-personal-info").style.borderBottom = "1px solid #828080";
    document.getElementById("personal-info-title-number").style.display = "flex";
    document.getElementById("personal-info-title-check").style.display = "none";
    document.getElementById("div-edit-personal-info").style.display = "none";
    document.getElementById("payment-info").style.display = "none";
    document.querySelectorAll(".form__input-personal_info").forEach((input) => {
        input.style.pointerEvents = "all";
        input.style.opacity = "1";
    });
    document.querySelectorAll(".form__label-personal_info").forEach((input) => {
        input.style.opacity = "initial";
    });
});

document.getElementById("paypal-form").addEventListener("submit", (e) => {
    let response = grecaptcha.getResponse();

    if(response.length == 0){
        e.preventDefault();
        document.getElementById("error-captcha").style.display = "initial";
        document.getElementById("error-captcha").innerHTML = "Complete el captcha.";
        setTimeout(() => {
            document.getElementById("error-captcha").style.display = "none";
        }, 3000);
    }
});