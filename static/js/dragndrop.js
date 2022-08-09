// $(document).ready( function () {
//     $('.list[id=ing], .list[id=must_have]').droppable({
//         // tolerance: 'fit'
//         tolerance: "intersect",
//         drop: function (event, ui) {
//             var ob = ui.draggable;
//             $(this).append(ob.css({position: 'static'}));
//             // ob.css({position: 'relative'});
//         }
//     });
// });

$(document).ready( function () {
    $('.list[id=ing], .list[id=must_have]').droppable({
        tolerance: "intersect",
        drop: function (event, ui) {
            var ob = ui.draggable;
            ob.css({position: 'static'})
            var targetList = $(this)
            var added = false;
            $(".removable-list-item", targetList).each(function(){
                if ($(this).text() > $(ob).text()) {
                    $(ob).insertBefore($(this)).fadeIn("fast");
                    added = true;
                    return false;
                }
            });
            if(!added) $(ob).appendTo($(targetList)).fadeIn("fast");
        }
    });
});

$(document).on('mouseup', '.removable-list-item', function() {
    $(this).css({position: 'static'})
});