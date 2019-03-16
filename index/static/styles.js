$(document).ready(function(){

    $('.var-del-btn').on('click',function(e){
        e.preventDefault()
        id = $(this).attr('data-id')
        name = $(this).attr('data-name')
        $.get( "/variables/"+id+"/delete", function( data ) {
            alert( name+' '+data );
            $('#var-'+id).remove()
          });
    });


    $('.del-obj-btn').on('click',function(e){
        e.preventDefault()
        form_id = $(this).attr('data-target')
        form = $('#'+form_id)
        console.log(form)
        form.trigger( "submit" );        
        
    });
});
