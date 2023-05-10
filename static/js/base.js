const searchForm = document.querySelector('#search-form')
const searchIcon= document.querySelector('.search-button')

searchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const input_ingredient = document.querySelector('#ingredientInput')
    window.location.href = `/search?ingredient_name=${input_ingredient.value}`;
});

searchIcon.addEventListener('click', (event) => {
    event.preventDefault();
    const input_ingredient = document.querySelector('#ingredientInput')
    window.location.href = `/search?ingredient_name=${input_ingredient.value}`;
});

