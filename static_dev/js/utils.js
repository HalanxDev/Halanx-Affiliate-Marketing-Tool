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
