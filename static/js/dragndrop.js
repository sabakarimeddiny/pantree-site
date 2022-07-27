$(document).ready( function () {
    $('.list[id=ing], .list[id=must_have]').droppable({
        // tolerance: 'fit'
        tolerance: "intersect",
        drop: function (event, ui) {
            var ob = ui.draggable;
            $(this).append(ob.css({position: 'static'}));
            // ob.css({position: 'relative'});
        }
    });
});

$(document).on('mouseup', '.removable-list-item', function() {
    $(this).css({position: 'static'})
});