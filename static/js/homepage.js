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
                    alert("succesfully removed recipe from favorites");
                } else {
                    alert("cannot remove recipe from favorites");
                }
            });
        event.target.style = 'display:none';
        const hearth_empty = event.target.parentNode.querySelector('.empty_hearth');
        hearth_empty.style = 'dispaly:block';
    })
}
const hearths_empty = document.querySelectorAll('.empty_hearth');

for (const hearth_empty of hearths_empty) {
    hearth_empty.addEventListener("click", (event) => {
        const hearth_id = hearth_empty.getAttribute('id')
        const recipe_id = hearth_id.split('_')[2]
        fetch(`/favorite_recipe?recipe_id=${recipe_id}`)
            .then((response) => response.json())
            .then((responseJson) => {
                const status = responseJson['status'];
                if (!status) {
                    alert("cannot add recipe to favorites");
                }
            });
        event.target.style = 'display:none';
        const hearth_full = event.target.parentNode.querySelector('.full_hearth');
        hearth_full.style = 'dispaly:block';
    })
}

