function ajax_form_submit(form_id, options={}) {

    let confirmation = options['confirmation'] || null;
    let success_result_alert = options['success_result_alert'] || true;
    let reload_after_submit = options['reload_after_submit'] || false;
    let success_callback = options['success_callback'] || function(){};

    $(form_id).submit(function (e) {
        e.preventDefault();

        if(confirmation !== null) {
            if (!confirm(confirmation)) {
                return;
            }
        }

        let form = $(this);
        let url = form.attr('action');

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {
                if(success_result_alert) {
                    alert(data['detail']);
                }
                if(reload_after_submit) {
                    location.reload();
                }
                success_callback();
            },
            error: function( jqXhr, textStatus, errorThrown ){
                console.log(errorThrown);
                alert("Some error occurred.");
                if(reload_after_submit) {
                    location.reload();
                }
            }
        });
    });
}
$(document).ajaxSend(function () {
    $('#ajaxLoad').addClass('show');
});

$(document).ajaxComplete(function () {
    $('#ajaxLoad').removeClass('show');
});
