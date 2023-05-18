$(document).ready(function () {
    var interval = 5000; // 5 seconds
    var currentIndex = 0;
    var photos = [
        'static/img/karuzela1.png',
        'static/img/karuzela2.png',
        'static/img/karuzela3.png',
        'static/img/karuzela4.png',
        'static/img/kanapka1.png',
    ];

    // Set initial active item
    $('.slider-item').eq(0).addClass('active');

    setInterval(function () {
        // Fade out current active item
        $('.slider-item.active').animate({ opacity: 0 }, 1000, function () {
            $(this).removeClass('active');
        });

        // Set next item as active
        currentIndex = (currentIndex + 1) % photos.length;
        $('.slider-item').eq(currentIndex).animate({ opacity: 1 }, 1000).addClass('active');
    }, interval);
});


const hearts_full = document.querySelectorAll('.full_heart');

for (const heart_full of hearts_full) {
    heart_full.addEventListener("click", (event) => {
        const heart_id = heart_full.getAttribute('id')
        const recipe_id = heart_id.split('_')[2]
        fetch(`/remove_favorite_recipe?recipe_id=${recipe_id}`)
            .then((response) => response.json())
            .then((responseJson) => {
                const status = responseJson['status'];
                if (!status) {
                    alert("cannot remove recipe from favorites");
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
        fetch(`/favorite_recipe?recipe_id=${recipe_id}`)
            .then((response) => response.json())
            .then((responseJson) => {
                const status = responseJson['status'];
                if (!status) {
                    alert("cannot add recipe to favorites");
                }
            });
        event.target.style = 'display:none';
        const heart_full = event.target.parentNode.querySelector('.full_heart');
        heart_full.style = 'display:block';
    })
}

// const recipe_boxes = document.querySelectorAll('.recipe-box');

// for (const recipe_box of recipe_boxes) {
//     const heart_div = recipe_box.querySelector(".heart-div");
//     recipe_box.addEventListener("mouseover", (event) => {
//         heart_div.style = 'display:block'
//     });
//     recipe_box.addEventListener("mouseout", (event) => {
//         heart_div.style = 'display:none'
//     });
// }