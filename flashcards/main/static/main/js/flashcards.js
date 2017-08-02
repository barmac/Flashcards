/**
 * Created by maciej on 26.07.17.
 */
$(document).ready(function () {
    $('.edit-btn').on('click', function (event) {
        var button = $(this);
        var form = $('#form');
        var id = button.data('id');
        var question = button.parent().parent().find('.question').text();
        var answer = button.parent().parent().find('.answer').text();
        form.attr('action', '/flashcard/edit/' + id + '/');
        form.find('[name="question"]').val(question);
        form.find('[name="answer"]').val(answer);
        $('#submit').text('Edytuj fiszkę');
    });
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