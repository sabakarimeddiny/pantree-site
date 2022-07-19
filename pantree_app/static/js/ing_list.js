$(document).ready(function() {

    $('button[id=ing_button]').click(function () {
		var toAdd=$('input[id=ingForm_ingredients]').val();
		$('<div class="removable-list-item">'+toAdd+'</div>').appendTo('.list[id=ing]');
        $('input[id=ingForm_ingredients]').val('');
    });

    $('button[id=must_have_button]').click(function () {
		var toAdd=$('input[id=ingForm_must_have_ings]').val();
		$('<div class="removable-list-item">'+toAdd+'</div>').appendTo('.list[id=must_have]');
        $('input[id=ingForm_must_have_ings]').val('');
    });

    var timeout = false;
    $("input, .sidebar, button").on({
        mouseenter: function () {
            $('.sidebar').animate({left:'0%'}, 1000); 
        },
        mouseleave: function () {
            timeout = setTimeout( function() { 
                $('.sidebar').animate({left:'-19%'}, 1000);
            }, 2000);
        },
        mouseover: function (){
            clearTimeout(timeout)
            $('.sidebar').animate({left:'0%'}, 1000); 
        }
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
        if(e.which == 13) {
            $('button[id=ing_button]').click();
        }
    });

    $('input[id=ingForm_must_have_ings], select').bind('keyup', function(e) {
        if(e.which == 13) {
            $('button[id=must_have_button]').click();
        }
    });
});

$(document).on('click','.removable-list-item',function(){ $(this).remove(); });