function equalizeHeight(x, y) {
    var textHeight = $(x).height();
    $(y).css('min-height', textHeight);
}

$(document).ready(function () {
    // ------------------------------------------------------- //
    // Equalize height
    // ------------------------------------------------------ //
    equalizeHeight('.featured-posts .feature-1 .text', '.featured-posts .feature-1 .image');
    equalizeHeight('.featured-posts .feature-2 .text', '.featured-posts .feature-2 .image');
    equalizeHeight('.featured-posts .feature-3 .text', '.featured-posts .feature-3 .image');
    $(window).resize(function () {
        equalizeHeight('.featured-posts .feature-1 .text', '.featured-posts .feature-1 .image');
        equalizeHeight('.featured-posts .feature-2 .text', '.featured-posts .feature-2 .image');
        equalizeHeight('.featured-posts .feature-3 .text', '.featured-posts .feature-3 .image');
    });

});





