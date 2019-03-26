$(document).ready(function(){

    $('.var-del-btn').on('click',function(e){
        e.preventDefault()
        id = $(this).attr('data-id')
        name = $(this).attr('data-name')
        delet = confirm("Do you really wish to delete "+name)
        if ( delet == true ){
            $.get( "/variables/"+id+"/delete", function( data ) {
                $('#var-'+id).remove()
            });
        }
    });

    $('.del-obj-btn').on('click',function(e){
        e.preventDefault()
        form_id = $(this).attr('data-target')
        form = $('#'+form_id)
        console.log(form)
        form.trigger( "submit" );        
        
    });

    $('.config-server').on('click',function(e){
        e.preventDefault()
        let s_id = $(this).attr('data-server-id')
        $('input[name="serverID"]').val(s_id)

    });

    $('.start-server').on('click', function(){
        let serverid=$('input[name="serverID"]').val()
        var csrf_token = $('#start_server_csrf').val();

        

        $.post("/start_server/"+serverid,
        {
            server : serverid,
            plc_ip : $('#input-ip').val()
        },
        function(data){
            console.log(data);
            $.each(data, function(key, value){
                // $('#alert-box').removeClass('d-none').addClass('alert-'+key)
                // $('#server-response').text(value)
                $('#msgs').html('<div id="alert-box" class="alert alert-'+key+' alert-dismissible">\
                  <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                  <span id="server-response">'+value+'</span>\
               </div>')
            
            });
            
        });
    });


    
    $('.stop-server').on('click', function(){
        // let serverid=$(this).attr('data-server-id')
        let serverid=$('input[name="serverID"]').val()
        $.get("stop_server/"+serverid, function(data){
            console.log(data)   
            $.each(data, function(key, value){
                $('#msgs').html('<div id="alert-box" class="alert alert-'+key+' alert-dismissible">\
                  <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>\
                  <span id="server-response">'+value+'</span>\
               </div>')            
            });
        });
    });

    $('.edit-server-btn').on('click',function(e){ 
        id = $(this).attr('data-serverid')
        name = $(this).attr('data-name')
        namespace = $(this).attr('data-namespace')
        epurl = $(this).attr('data-epurl')
        form = $('#projects_form').attr('action','server/'+id+'/edit')
        $('[name="server_name"]').val(name);
        $('[name="endpoint_url"]').val(epurl);
        $('[name="namespace"]').val(namespace);
    })

});
