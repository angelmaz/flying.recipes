const hearts_full = document.querySelectorAll('.full_heart');

for (const heart_full of hearts_full) {
    heart_full.addEventListener("click", (event) => {
        const heart_id = heart_full.getAttribute('id')
        const recipe_id = heart_id.split('_')[2]
        const original_recipe_id = document.querySelector('#original_recipe_id_hidden').value
        fetch(`/remove_favorite_recipe?copy_recipe_id=${recipe_id}`)
            .then((response) => response.json())
            .then((responseJson) => {
                const status = responseJson['status'];
                if (!status) {
                    alert("cannot remove recipe from favorites");
                }
                else {
                    window.location.href =  '/recipe/' + original_recipe_id;
                }
            });
        event.target.style = 'display:none';
        const heart_empty = event.target.parentNode.querySelector('.empty_heart');
        heart_empty.style = 'display:block';
    })
}
const hearts_empty = document.querySelectorAll('.empty_heart');

for (const heart_empty of hearts_empty) {
    heart_empty.addEventListener("click", (event) => {
        const heart_id = heart_empty.getAttribute('id')
        const recipe_id = heart_id.split('_')[2]
        fetch(`/favorite_recipe?copy_recipe_id=${recipe_id}`)
            .then((response) => response.json())
            .then((responseJson) => {
                const status = responseJson['status'];
                if (!status) {
                    alert("cannot add recipe to favorites");
                }
                else {
                    window.location.href = '/recipe/' + recipe_id
                }
            });
        event.target.style = 'display:none';
        const heart_full = event.target.parentNode.querySelector('.full_heart');
        heart_full.style = 'display:block';
    })
}


const scaleButton = document.querySelector('#scale_button');
const scaleContainer = document.querySelector('#scale_container');

scaleButton.addEventListener('click', () => {
    if (scaleContainer.style.display === "none") {
        scaleContainer.style.display = "block";
    } else {
        scaleContainer.style.display = "none";
    }
});

const fieldStand = document.querySelector('#field-is-cake-stand');
const fieldTin = document.querySelector('#field-is-cake-tin');
const fieldHomeStand = document.querySelector('#field-home-is-cake-stand');
const fieldHomeTin = document.querySelector('#field-home-is-cake-tin');
const measurement = document.querySelector('#measurement');
const homeMeasurement = document.querySelector('#home_measurement');


fieldStand.addEventListener('click', () => {
    document.querySelector('.size_cake_tin').style.display = 'none';
})
fieldTin.addEventListener('click', () => {
    document.querySelector('.size_cake_tin').style.display = 'block';
})
fieldHomeStand.addEventListener('click', () => {
    document.querySelector('.size_cake_home_tin').style.display = 'none';
})
fieldHomeTin.addEventListener('click', () => {
    document.querySelector('.size_cake_home_tin').style.display = 'block';
});

removeButton = document.querySelector('#remove');
if (removeButton) {
    removeButton.addEventListener('click', () => {
        const recipe_id = document.querySelector('#recipe_id_hidden').value;
        // Ask for confirmation before removing
        const confirmed = confirm("Do you want to remove?");
        if (!confirmed) {
            return; // Exit if the user cancels
        }
        const url = `/remove?recipe_id=${recipe_id}`;

        fetch(url)
            .then((response) => response.text())
            .then((status) => {
                alert(status);
                window.location.href = '/user_dashboard';
            });
    });
}
const calculByPerson = document.querySelector('#calculation_by_person');
const fromPerson = document.querySelector('#from_person');
const toPerson = document.querySelector('#to_person');

calculByPerson.addEventListener('click', () => {
    if (toPerson.value && fromPerson.value && !isNaN(toPerson.value) && !isNaN(fromPerson.value)) {
        let scale = parseFloat(toPerson.value) / parseFloat(fromPerson.value)
        for (const row of document.querySelectorAll(".ingredient_row")) {
            const quantity_span = row.querySelector(".quantity_field");
            if (quantity_span.innerHTML != "") {
                const old_value = parseFloat(quantity_span.innerHTML);
                const new_value = (old_value * scale).toFixed(2);
                quantity_span.innerHTML = new_value;
            }
        }
    }
});

const calculByPan = document.querySelector('#calculation');

calculByPan.addEventListener('click', () => {
    const size = document.querySelector('#size').value;
    const sizeY = document.querySelector('#size_y').value;
    const homeSize = document.querySelector('#home_size').value;
    const homeSizeY = document.querySelector('#home_size_y').value;

    let recipeArea, recipeHomeArea, radius, x, y, scale;

    if (fieldStand.checked == true) {
        if (!size || isNaN(size)) {
            return;
        }
        radius = parseFloat(size) / 2;
        recipeArea = Math.PI * radius * radius;
    } else {
        if (!size || !sizeY || isNaN(size) || isNaN(sizeY)) {
            return;
        }
        x = parseFloat(size);
        y = parseFloat(sizeY);
        recipeArea = x * y;
    }

    if (fieldHomeStand.checked == true) {
        if (!homeSize || isNaN(homeSize)) {
            return;
        }
        radius = parseFloat(homeSize) / 2;
        recipeHomeArea = Math.PI * radius * radius;
    } else {
        if (!homeSize || !homeSizeY || isNaN(homeSize) || isNaN(homeSizeY)) {
            return;
        }
        x = parseFloat(homeSize);
        y = parseFloat(homeSizeY);
        recipeHomeArea = x * y;
    }

    scale = recipeHomeArea / recipeArea

    if (measurement.value != homeMeasurement.value) {
        if (measurement.value == 'cm') {
            scale = scale * 2.54 * 2.54
        } else {
            scale = scale * 2.54 / 2.54
        }
    }

    for (const row of document.querySelectorAll(".ingredient_row")) {
        const quantity_span = row.querySelector(".quantity_field");
        if (quantity_span.innerHTML != "") {
            const old_value = parseFloat(quantity_span.innerHTML);
            const new_value = (old_value * scale).toFixed(2);
            quantity_span.innerHTML = new_value;
        }
    }
});

for (const row of document.querySelectorAll(".ingredient_row")) {
    const unit_span = row.querySelector(".unit_field");
    const select = unit_span.querySelector('select');
    if (select) {
        select.addEventListener('change', (event) => {
            const unitField = event.target.parentNode;
            const ingredientRow = unitField.parentNode.parentNode;
            const quantityField = ingredientRow.querySelector('.quantity_field');
            const ingredientId = ingredientRow.querySelector('.ingredient_id_field').value;
            fetch('/convert', {
                method: 'POST',
                body: JSON.stringify({ 'ingredient_id': ingredientId, 'unit': event.target.value }),
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then((response) => response.json())
                .then((responseJson) => {
                    const quantity = responseJson['quantity'];
                    quantityField.innerHTML = parseFloat(quantity).toFixed(2);
                });
        });
    }
}
