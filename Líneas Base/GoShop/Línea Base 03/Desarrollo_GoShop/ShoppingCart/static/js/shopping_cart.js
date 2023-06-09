const quantities = document.querySelectorAll(".input-quantity-product");
const data = JSON.parse(window.data.id_products);
const totalPriceAll = document.getElementById("total-price-all");
const totalDelivery = document.getElementById("total-delivery");
const totalToPay = document.getElementById("total-to-pay");
const buttonsUp = document.querySelectorAll(".button-up");
const buttonsUpClick = document.querySelectorAll(".button-up-click");
const buttonsDown = document.querySelectorAll(".button-down");
const buttonsRemoveProduct = document.querySelectorAll(".icon-trash");
const buttonsDownClick = document.querySelectorAll(".button-down-click");
let totalProductQuantity = 0;

window.addEventListener("load", () => {
    if (totalPriceAll) {
        let productPrice = 0;
        let productQuantity = 0;
        let total = 0;
        const totalProductQuantity = JSON.parse(window.data.total_quantity);
        quantities.forEach((q) => {
            let spanId = q.getAttribute("id");
            let productId = spanId.split("input-quantity-product-")[1];
            for (let j = 0; j < data.length; j++) {
                if (data[j] == productId) {
                    productQuantity = q.value;
                    if (document.getElementById(`price-${productId}`)) {
                        productPrice = document.getElementById(`price-${productId}`).innerHTML;
                    } else {
                        productPrice = document.getElementById(`sale_price-${productId}`).innerHTML;
                    }
                    document.getElementById(`total_product_price-${productId}`).innerHTML =
                    `<b>$${parseFloat(productPrice * productQuantity).toFixed(2)}</b>`;
                    total += parseFloat(productPrice * productQuantity);
                    break;
                }
            }
        })
        totalPriceAll.innerHTML = `$${total.toFixed(2)}`;
        totalDelivery.innerHTML = `$${parseInt(totalProductQuantity * 10)}`;
        totalToPay.innerHTML = `<b>$${(totalProductQuantity * 10 + total).toFixed(2)}</b>`;
    }
});

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

buttonsUpClick.forEach((buttonUp) => {
    buttonUp.addEventListener("click", async (e) => {
        let productId = null;
        let inputQuantity = null;
        let data = null;
        let unitPrice = 0;
        productId = e.target.getAttribute("id").split("button-icon-up-")[1];
        if (!productId) {
            productId = e.target.getAttribute("id").split("button-up-")[1];
        }
        inputQuantity = document.getElementById(`input-quantity-product-${productId}`);

        if (inputQuantity.value != document.getElementById(`stock-${productId}`).innerText.split("Stock disponible: ")[1]) {
            if (e.target.getAttribute("id").startsWith("button-icon-up-")) {
                e.stopPropagation();
            }
            data = await addProduct(productId);
            if (document.getElementById(`sale_price-${productId}`)) {
                unitPrice = data.product.sale_price;
            } else {
                unitPrice = data.product.price;
            }
            const totalProductPrice = document.getElementById(`total_product_price-${productId}`);
            totalProductPrice.innerHTML =
                `<b>$${(parseFloat(totalProductPrice.innerText.split("$")[1]) + parseFloat(unitPrice)).toFixed(2)}</b>`;
    
            inputQuantity.value = parseInt(inputQuantity.value) + 1;
            document.getElementById("total-quantity").innerHTML = `${parseInt(data.total_quantity)} artículos`;
            totalPriceAll.innerHTML = `$${(parseFloat(unitPrice) + parseFloat(totalPriceAll.innerHTML.split("$")[1])).toFixed(2)}`;
            totalDelivery.innerHTML = `$${parseInt(totalDelivery.innerText.split("$")[1]) + 10}`;
            totalToPay.innerHTML = `<b>$${(parseFloat(totalPriceAll.innerHTML.split("$")[1]) + parseInt(totalDelivery.innerText.split("$")[1])).toFixed(2)}</b>`;
        }
    })
})

