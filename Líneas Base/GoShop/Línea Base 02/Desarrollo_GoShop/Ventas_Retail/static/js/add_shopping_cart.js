const divUserPc = document.getElementById("user-pc");
const backProductDescription = document.getElementById("back_product_description");
const sectionCart = document.getElementById("section-cart");
const sectionCartForm = document.getElementById("form-cart");
const formInputs = document.querySelectorAll(".cart-form__input");
const formSelects = document.querySelectorAll(".form__select");
const productId = window.data.product_id;

const addProduct = async (id) => {
    try {
        const response = await fetch(`../../../products/add_product/${id}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

document.getElementById("form-single-product").addEventListener("submit", async (e) => {
    if (divUserPc) {
        e.preventDefault();
        const data = await addProduct(productId);
        document.getElementById("shopcart-quantity").innerHTML = `Hay ${data.total_quantity} productos en el carrito`;
        document.getElementById("product-quantity").innerHTML = `<b>Cantidad del producto: ${data.product.product[0].quantity}</b>`;
        if (document.getElementById("product-on_sale-price")) {
            document.getElementById("total-price").innerHTML = `<b>Precio total: ${data.product.product[0].quantity * parseFloat(data.product.product[0].sale_price).toFixed(2)}</b>`;
        } else {
            document.getElementById("total-price").innerHTML = `<b>Precio total: ${data.product.product[0].quantity * parseFloat(data.product.product[0].price).toFixed(2)}</b>`;
        }
        const articleStock = document.getElementById(`single-stock-article`);
        if (articleStock.innerHTML === `<b>Stock disponible: 0</b>`) {
            span.style.display = "flex";
            span.style.color = "#f00";
            span.innerText = "Se han agotado los artículos.";
            setTimeout(() => {
                span.style.display = "none";
            }, 10000);
        } else {
            sectionCart.style.display = "flex";
            backProductDescription.style.display = "flex";
            setTimeout(() => {
                sectionCartForm.classList.add("section-cart__form-show");
            }, 0);
        }
    }
})

backProductDescription.addEventListener("click", () => {
    sectionCart.style.display = "none";
    sectionCartForm.classList.remove("section-cart__form-show");
})

// sectionCartForm.addEventListener("submit", async (e) => {
//     e.preventDefault();
//     if (!divUserPc){
//         sectionCartForm.style.border = "4px solid #d00";
//         setTimeout(() => {
//             sectionCartForm.style.border = "0px solid transparent";
//         }, 2000);
//     } else {
//         console.log("tas registrado");
//     }
// })