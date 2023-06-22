const input = document.getElementById("search");
const form = document.getElementById("header-form");
const options = document.getElementById("options");
const backMain = document.getElementById("back_main");

const getProducts = async (text) => {
    try{
        if (document.getElementById("single_product-container")) {
            const response = await fetch(`../../../products/${text}`);
            const data = await response.json();
            return data.products;
        } else {
            const response = await fetch(`../products/${text}`);
            const data = await response.json();
            return data.products;
        }
    } catch (error) {
        console.log(error);
    }
}

const searchKeyUp = async (e) => {
    if (e.target.value) {
        const lista = await getProducts(e.target.value);
        if (lista[0]) {
            lista.forEach(element => {
                let content = `<div class="option">${element}</div>`;
                if (!options.innerHTML) {
                    options.innerHTML += content;
                } else {
                    let cont = 0;
                    document.querySelectorAll(".option").forEach((option) => {
                        if (option.innerHTML === element) {
                            cont++;
                            if (cont > 1) {
                                option.remove();
                            }
                        }
                    });
                    if (cont === 0) {
                        options.innerHTML += content;
                    }
                }
            });
        } else {
            document.querySelectorAll(".option").forEach((option) => {
                option.remove();
            });
        }
        if (options.innerText) {
            backMain.style.display = "flex";
        } else {
            backMain.style.display = "none";
        }
    } else {
        document.querySelectorAll(".option").forEach((option) => {
            option.remove();
        });
        backMain.style.display = "none";
    }

    document.querySelectorAll(".option").forEach((option) => {
        option.addEventListener("click", (e) => {
            input.value = e.target.innerHTML;
        });
    });
}

input.addEventListener("keyup", searchKeyUp);
backMain.addEventListener("click", (e) => {
    e.target.style.display = "none";
})