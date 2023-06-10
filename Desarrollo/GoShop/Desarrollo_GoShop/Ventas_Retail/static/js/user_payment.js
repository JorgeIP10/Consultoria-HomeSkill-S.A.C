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

const addPaymentMethod = async () => {
    const formData = new FormData(formPayment);
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value; 
    formData.append('csrfmiddlewaretoken', csrf_token);
    try {
        const response = await fetch('/profile/payment/add_payment_method', {
        method: 'POST',
        body: formData
        });
        const data = response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

let counterAdd = 0;
formPayment.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (counterAdd < 1) {
        validateFormSelect();
        if (!fields.card || !fields.cvv || !fields.selects){
            document.getElementById("error-add").style.display = "initial";
            document.getElementById("error-add").innerHTML = "Rellene los campos correctamente.";
            setTimeout(() => {
                document.getElementById("error-add").style.display = "none";
            }, 3000);
        } else {
            const data = await addPaymentMethod();
            if (data.data.message) {
                if (document.getElementById("error-title")) {
                    document.getElementById("error-title").style.display = "none";
                    document.getElementById("button-remember-card").style.display = "initial";
                }
                document.getElementById("grid-main").innerHTML += 
                `<div class="div-view-cards">
                    <div class="div-payment__container">
                        <div class="card-container">
                            <p class="card-number">${"*".repeat(data.data.card.number.length - 4) + data.data.card.number.slice(-4)}</p>
                            <div class="info-container">
                                <p class="card-owner">${document.getElementById("hello-user-pc").innerText.split("Hola, ")[1]}</p>
                                <p class="card-expiration-date">${data.data.card.expiration_month} / ${data.data.card.expiration_year}</p>
                            </div>
                        </div>
                    </div>
                    <div class="checkbox-container"><input class="check" id="${data.data.card.id}" type="checkbox"></div>
                </div>`;
                checkEvent();
                document.getElementById("message-add").style.display = "initial";
                document.getElementById("message-add").innerHTML = data.data.message;
                setTimeout(() => {
                    document.getElementById("message-add").style.display = "none";
                }, 3000);
            } else {
                document.getElementById("error-add").style.display = "initial";
                document.getElementById("error-add").innerHTML = data.data.error;
                setTimeout(() => {
                    document.getElementById("error-add").style.display = "none";
                }, 3000);
            }
            counterAdd++;
        }
    } else {
        document.getElementById("csrf-error-add").style.display = "initial";
        document.getElementById("csrf-error-add").innerHTML = "Error al intentar agregar la tarjeta, recargue la página.";
        setTimeout(() => {
            document.getElementById("csrf-error-add").style.display = "none";
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

const rememberPaymentMethod = async () => {
    const formData = new FormData(document.getElementById("form-view-cards"));
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value; 
    formData.append('csrfmiddlewaretoken', csrf_token);
    try {
        const response = await fetch('/profile/payment/remember_payment_method', {
        method: 'POST',
        body: formData
        });
        const data = response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

let counterView = 0;
document.getElementById("form-view-cards").addEventListener("submit", async (e) => {
    e.preventDefault();
    if (counterView < 1) {
        if (document.getElementById("remember-card").value === " ") {
            document.getElementById("error-remember").style.display = "initial";
            document.getElementById("error-remember").innerHTML = "Debe seleccionar una tarjeta para recordar.";
            setTimeout(() => {
                document.getElementById("error-remember").style.display = "none";
            }, 3000);
        } else {
            const data = await rememberPaymentMethod();
            counterView++;
            if (data.data.message) {
                document.getElementById("message-remember").style.display = "initial";
                document.getElementById("message-remember").innerHTML = data.data.message;
                setTimeout(() => {
                    document.getElementById("message-remember").style.display = "none";
                }, 3000);
            } else {
                document.getElementById("message-remember").style.display = "initial";
                document.getElementById("message-remember").innerHTML = data.data.message_without_remember;
                setTimeout(() => {
                    document.getElementById("message-remember").style.display = "none";
                }, 3000);
            }
        }
    } else {
        document.getElementById("csrf-error-view").style.display = "initial";
        document.getElementById("csrf-error-view").innerHTML = "Error al intentar recordar la tarjeta, recargue la página.";
        setTimeout(() => {
            document.getElementById("csrf-error-view").style.display = "none";
        }, 3000);
    }
})