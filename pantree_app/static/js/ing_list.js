$(document).ready(function() {

    // $('button[id=add_button]').click(function () {
	// 	var toAdd=$('input[id=ingForm_ingredients]').val();
	// 	$('<div class="removable-list-item"><i class="fas fa-ellipsis-v"></i><i class="fas fa-ellipsis-v"></i>&nbsp'+toAdd+'&nbsp<i class="fa-solid fa-xmark"></i></div>').draggable({ 
    //         revert: 'invalid',
    //         helper: 'clone',
    //         refreshPositions: true,
    //         opacity: 0.5,
    //     }).appendTo('.list[id=ing]');
    //     $('input[id=ingForm_ingredients]').val('');
    // });

    $('button[id=add_button]').click(function () {
        var added = false;
		var toAdd=$('input[id=ingForm_ingredients]').val();
        var targetList=$('.list[id=ing]');
		var ing = $('<div class="removable-list-item"><i class="fas fa-ellipsis-v"></i><i class="fas fa-ellipsis-v"></i>&nbsp'+toAdd+'&nbsp<i class="fa-solid fa-xmark"></i></div>').draggable({ 
            revert: 'invalid',
            helper: 'clone',
            refreshPositions: true,
            opacity: 0.5,
        })
        $(".removable-list-item", targetList).each(function(){
            if ($(this).text() > $(ing).text()) {
                $(ing).insertBefore($(this)).fadeIn("fast");
                added = true;
                return false;
            }
        });
        if(!added) $(ing).appendTo($(targetList)).fadeIn("fast");
        $('input[id=ingForm_ingredients]').val('');
    });

    $('button[id=require_button]').click(function () {
		var added = false;
		var toAdd=$('input[id=ingForm_ingredients]').val();
        var targetList=$('.list[id=must_have]');
		var ing = $('<div class="removable-list-item"><i class="fas fa-ellipsis-v"></i><i class="fas fa-ellipsis-v"></i>&nbsp'+toAdd+'&nbsp<i class="fa-solid fa-xmark"></i></div>').draggable({ 
            revert: 'invalid',
            helper: 'clone',
            refreshPositions: true,
            opacity: 0.5,
        })
        $(".removable-list-item", targetList).each(function(){
            if ($(this).text() > $(ing).text()) {
                $(ing).insertBefore($(this)).fadeIn("fast");
                added = true;
                return false;
            }
        });
        if(!added) $(ing).appendTo($(targetList)).fadeIn("fast");
        $('input[id=ingForm_ingredients]').val('');
    });

    $('button[id=clear]').click(function () {
        $('.list[id=ing] .removable-list-item').remove();
        $('.list[id=must_have] .removable-list-item').remove();
    });

    var timeout = false;
    $("form").on("submit", function () {
        var textInput = $('.list[id=ing] .removable-list-item').map(function() {
            return $(this).text();
        }).get().join(', ');
        $('input[id=ingForm_ingredients]').val(textInput);

        var textInput = $('.list[id=must_have] .removable-list-item').map(function() {
            return $(this).text();
        }).get().join(', ');
        $('input[id=ingForm_must_have_ings]').val(textInput);
    });

    $('input[id=ingForm_ingredients], select').bind('keyup', function(e) {
        if(e.which == 13 && !e.shiftKey) {
            $('button[id=add_button]').click();
        }
    });

    $('input[id=ingForm_ingredients], select').bind('keyup', function(e) {
        if(e.which == 13 && e.shiftKey) {
            $('button[id=require_button]').click();
        }
    });

    var array = $('input[id=ings]').val().split(',');
    $.each(array,function(i) {
        // alert(array[i]);
        $('input[id=ingForm_ingredients]').val(array[i]);
        $('button[id=add_button]').click();
     });
    
     $(".ingredient").click(function(){
        var element = $(this);
        var added = false;
        var targetList = $(this).parent().siblings(".ingredientList")[0];
        $(this).fadeOut("fast", function() {
            $(".ingredient", targetList).each(function(){
                if ($(this).text() > $(element).text()) {
                    $(element).insertBefore($(this)).fadeIn("fast");
                    added = true;
                    return false;
                }
            });
            if(!added) $(element).appendTo($(targetList)).fadeIn("fast");
        });
    });
});

// $(document).on('click','.removable-list-item',function(){ $(this).remove(); });
$(document).on('click','.fa-solid.fa-xmark',function(){ $(this).parent().remove(); });
