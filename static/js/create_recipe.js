const addIngredient = document.querySelector('#add_ingredient');
const ingredientList = document.querySelector('#ingredient_list');

addIngredient.addEventListener('click', () => {
    fetch('/get_all_units')
        .then((response) => response.json())
        .then((responseData) => {
            let all_units = responseData['all_units'];
            let unitList = '<div> quantity <input type="text" id="quantity" value=" " size="8"> unit <select id="unit">';
            for (let unit of all_units) {
                unitList += '<option value=' + unit + '>' + unit + '</option>'

            }
            unitList += '</select>name <input type="text" id="name" value=" " size="8"></div>';
            ingredientList.insertAdjacentHTML('beforeend', unitList);
        });
});

const saveButton = document.querySelector('#save');
saveButton.addEventListener('click', () => {
    
    formInputs = []
    for (let child of ingredientList.children){
        let quantity = child.querySelector('#quantity').value; 
        let unit = child.querySelector('#unit').value;
        let name = child.querySelector('#name').value;
        formInputs.push({'quantity':quantity, 'unit':unit, 'name':name});

    }
    fetch('/save', {
        method: 'POST',
        body: JSON.stringify({'ingredients':formInputs}),
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((response) => response.json())
        .then((responseJson) => {
            alert(responseJson.status);
        });
});