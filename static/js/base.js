const searchButton = document.querySelector('#search')

searchButton.addEventListener('click', (event) => {
    event.preventDefault();
    const input_ingredient = document.querySelector('#ingredientInput')
    window.location.href = `/search?ingredient_name=${input_ingredient.value}`;
});