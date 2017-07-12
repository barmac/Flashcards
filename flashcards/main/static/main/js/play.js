/**
 * Created by maciej on 12.07.17.
 */
$(document).ready(function () {
    $('.btn').on('click', function () {
        $(this).parent().find('.answer').show();
    });
});