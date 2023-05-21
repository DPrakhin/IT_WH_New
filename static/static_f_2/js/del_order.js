$(document).ready(() => {

    console.log('Start del order')

    $('.del-btn').click(event => {

        let ItemId = $(event.target).next().val();

        $.ajax({
            url: '/storage/item_delete',
            data: `ItemId=${ItemId}`,
            success: (response) => {
                alert(response.result)
                window.location = '/storage/cart/view'
            }
        })
    })
})