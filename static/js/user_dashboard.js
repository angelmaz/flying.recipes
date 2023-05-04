const hearths_full = document.querySelectorAll('.full_hearth');

for (const hearth_full of hearths_full) {
    hearth_full.addEventListener("click", (event) => {
        const hearth_id = hearth_full.getAttribute('id')
        const recipe_id = hearth_id.split('_')[2]
        fetch(`/remove_favorite_recipe?recipe_id=${recipe_id}`)
            .then((response) => response.json())
            .then((responseJson) => {
                const status = responseJson['status'];

                if (status) {
                    event.target.style = 'display:none';
                    event.target.parentNode.style = 'display:none';
                } else {
                    alert("cannot remove recipe from favorites");
                }

            });
    })
}

const takeRecipe = document.querySelector('#link_button')
const linkWeb = document.querySelector('#link_web_scrapping')

takeRecipe.addEventListener('click', () => {
    fetch(`/web_scrapping?url=${linkWeb.value}`)
        .then((response) => response.json())
        .then((responseJson) => {
            const status = responseJson['status'];
            if (status) {
                alert("recipe succesfully added to your list");
                location.reload()
            } else {
                alert("cannot fetch the recipe");
            }
        })
})