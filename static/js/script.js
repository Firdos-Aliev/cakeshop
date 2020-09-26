"use strict"

window.onload = function(){
    console.log("Все подгружено");
    let basketList = $('.basket-list');

    basketList.on('click', '.basketadd', function (event) {
        $.ajax({ //передаем словарь аргуметов (json)
            url: '/basket/product/' + event.target.dataset.pk + '/add/' + event.target.dataset.count + '/ajax/',
            success: function (data) {
            console.log(data) // чтобы понять что страница не обновляется
                basketList.html(data.basket_list);
            },
        });
    })

    basketList.on('click', '.basketpop', function (event) {
        $.ajax({ //передаем словарь аргуметов (json)
            url: '/basket/product/' + event.target.dataset.pk + '/pop/' + event.target.dataset.count + '/ajax/',
            success: function (data) {
            console.log(data) // чтобы понять что страница не обновляется
                basketList.html(data.basket_list);
            },
        });
    })
}



