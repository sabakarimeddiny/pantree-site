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

$(document).on('mouseover', '.removable-list-item', function() {
    $(this).draggable({ 
        revert: 'invalid',
        helper: 'clone',
        refreshPositions: true,
        opacity: 0.5,
    });
});

$(document).on('mouseup', '.removable-list-item', function() {
    $(this).css({position: 'static'})
});