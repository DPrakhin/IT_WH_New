$(document).ready(() => {

    $('#choose_item').on('click', '.add-to-cart-btn', (event) => {
            if($(event.target).prev().val() == "") {
                alert('Заповніть поле типу')
            } else {
                console.log('add-btn -> Click')
                const userId = $('#user-id').val();
                console.log('User-ID: ' + userId)

                if (userId == 'None') {
                     alert('For using cart you should be authorized!!!')
                } else {
                    let ItemId = $(event.target).prev().val()
                    console.log('Item-ID: ' + ItemId)

                    let EmplId = $(event.target).prev().prev().val()
                    console.log('employee-ID: ' + EmplId)

                    $.ajax({
                        url: '/storage/cart',
                        data: `uid=${userId}&itid=${ItemId}&empid=${EmplId}`,
                        success: (response) => {
                            console.log(response);
                            $('.number').text(response.count);
                        }
                    });
                    $(event.target).prev().val("")
                }
            }

    });
});