/*$(document).ready(function(){
    $('.check:button').toggle(function(){
        $('input:checkbox').attr('checked','checked');
        $(this).val('uncheck all')
    },function(){
        $('input:checkbox').removeAttr('checked');
        $(this).val('check all');        
    })
})*/


$(document).ready(function(){
	$('#selectall').click(
		function(){
			$('input:checkbox').prop('checked',true);
		}
	);
});


$(document).ready(function(){
    $('#deselectall').click(
        function(){
            $('input:checkbox').prop('checked', false);
        }
    );
});


