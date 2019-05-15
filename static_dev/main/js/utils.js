function remove_select_option_duplicates() {
    $('select').each(function () {
        let finishItems = {};
        $(this).find('option').each(function () {
            if (finishItems[this.text]) {
                $(this).remove();
            } else {
                finishItems[this.text] = this.value;
            }
        });
    });
}

String.prototype.format = function () {
    let a = this;
    for (let k in arguments) {
        a = a.replace(new RegExp("\\{" + k + "\\}", 'g'), arguments[k]);
    }
    return a;
};

$('.visibility_toggle').click(function () {
    let ele = $($(this).attr('data-container-id').split(',').map(x => '#' + x).join());
    ele.toggle();
    if ($(this).prop('tagName') === 'I') {
        ele.trigger('isVisible');
        if ($(this).attr('class').includes('plus')) {
            $(this).attr('class', 'fa fa-minus-circle visibility_toggle');
        } else {
            $(this).attr('class', 'fa fa-plus-circle visibility_toggle');
        }
    }
});
