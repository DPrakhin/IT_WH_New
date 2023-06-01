const doCalculate = () => {
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

const doRequired = () => {
    let field_required = $('.field_required')

    for (let field of field_required) {
        if ($(field).text().length > 0){
            $(field).prev().hide()
        } else {
            $(field).prev().show()
        }
    }
}

const doSaveCheckbox = () => {
    let checkedBoxes = $('.check')
    for (let box of checkedBoxes) {
        let parentRow = $(box).parent().parent()
        findcode = $(parentRow).find('td.id_empl_cell').find('input').val()
        box.setAttribute("name", findcode)
    }

    // Avoid scoping issues by encapsulating code inside anonymous function
    (function() {
      // variable to store our current state
      var cbstate;

      // bind to the onload event
      window.addEventListener('load', function() {
        // Get the current state from localstorage
        // State is stored as a JSON string
        cbstate = JSON.parse(localStorage['CBState'] || '{}');

        // Loop through state array and restore checked
        // state for matching elements
        for(var i in cbstate) {
          var el = document.querySelector('input[name="' + i + '"]');
          if (el) el.checked = true;
        }

        // Get all checkboxes that you want to monitor state for
        var cb = document.getElementsByClassName('save-cb-state');

        // Loop through results and ...
        for(var i = 0; i < cb.length; i++) {

          //bind click event handler
          cb[i].addEventListener('click', function(evt) {
            // If checkboxe is checked then save to state
            if (this.checked) {
              cbstate[this.name] = true;
            }

        // Else remove from state
            else if (cbstate[this.name]) {
              delete cbstate[this.name];
            }

        // Persist state
            localStorage.CBState = JSON.stringify(cbstate);
          });
        }
      });
    })();

}


$(document).ready(() => {
    doSaveCheckbox()
    doRequired()

    window.onload = (event) =>{
        doCalculate()
    };

    $('.check').click((event) => {
        doCalculate()
    })

})