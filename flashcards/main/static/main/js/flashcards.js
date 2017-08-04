/**
 * Created by maciej on 26.07.17.
 */
$(document).ready(function () {
    $('.special-letter-btn').on('click', function (event) {
       event.preventDefault();
       var btn = $(this);
       var input = btn.closest('.input').find('input').eq(0);
       var caretPosStart = input.prop('selectionStart');
       var caretPosEnd = input.prop('selectionEnd');
       var inputValue = input.val();
       input.val(inputValue.substring(0, caretPosStart) + btn.text() + inputValue.substring(caretPosEnd));
    });
});