const removeProductUnit = async (id) => {
    try {
        const response = await fetch(`../../../products/remove_product_unit/${id}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

buttonsDownClick.forEach((buttonDown) => {
    buttonDown.addEventListener("click", async (e) => {
        let idButton = null;
        let productId = null;
        let inputQuantity = null;
        let data = null;
        let unitPrice = 0;
        if (e.target.getAttribute("id").startsWith("button-down-")) {
            idButton = e.target.getAttribute("id");
            productId = idButton.split("button-down-")[1];
            inputQuantity = document.getElementById(`input-quantity-product-${productId}`);
            if (inputQuantity.value > 1) {
                data = await removeProductUnit(productId);
                if (document.getElementById(`sale_price-${productId}`)) {
                    unitPrice = data.product.sale_price;
                } else {
                    unitPrice = data.product.price;
                }
            }
        } else if (e.target.getAttribute("id").startsWith("button-icon-down-")) {
            e.stopPropagation();
            idButton = e.target.getAttribute("id");
            productId = idButton.split("button-icon-down-")[1];
            inputQuantity = document.getElementById(`input-quantity-product-${productId}`);
            if (inputQuantity.value > 1) {
                data = await removeProductUnit(productId);
                if (document.getElementById(`sale_price-${productId}`)) {
                    unitPrice = data.product.sale_price;
                } else {
                    unitPrice = data.product.price;
                }
            }
        }
        if (inputQuantity.value != 1) {
            const totalProductPrice = document.getElementById(
                `total_product_price-${productId}`);
            totalProductPrice.innerHTML =
                `<b>$${(parseFloat(totalProductPrice.innerText.split("$")[1]) - parseFloat(unitPrice)).toFixed(2)}</b>`;
            inputQuantity.value = parseInt(inputQuantity.value) - 1;
            document.getElementById("total-quantity").innerHTML = `${data.total_quantity} artículos`;
            totalPriceAll.innerHTML = `$${(parseFloat(totalPriceAll.innerHTML.split("$")[1]) - parseFloat(unitPrice)).toFixed(2)}`;
            totalDelivery.innerHTML = `$${parseInt(totalDelivery.innerText.split("$")[1]) - 10}`;
            totalToPay.innerHTML = `<b>$${(parseFloat(totalPriceAll.innerHTML.split("$")[1]) + parseInt(totalDelivery.innerText.split("$")[1])).toFixed(2)}</b>`;
        }
    })
})

const removeProduct = async (id) => {
    try {
        const response = await fetch(`../../../products/remove_product/${id}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.log(error);
    }
}

buttonsRemoveProduct.forEach((buttonRemove) => {
    buttonRemove.addEventListener("click", async (e) => {
        const idButton = e.target.getAttribute("id");
        const productId = idButton.split("icon-trash-")[1];
        const productContainer = document.getElementById("products-container");
        const product = document.getElementById(`product-${productId}`);
        const productHr = document.getElementById(`hr-${productId}`);
        productContainer.removeChild(product);
        productContainer.removeChild(productHr);
        const data = await removeProduct(productId);
        if (data.total_quantity) {
            document.getElementById("total-quantity").innerHTML = `${data.total_quantity} artículos`;
            totalPriceAll.innerHTML = `$${data.total_price}`;
            totalDelivery.innerHTML = `$${data.total_quantity*10}`;
            totalToPay.innerHTML = `<b>$${(parseFloat(totalPriceAll.innerHTML.split("$")[1]) + parseInt(totalDelivery.innerText.split("$")[1])).toFixed(2)}</b>`;
        } else {
            document.getElementById("main").removeChild(document.querySelectorAll(".cart-container")[0]);
            document.getElementById("main").removeChild(document.querySelectorAll(".cart-container__info")[0]);
            let h2 = document.createElement("h2")
            h2.innerHTML = "No hay artículos en el carrito.";
            document.getElementById("main").appendChild(h2);
        }
    })
})