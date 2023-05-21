const doCalculate = () => {
    console.log('doCalculate() -> Work')

    let checkedBoxes = $('.check:checked')
    let currentItem = ""
    let selRequestIds = ""

    for (let box of checkedBoxes) {
        let parentRow = $(box).parent().parent()
        currentItem += $(parentRow).find('td.item_cell').text().replace(/\s/g, '') + '+'
        selRequestIds += $(parentRow).find('td.id_empl_cell').find('input').val() + ','
    }
    selRequestIds += currentItem

    console.log(`selRequestIds: ${selRequestIds}`)

    $('#moveto').attr('href', `/storage/request_check/${selRequestIds}`)

    if (selRequestIds == /\s/g.test(selRequestIds)) {
        $('#moveto').fadeOut(1000);
    } else {
        $('#moveto').fadeIn(1000);
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