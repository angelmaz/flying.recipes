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
        hearth_empty.style = 'display:block';
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
        hearth_full.style = 'display:block';
    })
}

$(document).ready(function() {
    var interval = 5000; // 5 seconds
    var currentIndex = 0;
    var photos = [
      'static/img/photo_recipes/5.jpeg',
      'static/img/photo_recipes/4.jpeg',
      'static/img/photo_recipes/8.jpeg'
    ];
    
    // Set initial active item
    $('.slider-item').eq(0).addClass('active');
    
    setInterval(function() {
      // Fade out current active item
      $('.slider-item.active').animate({opacity: 0}, 1000, function() {
        $(this).removeClass('active');
      });
      
      // Set next item as active
      currentIndex = (currentIndex + 1) % photos.length;
      $('.slider-item').eq(currentIndex).animate({opacity: 1}, 1000).addClass('active');
    }, interval);
  });
