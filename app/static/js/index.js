$(function() {

    function get_cart() {
        const cart = $.cookie("cart");
        if (!cart) return [];
        return JSON.parse(cart);
    }

    function add_cart(id) {
        const cart = get_cart();
        if (cart) {
            cart.push({'id': id, count: 1});
            $.cookie("cart", JSON.stringify(cart), { expires : 10 });
        } else {
            $.cookie("cart", JSON.stringify([{'id': id, count: 1}]), { expires : 10 });
        }
    }

    function update_counter_cart() {
        const count = get_cart().length;
        if (count) {
            $('#cartCount').text(count);
            $('#cartCount').show();
        } else {
            $('#cartCount').hide();
        }
    }

    function remove_cart(id) {
        const cart = get_cart();
        if (cart) {
            $.cookie("cart", JSON.stringify(
                cart.filter(function(item) {return item['id'] !== id})
            ), { expires : 10 })
        }
    }

    function clear_cart() {
        $.removeCookie('cart');
    }

    function check_cart_btn(btn, id) {
        if (get_cart().filter(function(item) {return item['id'] === id}).length) {
            btn.addClass('active');
            btn.text('-');
        } else {
            btn.removeClass('active');
            btn.text('+');
        }
    }

    $(document).on('click', '#add-to-cart:not(.active)', function() {
        const id = $(this).data('id');
        add_cart(id);
        check_cart_btn($(this), id);
        update_counter_cart();
    });

    $(document).on('click', '#add-to-cart.active', function() {
        const id = $(this).data('id');
        remove_cart(id);
        check_cart_btn($(this), id);
        update_counter_cart();
    });

    $('#add-to-cart').each(function(e){
        check_cart_btn($(this), $(this).data('id'));
    });

    update_counter_cart();

    function update_cart_view() {
        $.ajax({
            url: '/cart',
            type: 'POST',
            data: JSON.stringify({
                items: get_cart(),
                promocode: $('[name="promo"]').val(),
            }),
            success: (data) => {
                $('#cart').html(data);
            }
        });
    }

    if ($('#cart').length) {
        update_cart_view();
    }

    $(document).on('click', '#clearCart', function() {
        clear_cart();
        update_counter_cart();
        update_cart_view();
    });

    function updateCountProducts(id, action="plus") {
        let cart = get_cart();
        for (let i in cart) {
            if (cart[i].id == id) {
                if (action == "plus") cart[i].count += 1;
                else cart[i].count -= 1;
            }
        }
        $.cookie("cart", JSON.stringify(cart), { expires : 10 });
        update_cart_view();
    }

    $(document).on('click', '[data-counter-product] #mincount', function() {
        let count = parseInt($(this).parent().find('#count').text());
        const id = $(this).parent().data('counter-product');
        if (count - 1 == 0) {
            remove_cart(id);
            check_cart_btn($(this), id);
            update_cart_view();
        } else {
            updateCountProducts(id, 'minus');
        }
    });

    $(document).on('click', '[data-counter-product] #addcount', function() {
        const id = $(this).parent().data('counter-product');
        updateCountProducts(id, 'plus');
    });

    $(document).on('keyup', '#usePromo__value', function(){
        $('#promoError').hide();
    });

    $(document).on('click', '#delPromo', function() {
        $('[name="promo"]').val("");
        update_cart_view();
    });

    $(document).on('click', '#usePromo', function(){
        const code = $('#usePromo__value').val();
        if (code.length) {
            $.ajax({
                type: 'POST',
                url: '/cart',
                data: JSON.stringify({
                    'action': 'promo',
                    'code': code,
                }),
                success: (data) => {
                    if (data.success) {
                        $('[name="promo"]').val(code);
                        update_cart_view();
                    } else {
                        $('#promoError').show();
                    }
                }
            })
        }
    });

    $(document).on('click', '.cart_btn .btn', function(e) {
        e.preventDefault();
        $(this).css({'opacity': .5, 'pointer-events': 'none'});
        const name = $('[name="name"]').val();
        const phone = $('[name="phone"]').val();
        if (name.length === 0 || phone.length === 0) {
            $('#cartError').show();
        } else {
            clear_cart();
            $('#cartError').hide();
            setTimeout(() => {
                $('#cartForm').submit();
            }, 500);
        }
    });

    $(document).on('click', '[data-order-toproccess]', function() {
        const id = $(this).data('order-toproccess');
        $.ajax({
            type: 'POST',
            data: JSON.stringify({
                action: 'PROCCESS',
                id: id
            }),
            success: (data) => {
                if (data.success) {
                    $(this).parent().parent().parent().find('#status__name').text($(this).data('status-name'));
                    $(this).parent().parent().find('[data-status="new"]').hide();
                    $(this).parent().parent().find('[data-status="proccess"]').show();
                }
            }
        })
    });

    $(document).on('click', '[data-order-tocomplete]', function() {
        const id = $(this).data('order-tocomplete');
        $.ajax({
            type: 'POST',
            data: JSON.stringify({
                action: 'COMPLETE',
                id: id
            }),
            success: (data) => {
                if (data.success) {
                    $(this).parent().parent().parent().find('#status__name').text($(this).data('status-name'));
                    $(this).parent().parent().find('[data-status="new"]').hide();
                    $(this).parent().parent().find('[data-status="proccess"]').hide();
                }
            }
        })
    });

    $(document).on('click', '[data-order-tocancel]', function() {
        const id = $(this).data('order-tocancel');
        $.ajax({
            type: 'POST',
            data: JSON.stringify({
                action: 'CANCEL',
                id: id
            }),
            success: (data) => {
                if (data.success) {
                    $(this).parent().parent().parent().find('#status__name').text($(this).data('status-name'));
                    $(this).parent().parent().find('[data-status="new"]').hide();
                    $(this).parent().parent().find('[data-status="proccess"]').hide();
                }
            }
        })
    });

    $(document).on('click', '.orders__item .orders__item-header', function() {
        if ($(this).parent().hasClass('active')) {
            $(this).parent().removeClass('active');
        } else {
            $(this).parent().addClass('active');
        }
    });

});