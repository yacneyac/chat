/**
 * Created with PyCharm.
 * User: yac
 * Date: 9/18/15
 * Time: 8:48 AM
 * To change this template use File | Settings | File Templates.
 */

$('#user_online').click(function(evnt){
    if (evnt.target.selectedIndex != 0){
        var text = 'to '+evnt.target.value +': ';
        $('#text_message').val(text);
    }
});

$("#login").click(function(event){

    var formData = $( "input" ).serialize();
    var request = $.ajax({
        url: "/login",
        type: "post",
        data: formData
    });

    request.done(function (response){
        if (response.success == true){
            // TODO update only header. don't touch chat :)
            window.location.replace("/chat");
            $('#text_message').focus();
        }
        else{
            $('#text_error').text(response.errorMessage);
        }
    });
    request.fail(function (jqXHR, textStatus, errorThrown){
        console.error("The following error occured: " + textStatus, errorThrown);
    });

    // prevent default posting of form
    event.preventDefault();
});

function mainChat(is_authenticated, username){
    var socket = null;
    var billboard = $('#billboard');
    var scrollHeight = 25;
    var maxFileSize = 1048576; // 1Mb
    var message = $("#text_message");

    socket = io.connect("/chat");

    $('#text_message').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
            if (is_authenticated=='True'){
                sendMessage();}
            }
            event.stopPropagation();
        });

    $('#send_message').click(function(event){
        sendMessage();
        return false;
    });

    // join to the chat. if not username its spectators
    socket.emit('join', username);

    // disconnect
    $(window).on('beforeunload',function(){
        if (is_authenticated=='True')
            socket.disconnect();

        });

    //receive messages and update html
    socket.on('receive msg', function(nick, message){
        var text = '[' + dateTime() +'] '+ nick +' says: '+ message;

        billboard.append('<br/>' + text);
        billboard.scrollTop(billboard.scrollTop() + scrollHeight);

        return false;
    });

    //user connected
    socket.on('user connected', function(nick, users){

        $('#user_count').text('User online: '+ users.length);

        if (is_authenticated=='True'){

            $('#user_online option:gt(0)').remove();  // remove old options
            var $el = $("#user_online");

            $.each(users, function(index, value) {
                if (value != username ){
                    $el.append($("<option></option>").attr("value", value).text(value));
                }
            });
        }

        if (nick){
            var nickAux = '<span style=\'font-weight:bold; color: red;\'>' + nick + '</span>';
            var text = '[' + dateTime() +'] ' + nickAux+ ' joined the chat';

            $('<div class="alert alert-success">').html(text).appendTo(billboard);
            billboard.scrollTop(billboard.scrollTop() + scrollHeight);
        }
            return false;
        });

    //user disconnected
    socket.on('user disconnected', function(nick){
        var nickAux = '<span style=\'font-weight:bold; color:red;\'>' + nick + '</span>';
        var text = '[' + dateTime() +'] ' + nickAux + ' has left the chat';

        $('<div class="alert alert-warning">').html(text).appendTo('#billboard');
        billboard.scrollTop(billboard.scrollTop() + scrollHeight);

        return false;
    });

    //get file
    socket.on('user file', function(nick, msg){
        var warMsg = '';
        if (is_authenticated!='True'){
            warMsg = ' Only authorized user have permission to view file.'
        }

        var text = '[' + dateTime() +'] ' + nick + ' send ' +msg['imageName'] + warMsg;
        $('<div class="alert alert-warning">').html(text).appendTo('#billboard');

        if (is_authenticated=='True')
            $('<img src=' +msg['imageData']+  ' height="200" width="200" alt=""/>').appendTo('#billboard');

            billboard.scrollTop(billboard.scrollTop() + scrollHeight);

            return false;

        });

    // read file and send
    $('#imageFile').on('change', function(e){
        var file = e.originalEvent.target.files[0];
        var fileType = file.type.split('/')[0];
        var fileSize = file.size;
        var err = $('#file_error');

        err.text('');
        $("#imageFile" ).val("");

        if (fileType != 'image'){
            err.text('Only image file can be loaded');
            return
        }

        if (fileSize > maxFileSize){
            err.text('Max file size: 1M');
            return
        }

        var reader = new FileReader();
        reader.onload = function(evt){
            var jsonObject = {
                'imageData': evt.target.result,
                'imageName': file.name
            };

            // send a custom socket message to server
            socket.emit('file', jsonObject);
        };
        reader.readAsDataURL(file);
    });

    function sendMessage(){
        var msg = $.trim(message.val());
        if (msg)
            socket.emit('says', msg);
        message.val('');
    }

    function dateTime(){
        var options = {
            year: 'numeric', month: 'numeric', day: 'numeric',
            hour: 'numeric', minute: 'numeric', second: 'numeric',
            hour12: false
        };
        var date = new Date();
        return date.toLocaleString('UA', options)
    }
}
