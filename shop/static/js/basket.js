import {update_header} from '/shop/static/js/common.js';


const generalTotalPrice = $('#generalTotalPrice');

function is_basket_empty() {
    if(parseInt(generalTotalPrice.text()) > 0){
        location.href = '/order/';
    }
    else {
        return false;
    }
}

function updateVal(jobject, obj) {
    // Предыдущее значение
    let prevVal = parseInt(jobject.text());
    // Сложить obj с предыдущим значением и записать его
    jobject.text(prevVal + parseInt(obj));
}

// Ко всем input'ам с name=qty записать текущее значение
$(document).ready(function () {
    const inputs = $(":input[name='qty']");
    inputs.each(i => inputs.eq(i).data('oldVal', inputs.eq(i).val()));
});

function recountPrices(block, target, id, quantity, price) {
    console.log('recount');
    // Разница между прошлым числом и текущим
    let delta = quantity - parseInt(target.data('oldVal'));
    // В качестве прошлого значения поставить текущее
    target.data('oldVal', quantity);
    // Что послать во view
    const toSend = {product_id: id, delta: delta, action: 1};
    // Обновить все на бэке
    $.post('/basket/', toSend, function () {
        let itemTotalPrice = block.find('#itemTotalPrice');
        update_header();
        console.log('recount');
        // Слагаемое
        let summand = delta * price;
        // Обновить общую и текущего товара суммы
        updateVal(generalTotalPrice, summand);
        updateVal(itemTotalPrice, summand);
    });
}

function removeBlock(block, target, id, quantity, price) {
    // Удалить блок
    block.remove();
    // Вычесть его общую
    let summand = -quantity * price;
    // Обновить общую сумму
    updateVal(generalTotalPrice, summand);
    // Обновить все на бэке
    $.post('/basket/', { product_id: id, action: 0}, update_header);
}

let fnDelay = (function() {
    let timer = 0;
    return function(callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

function blockHandler(e) {
    // Получаем все данные о товаре
    let target = $(e.target);
    let block = target.parents('#block');
    let price = parseInt(block.find('input[name="price"]').val());
    let quantity = parseInt(target.val());
    let id = block.find('input[name="id"]').val();
    // Если изменился input
    if (target.attr('name') === 'qty' && e.type === 'change') {
        console.log('if recount');
        recountPrices(block, target, id, quantity, price);
    }
    // Если кликнули по корзине
    else if (target.attr('id') === 'trash' && e.type === 'click') {
        removeBlock(block, target, id, quantity, price);
    }
}

// $('#block').bind('change click', function (e) {
//     fnDelay(blockHandler.bind(this, e), 200);
//     // Получаем все данные о товаре
//     console.log(e);
//     // let block = $(e.currentTarget);
//     // let target = $(e.target);
//     // let price = parseInt(block.find('input[name="price"]').val());
//     // let quantity = parseInt(block.find('input[name="qty"]').val());
//     // let id = block.find('input[name="id"]').val();
//     // // Если изменился input
//     // if (target.attr('name') === 'qty' && e.type === 'change') {
//     //     console.log('if recount');
//     //     recountPrices(block, target, id, quantity, price);
//     // }
//     // // Если кликнули по корзине
//     // else if (target.attr('id') === 'trash' && e.type === 'click') {
//     //     removeBlock(block, target, id, quantity, price);
//     // }
// });
// console.log($('#block #trash'));
// console.log($('#block input[name="qty"]'));
let blocks = $('#block');
console.log(blocks);
console.log($('#block').find('#trash'));
console.log($('#block').find('input[name="qty"]'));
blocks.find('#trash').bind('click',function (e) {
    console.log(e);
    fnDelay(blockHandler.bind(this, e), 500);
});

blocks.find('input[name="qty"]').bind('change',function (e) {
     console.log(e);
    fnDelay(blockHandler.bind(this, e), 500);
});
