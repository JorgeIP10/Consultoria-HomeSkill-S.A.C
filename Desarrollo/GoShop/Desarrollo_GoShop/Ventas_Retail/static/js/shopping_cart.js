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
                `<b>S/. ${parseFloat(productPrice * productQuantity).toFixed(2)}</b>`;
                total += parseFloat(productPrice * productQuantity);
                break;
            }
        }
    })
    totalPriceAll.innerHTML = `S/. ${total.toFixed(2)}`;
    totalDelivery.innerHTML = `S/. ${parseInt(totalProductQuantity * 10)}`;
    totalToPay.innerHTML = `<b>S/. ${(totalProductQuantity * 10 + total).toFixed(2)}</b>`;
})

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
        let idButton = null;
        let productId = null;
        let inputQuantity = null;
        let data = null;
        let unitPrice = 0;
        if (e.target.getAttribute("id").startsWith("button-up-")) {
            idButton = e.target.getAttribute("id");
            productId = idButton.split("button-up-")[1];
            data = await addProduct(productId);
            inputQuantity = document.getElementById(`input-quantity-product-${productId}`);
            if (document.getElementById(`sale_price-${productId}`)) {
                unitPrice = data.product.product[0].sale_price;
            } else {
                unitPrice = data.product.product[0].price;
            }
        } else if (e.target.getAttribute("id").startsWith("button-icon-up-")) {
            e.stopPropagation();
            idButton = e.target.getAttribute("id");
            productId = idButton.split("button-icon-up-")[1];
            data = await addProduct(productId);
            inputQuantity = document.getElementById(`input-quantity-product-${productId}`);
            if (document.getElementById(`sale_price-${productId}`)) {
                unitPrice = data.product.product[0].sale_price;
            } else {
                unitPrice = data.product.product[0].price;
            }
        }
        const totalProductPrice = document.getElementById(`total_product_price-${productId}`);
        totalProductPrice.innerHTML =
            `<b>S/. ${(parseFloat(totalProductPrice.innerText.split("S/. ")[1]) + parseFloat(unitPrice)).toFixed(2)}</b>`;

        inputQuantity.value = parseInt(inputQuantity.value) + 1;
        document.getElementById("total-quantity").innerHTML = `${parseInt(data.total_quantity)} artículos`;
        totalPriceAll.innerHTML = `S/. ${(parseFloat(unitPrice) + parseFloat(totalPriceAll.innerHTML.split("S/. ")[1])).toFixed(2)}`;
        totalDelivery.innerHTML = `S/. ${parseInt(totalDelivery.innerText.split("S/. ")[1]) + 10}`;
        totalToPay.innerHTML = `<b>S/. ${(parseFloat(totalPriceAll.innerHTML.split("S/. ")[1]) + parseInt(totalDelivery.innerText.split("S/. ")[1])).toFixed(2)}</b>`;
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
                    // unitPrice = document.getElementById(`sale_price-${productId}`).innerHTML;
                    unitPrice = data.product.product[0].sale_price;
                } else {
                    // unitPrice = document.getElementById(`price-${productId}`).innerHTML;
                    unitPrice = data.product.product[0].price;
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
                    // unitPrice = document.getElementById(`sale_price-${productId}`).innerHTML;
                    unitPrice = data.product.product[0].sale_price;
                } else {
                    // unitPrice = document.getElementById(`price-${productId}`).innerHTML;
                    unitPrice = data.product.product[0].price;
                }
            }
        }
        if (inputQuantity.value != 1) {
            const totalProductPrice = document.getElementById(
                `total_product_price-${productId}`);
            totalProductPrice.innerHTML =
                `<b>S/. ${(parseFloat(totalProductPrice.innerText.split("S/. ")[1]) - parseFloat(unitPrice)).toFixed(2)}</b>`;
            inputQuantity.value = parseInt(inputQuantity.value) - 1;
            // totalProductQuantity -= 1;
            document.getElementById("total-quantity").innerHTML = `${data.total_quantity} artículos`;
            totalPriceAll.innerHTML = `S/. ${(parseFloat(totalPriceAll.innerHTML.split("S/. ")[1]) - parseFloat(unitPrice)).toFixed(2)}`;
            totalDelivery.innerHTML = `S/. ${parseInt(totalDelivery.innerText.split("S/. ")[1]) - 10}`;
            totalToPay.innerHTML = `<b>S/. ${(parseFloat(totalPriceAll.innerHTML.split("S/. ")[1]) + parseInt(totalDelivery.innerText.split("S/. ")[1])).toFixed(2)}</b>`;
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
        document.getElementById("total-quantity").innerHTML = `${data.total_quantity} artículos`;
        totalPriceAll.innerHTML = `S/. ${data.total_price}`;
        totalDelivery.innerHTML = `S/. ${data.total_quantity*10}`;
        totalToPay.innerHTML = `<b>S/. ${(parseFloat(totalPriceAll.innerHTML.split("S/. ")[1]) + parseInt(totalDelivery.innerText.split("S/. ")[1])).toFixed(2)}</b>`;
    })
})