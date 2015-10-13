$(function() {
    $( "#selectable" ).selectable({
        stop: function() {
            var result = $( "#id_cols" ).empty();
            text = '0'
            $( ".ui-selected", this ).each(function() {
                var index = $( this ).attr('id');
                text = text + "," + index;
                $( "#id_cols" ).val(text);
            });
        },
        create: function() {
            $( "#id_cols" ).val("");
        }
    });
});

