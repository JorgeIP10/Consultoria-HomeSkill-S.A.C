const formPayment = document.getElementById("form-payment");
const formInputs = document.querySelectorAll(".form__input");
const formSelects = document.querySelectorAll(".form__select");

const validations = {
    card: /^(4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$/,
    cvv: /^\d{3,4}$/
};

const fields = {
    card: false,
    cvv: false,
    selects: false
};

document.getElementById("view-methods").addEventListener("click", (e) => {
    document.getElementById("site-main").style.display = "grid";
    document.getElementById("div-add-card").style.display = "none";
    document.getElementById("div-payment-view-cards").style.display = "grid";
})

document.getElementById("add-method").addEventListener("click", (e) => {
    document.getElementById("site-main").style.display = "grid";
    document.getElementById("div-payment-view-cards").style.display = "none";
    document.getElementById("div-add-card").style.display = "grid";
})

window.addEventListener("load", () => {
    if (document.getElementById("error-title")) {
        document.getElementById("button-remember-card").style.display = "none";
    }
    document.querySelectorAll(".card-number").forEach((card) => {
        let number = card.innerText;
        for (let i = 0; i < number.length; i++){
            if (i < number.length - 4) {
                number = number.replace(number[i], "*");
            }
        }
        card.innerText = number;
    })
})

const validateFieldKeyUp = (expression, input, field) => {
    if (expression.test(input.value)) {
        input.classList.remove("form__input-error");
        fields[field] = true;
    } else {
        input.classList.add("form__input-error");
        fields[field] = false;
        if (!input.value) {
            input.classList.remove("form__input-error");
        }
    }
};

const validateFormKeyUp = (e) => {
    switch (e.target.name) {
        case "card":
            validateFieldKeyUp(validations.card, e.target, "card");
            break;
        case "cvv":
            validateFieldKeyUp(validations.cvv, e.target, "cvv");
            break;
    }
};

formInputs.forEach((input) => {
    input.addEventListener("keyup", validateFormKeyUp);
});

formSelects.forEach((select) => {
    select.addEventListener("change", (e) => {
        if (select.value == "--" || select.value == "----"){
            select.classList.add("form__select-error");
        }
        else{
            select.classList.remove("form__select-error");
        }
    })
})

function validateFormSelect(){
    counter = 0;
    formSelects.forEach((select) => {
        if (select.value != "--" && select.value != "----"){
            counter++;
        }

        if (counter == 2){
            fields.selects = true;
        }
        else{
            fields.selects = false;
        }
    })
}

formPayment.addEventListener("submit", (e) => {
    validateFormSelect();
    if (!fields.card || !fields.cvv || !fields.selects){
        e.preventDefault();
        document.getElementById("error-add").style.display = "initial";
        document.getElementById("error-add").innerHTML = "Rellene los campos correctamente.";
        setTimeout(() => {
            document.getElementById("error-add").style.display = "none";
        }, 3000);
    }
});

const checkEvent = () => {
    document.querySelectorAll(".check").forEach((checkbox) => {
        checkbox.addEventListener("change", (e) => {
            document.querySelectorAll(".check").forEach((check) => {
                if (check.checked) {
                    document.getElementById("remember-card").setAttribute("value", check.id);
                    check.disabled = false;
                } else {
                    check.disabled = true;
                }
                if (!e.target.checked) {
                    document.getElementById("remember-card").setAttribute("value", " ");
                    check.disabled = false;
                }
            })
        })
    })
}

checkEvent();

document.getElementById("form-view-cards").addEventListener("submit", (e) => {
    if (document.getElementById("remember-card").value === " ") {
        e.preventDefault();
        document.getElementById("error-remember").style.display = "initial";
        document.getElementById("error-remember").innerHTML = "Debe seleccionar una tarjeta para recordar.";
        setTimeout(() => {
            document.getElementById("error-remember").style.display = "none";
        }, 3000);
    }
});