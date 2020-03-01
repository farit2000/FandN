import {update_header} from '/shop/static/js/common.js';


const generalTotalPrice = $('#generalTotalPrice');
const orderLink = $('#order');
let isNegativeQuantity = false;

$('title').append(' - Корзина');
chageOrderButton();

// Ко всем input'ам с name=quantity записать текущее значение и добавить событие
// изменения
// Ко всем товарам добавить событие удаления
$(document).ready(function () {
    const inputs = $(":input[name='quantity']");
    inputs.each(i => inputs.eq(i).data('oldVal', inputs.eq(i).val()));
    inputs.bind('change', trackQuntityInput);
    inputs.bind('change', function (e) {
        fnDelay(recountPrices.bind(this, e), 500);
    });
    let commodities = $("div[id='commodity']");
    commodities.find('i').bind('click', function (e) {
        fnDelay(removeCommodity.bind(this, e), 500);
    });
});

function updateVal(jobject, obj) {
    // Предыдущее значение
    let prevVal = parseInt(jobject.text());
    // Сложить obj с предыдущим значением и записать его
    jobject.text(prevVal + parseInt(obj));
    chageOrderButton();
}

function chageOrderButton() {
     if (parseInt(generalTotalPrice.text()) <= 0 || orderLink.hasClass('disabled')) {
        orderLink.toggleClass('disabled');
    }
}

function trackQuntityInput(e) {
    let target = $(e.target);
    if (target.val() < 1) {
        isNegativeQuantity = true;
        target.val(target.data('oldVal'));
    }
}

function recountPrices(e) {
    let info = getAllData(e);
    if (!isNegativeQuantity) {
        // Разница между прошлым числом и текущим
        let delta = info.quantity - parseInt(info.target.data('oldVal'));
        // В качестве прошлого значения поставить текущее
        info.target.data('oldVal', info.quantity);
        // Что послать во view
        const toSend = {product_id: info.id, delta: delta, action: 1, option_ids: info.optionIds};
        // Обновить все на бэке
        $.post('/basket/', toSend, function () {
            let itemTotalPrice = info.commodity.find('#itemTotalPrice');
            update_header();
            // Слагаемое
            let summand = delta * info.price;
            // Обновить общую и текущего товара суммы
            updateVal(generalTotalPrice, summand);
            updateVal(itemTotalPrice, summand);
        });
    }
    isNegativeQuantity = false;
}

function removeCommodity(e) {
    let info = getAllData(e);
    // Удалить блок
    info.commodity.remove();
    // Вычесть его общую
    let summand = -info.quantity * info.price;
    // Обновить общую сумму
    updateVal(generalTotalPrice, summand);
    // Обновить все на бэке
    $.post('/basket/', {product_id: info.id, action: 0, option_ids: info.optionIds}, update_header);
}

let fnDelay = (function() {
    let timer = 0;
    return function(callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

function getAllData(e) {
    let target = $(e.target);
    let commodity = target.parents('#commodity');
    let price = parseInt(commodity.data('price'));
    let id = commodity.data('id');
    let quantity = parseInt(commodity.find("input[name='quantity']").val());
    let optionIds = JSON.parse(commodity.find("ul[data-opt_ids]").attr('data-opt_ids'));
    return {target: target, commodity: commodity, price: price, id: id, quantity: quantity, optionIds: optionIds};
}