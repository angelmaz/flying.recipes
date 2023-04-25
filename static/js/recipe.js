const scaleButton = document.querySelector('#scale_button');
const scaleContainer = document.querySelector('#scale_container');

scaleButton.addEventListener('click', () => {
    if (scaleContainer.style.display === "none") {
        scaleContainer.style.display ="block";
    } else {
        scaleContainer.style.display = "none";
    }
});

const fieldStand = document.querySelector('#field-is-cake-stand');
const fieldTin = document.querySelector('#field-is-cake-tin');
const fieldHomeStand = document.querySelector('#field-home-is-cake-stand');
const fieldHomeTin = document.querySelector('#field-home-is-cake-tin');

fieldStand.addEventListener('click', () => {
    document.querySelector('.size_cake_tin').style.display ='none';
})
fieldTin.addEventListener('click', () => {
    document.querySelector('.size_cake_tin').style.display = 'block';
})
fieldHomeStand.addEventListener('click', () => {
    document.querySelector('.size_cake_home_tin').style.display ='none';
})
fieldHomeTin.addEventListener('click', () => {
    document.querySelector('.size_cake_home_tin').style.display ='block';
});