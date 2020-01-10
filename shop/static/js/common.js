export function update_header() {
    $.get(window.location.pathname, function (data) {
        $('.dropdown').replaceWith($(data).find('.dropdown')[0]);
    });
}