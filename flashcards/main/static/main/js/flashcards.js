/**
 * Created by maciej on 26.07.17.
 */
$(document).ready(function () {
    $('.edit-btn').on('click', function (event) {
        event.preventDefault();
        var id = $(this).data('id');
        var form = $('#form');
        var button = $(this);
        var question = button.parent().parent().find('.question').text();
        var answer = button.parent().parent().find('.answer').text();
        form.attr('action', '/flashcard/edit/' + id + '/');
        form.find('[name="question"]').prop('value', question)
        form.find('[name="answer"]').prop('value', answer)
        $('#submit').text('Edytuj fiszkę');
    });
});