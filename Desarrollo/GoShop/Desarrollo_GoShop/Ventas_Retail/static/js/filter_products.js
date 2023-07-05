const minPriceInput = document.getElementById('min-price');
const maxPriceInput = document.getElementById('max-price');
const minPriceValue = document.getElementById('min-price-value');
const maxPriceValue = document.getElementById('max-price-value');
// const filterButton = document.getElementById('filter-button');

function filterProducts() {
    const minPrice = parseFloat(minPriceInput.value);
    const maxPrice = parseFloat(maxPriceInput.value);
    minPriceValue.textContent = `$${minPrice}`;
    maxPriceValue.textContent = `$${maxPrice}`;
}

minPriceInput.addEventListener('input', filterProducts);
maxPriceInput.addEventListener('input', filterProducts);

document.getElementById("filter-form").addEventListener("submit", (e) => {
    if (parseFloat(minPriceInput.value) > parseFloat(maxPriceInput.value)) {
        console.log("aea");
        e.preventDefault();
    }
})