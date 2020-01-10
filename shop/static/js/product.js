export function change_button_to_basket() {
    $('.btn').replaceWith(`<a href="/basket/">
                           <button type="button" class="btn btn-outline-secondary">Перейти в корзину</button>
                           </a>`);
}

$('.img-choice').first().addClass('active');
const activeImage = $('.img-fluid');
$('.img-choices-container').mouseover(function (e) {
    let target = $(e.target);
    if (target.hasClass('img-choice')){
        $('.active').removeClass('active');
        target.addClass('active');
        activeImage.attr('src', target.attr('src'))
    }
});