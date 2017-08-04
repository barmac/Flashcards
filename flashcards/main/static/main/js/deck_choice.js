$(document).ready(function () {
    $('#btn-add').on('click', function (event) {
       event.preventDefault();
       $('#form').removeClass('hidden');
       $(this).addClass('hidden');
    });
});