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

removeButton=document.querySelector('#remove');

removeButton.addEventListener('click', () => {
    const recipe_id = document.querySelector('#recipe_id_hidden').value;
    const url = `/remove?recipe_id=${recipe_id}`;
  
    fetch(url)
      .then((response) => response.text())
      .then((status) => {
        alert(status);
        window.location.href='/user_dashboard';
      });
  });
