const addIngredient = document.querySelector('#add_ingredient');
const ingredientList = document.querySelector('#ingredient_list');
const addParagraph = document.querySelector('#add_paragraph');
const paragraphList = document.querySelector('#paragraph_list');

addIngredient.addEventListener('click', () => {
    fetch('/get_all_units')
        .then((response) => response.json())
        .then((responseData) => {
            let all_units = responseData['all_units'];
            let new_div = document.createElement("div");
            new_div.innerHTML = `
                qty <input type="number" id="quantity" value="">
                unit <select id="unit">
                    ${all_units.map(unit => `<option value="${unit}">${unit}</option>`).join('')}
                </select>
                name <input type="text" id="name" value="">
                <button class="remove-ingredient"><i class="fas fa-times"></i></button>
            `;
            new_div.classList.add("ingredient");
            new_div.querySelector(".remove-ingredient").addEventListener('click', (event) => {
                event.target.closest('.ingredient').remove();

            });
            ingredientList.appendChild(new_div);
        });
});

addParagraph.addEventListener('click', () => {
    let new_div = document.createElement("div");
    new_div.innerHTML = `
                <textarea rows="3" id="text"></textarea>
                <button class="remove-paragraph"><i class="fas fa-times"></i></button>
            `;
    new_div.classList.add("paragraph");
    new_div.querySelector(".remove-paragraph").addEventListener('click', (event) => {
        event.target.closest('.paragraph').remove();
    });
    paragraphList.appendChild(new_div);

});

const upload_form = document.querySelector('#upload_form');

upload_form.addEventListener('submit', (event) => {
    event.preventDefault();

    formInputs = []
    paragraphTexts = []
    for (let child of ingredientList.children) {
        let quantity = child.querySelector('#quantity').value;
        let unit = child.querySelector('#unit').value;
        let name = child.querySelector('#name').value;
        formInputs.push({ 'quantity': quantity, 'unit': unit, 'name': name });
    }
    for (let child of paragraphList.children) {
        let text = child.querySelector('#text').value;
        paragraphTexts.push(text);
    }
    let title = document.querySelector('#title').value;
    let recipe_id = document.querySelector('#recipe_id_hidden').value;
    let file_input = document.querySelector("#file_input")
    fetch('/save', {
        method: 'POST',
        body: JSON.stringify({ 'ingredients': formInputs, 'title': title, 'paragraphs': paragraphTexts, 'recipe_id': recipe_id, 'file_input': file_input.value }),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
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

const removeParagraphButtons = document.querySelectorAll('.remove-paragraph');
removeParagraphButtons.forEach(button => {
    button.addEventListener('click', () => {
        button.parentElement.remove();
    });
});
