const addIngredient = document.querySelector('#add_ingredient');
const ingredientList = document.querySelector('#ingredient_list');

addIngredient.addEventListener('click', () => {
    fetch('/get_all_units')
        .then((response) => response.json())
        .then((responseData) => {
            let all_units = responseData['all_units'];
            let unitList = '<div> quantity <input type="text" id="quantity" value="" size="8"> unit <select id="unit">';
            for (let unit of all_units) {
                unitList += '<option value=' + unit + '>' + unit + '</option>'

            }
            unitList += '</select> name <input type="text" id="name" value="" size="60"></div>';
            ingredientList.insertAdjacentHTML('beforeend', unitList);
        });
});

const upload_form = document.querySelector('#upload_form');

upload_form.addEventListener('submit', (event) => {
    event.preventDefault();

    formInputs = []
    for (let child of ingredientList.children) {
        let quantity = child.querySelector('#quantity').value;
        let unit = child.querySelector('#unit').value;
        let name = child.querySelector('#name').value;
        formInputs.push({ 'quantity': quantity, 'unit': unit, 'name': name });
    }
    let title = document.querySelector('#title').value;
    let description = document.querySelector('#description').value;
    let recipe_id = document.querySelector('#recipe_id_hidden').value;
    fetch('/save', {
        method: 'POST',
        body: JSON.stringify({ 'ingredients': formInputs, 'title': title, 'description': description, 'recipe_id': recipe_id }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            let file_input = document.querySelector("#file_input")
            if (!file_input.value) {
                // keep existing image
                window.location.href = '/user_dashboard';
            } else {
                // new image uploaded
                const new_file_path = responseJson['new_file_path'];
                const formData = new FormData(upload_form);
                formData.append('new_file_path', new_file_path);
                fetch('/uploader', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => {
                        fetch('/rename', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ 'new_file_path': new_file_path })
                        })
                            .then(response => {
                                if (response.status === 200) {
                                    window.location.href = '/user_dashboard';
                                } else {
                                    console.log('Error submitting data');
                                }
                            })
                            .catch(error => {
                                console.log('Network error', error);
                            });
                    })
                    .catch(error => {
                        console.error('Error occured:', error);
                    });
            }

        });
});
const removeButtons = document.querySelectorAll('.remove-ingredient');
removeButtons.forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.remove();
    });
});