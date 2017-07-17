/**
 * Created by maciej on 12.07.17.
 */
$(document).ready(function () {
    $('.btn-info').on('click', function () {
        $(this).parent().parent().parent().find('.answer').show();
        $(this).parent().parent().find('[hidden]').show();
        $(this).parent().parent().find('[hidden]').show();
        $(this).hide();
    });
    $('')
});
