const w_quantity = document.querySelector('#quick_weight_eu');
const new_w_quantity = document.querySelector('#quick_weight_us');
const v_quantity = document.querySelector('#quick_volume_eu');
const new_v_quantity = document.querySelector('#quick_volume_us');
const quick_temperature_c = document.querySelector('#quick_temperature_c');
const quick_temperature_f = document.querySelector('#quick_temperature_f');
const w_unit = document.querySelector('#unit_weight_eu');
const new_w_unit = document.querySelector('#unit_weight_us');
const v_unit = document.querySelector('#unit_volume_eu');
const new_v_unit = document.querySelector('#unit_volume_us');


for (let element_weight of [w_quantity, w_unit, new_w_unit]) {
    element_weight.addEventListener('change', () => {
        let w_quantity_string = w_quantity.value;
        if (w_quantity_string == "") {
            new_w_quantity.innerHTML = "";
        } else {
            fetch('/quick_convert', {
                method: 'POST',
                body: JSON.stringify({ 'quantity': w_quantity.value, 'unit': w_unit.value, 'new_unit': new_w_unit.value }),
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then((response) => response.json())
                .then((responseJson) => {
                    const new_quantity = responseJson['new_quantity'];
                    new_w_quantity.innerHTML = parseFloat(new_quantity).toFixed(2);
                });
        }

    });
}
for (let element_volume of [v_quantity, v_unit, new_v_unit]) {
    element_volume.addEventListener('change', () => {
        let v_quantity_string = v_quantity.value;
        if (v_quantity_string == "") {
            new_v_quantity.innerHTML = "";
        } else {
            fetch('/quick_convert', {
                method: 'POST',
                body: JSON.stringify({ 'quantity': v_quantity.value, 'unit': v_unit.value, 'new_unit': new_v_unit.value }),
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then((response) => response.json())
                .then((responseJson) => {
                    const new_quantity = responseJson['new_quantity'];
                    new_v_quantity.innerHTML = parseFloat(new_quantity).toFixed(2);
                });
        }

    });
}
quick_temperature_c.addEventListener("change", () => {

    let celsius_string = quick_temperature_c.value;
    if (celsius_string == "") {
        quick_temperature_f.value = "";
    } else {
        quick_temperature_f.value = ((parseFloat(celsius_string) * 1.8) + 32).toFixed(0);
    }
});
quick_temperature_f.addEventListener('change', () => {
    let fahrenheit_string = quick_temperature_f.value;
    if (fahrenheit_string == "") {
        quick_temperature_c.value = "";
    } else {
        quick_temperature_c.value = ((parseFloat(fahrenheit_string) - 32) / 1.8).toFixed(0);
    }


});


