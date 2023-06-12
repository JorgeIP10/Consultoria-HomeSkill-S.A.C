const divUserPc = document.getElementById("user-pc");
const backProductDescription = document.getElementById("back_product_description");
const sectionCart = document.getElementById("section-cart");
const sectionCartForm = document.getElementById("form-cart");
const formInputs = document.querySelectorAll(".cart-form__input");
const formSelects = document.querySelectorAll(".form__select");
const productId = window.data.product_id;

const getQuantityProductCart = async (id) => {
    try {
        const response = await fetch(`../../../shopping_cart/${id}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

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
        const dataCart = await getQuantityProductCart(productId);
        const productStock = document.getElementById("single-stock-article").innerText.split("Stock disponible: ")[1];
        if (productStock == dataCart.quantity) {
            document.getElementById("warning").style.display = "initial";
            setTimeout(() => {
                document.getElementById("warning").style.display = "none";
            }, 5000);
        } else {
            const data = await addProduct(productId);
            document.getElementById("shopcart-quantity").innerHTML = `Hay ${data.total_quantity} productos en el carrito`;
            document.getElementById("product-quantity").innerHTML = `<b>Cantidad del producto: ${data.product.quantity}</b>`;
            if (document.getElementById("product-on_sale-price")) {
                document.getElementById("total-price").innerHTML = `<b>Precio total: $${(data.product.quantity * parseFloat(data.product.sale_price)).toFixed(2)}</b>`;
            } else {
                document.getElementById("total-price").innerHTML = `<b>Precio total: $${(data.product.quantity * parseFloat(data.product.price)).toFixed(2)}</b>`;
            }
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