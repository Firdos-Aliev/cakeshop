"use strict"

let orderCount; // общее количество товаров в заказе
let orderPrice; // обшая цена товаров в заказе
let orderForm;

let orderCountDOM, orderPriceDOM; // DOM модели
let countForms;// количество форм + extra=1

let countArr = [];// список количества каждого товара
let priceArr = [];// список цен каждого товара

function fillArr(){
    for(let i=0;i<countForms;i++){
        let count = parseInt($("#id_orderitem_set-" + i + "-quantity").val());
        let price = parseFloat($("#id_orderitem_set-" + i + "-price").val().replace(',','.'));

        countArr[i] = count;
        priceArr[i] = price;
    }
}

function updateOrder(){
    orderCount = 0;
    orderPrice = 0;
    for(let i=0;i <countForms;i++){
        orderCount +=countArr[i];
        orderPrice += countArr[i] * priceArr[i];
    }
    orderCountDOM.html(orderCount.toString());
    orderPriceDOM.html(orderPrice.toString());
}

window.onload = function(){
    console.log("Все подружено");
    orderForm = $('.order-form');
    //console.log(orderForm);

    orderCountDOM = $(".total_count");
    orderCount = parseInt(orderCountDOM.text()) || 0;
    //console.log("Общаее количество: " + orderCount);

    orderPriceDOM = $(".total_price");
    orderPrice = parseInt(orderPriceDOM.text().replace(',','.')) || 0;
    //console.log("Общаяя цена: " + orderPrice);

    countForms = $("#id_orderitem_set-TOTAL_FORMS").val();
    //console.log("Количество форм: " + countForms);


    fillArr();
    updateOrder();

    orderForm.on('change','input[type="number"]', function(event){
        let orderId = event.target.name;
        orderId = orderId.replace('orderitem_set-','');
        orderId = orderId.replace('-quantity','');

        let product_pk = $($("#id_orderitem_set-" + orderId + "-product")).val();
        let delete_obj = $($("#id_orderitem_set-" + orderId + "-DELETE"));

        if(product_pk > 0 && delete_obj[0].checked==false){ // если id продукта > 0 тоесть сущесвует тогда вносим изменения
            countArr[orderId] = parseInt(event.target.value);
            updateOrder();
        }

    });

    orderForm.on('change','input[type="checkbox"]', function(event){

        let orderId = event.target.name;
        orderId = orderId.replace('orderitem_set-','');
        orderId = orderId.replace('-DELETE','');

        let product_pk = $($("#id_orderitem_set-" + orderId + "-product")).val();
        if(product_pk>0){
            if(event.target.checked == true){
                countArr[orderId] = 0;
                updateOrder();
            }
            else{
                let order = $('#id_orderitem_set-' + orderId + '-quantity');
                countArr[orderId] = parseInt(order.val());
                updateOrder();
            }
        }
    });

    orderForm.on('change','select', function(event){
        console.log(event.target);
    });



    $('.order-list').formset({
        addText: 'добавить продукт',
        deleteText: 'удалить',
        prefix: 'orderitems',
        //removed: deleteOrder
    });

}