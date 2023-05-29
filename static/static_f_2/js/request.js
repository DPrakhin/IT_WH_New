const doCalculate = () => {
    console.log('doCalculate() -> Work')

    let checkedBoxes = $('.check:checked')
    let currentItem = ""
    let selRequestIds = ""
    selcounter = 0

    for (let box of checkedBoxes) {
        let parentRow = $(box).parent().parent()
        currentItem += $(parentRow).find('td.item_cell').text().replace(/\s/g, '') + '+'
        selRequestIds += $(parentRow).find('td.id_empl_cell').find('input').val() + ','
        selcounter += 1
    }
    selRequestIds += currentItem
    amount = selcounter

    $('.counter_items').text(amount);
    $('#moveto').attr('href', `/storage/request_check/${selRequestIds}`)

    if (amount == 0) {
        $('.checker_count').text('Щоб перейти далі виберіть як найменше один запит')
    } else {
        $('.checker_count').text('')
    }

    if (selRequestIds == /\s/g.test(selRequestIds)) {
        $('#moveto').fadeOut(0);
    } else {
        $('#moveto').fadeIn(0);
    }
}

$(document).ready(() => {

    console.log('calc_order.js -> Start!')
    doCalculate()

    $('.check').click((event) => {
        console.log('input.check -> click')
        doCalculate()
    })
})