/**
 * Created with PyCharm.
 * User: yac
 * Date: 9/18/15
 * Time: 1:14 PM
 * To change this template use File | Settings | File Templates.
 */

$("#signup").validate({
    rules:{
        username: {
            required: true,
            minlength: 3
        },
        password:{
            required:true,
            minlength: 5
        },
        password_confirm:{
            required:true,
            equalTo: "#password"
        }
    },
    submitHandler: function(form) {
        var formData = $( "input" ).serialize();
        var request = $.ajax({
            url: "/signup",
            type: "post",
            data: formData
        });

        request.done(function (response, textStatus, jqXHR){
            var $sign = $("#signup");
            var $inputs = $sign.find("input");
            var $pass = $sign.find('input[type=password]');

            if (response.success == true){
                alert('Well done!');
                window.location.replace("/");
            }
            else {
                $('#text_error').text(response.errorMessage);
            }
        })
    }

});