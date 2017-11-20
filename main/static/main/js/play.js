/**
 * Created by maciej on 12.07.17.
 */
$(document).ready(function () {
    $('.btn-info').on('click', function () {
        $('#answer').removeClass('hidden');
        $('#grade').removeClass('hidden');
        $(this).addClass('hidden');
    });
});
