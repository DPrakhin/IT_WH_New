$(document).ready(() => {

    console.log('cart-display.js -> start')
    const user_id = $('#user-id').val();

    $.ajax({
        url: "/storage/cart_display",
        data: `uid=${user_id}`,
        success: (response) => {
            $('.number').text(response.count);
            $('.number_wait').text(response.count_wait);
        }
    })

})