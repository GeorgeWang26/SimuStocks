console.log("HELLO")
$(function(){
    
    var $email = $('#email-field');
    var $username = $('#username-field');
    var $password = $('#password-field');

    $("#signup").on('click', function(){
        console.log("Clicked")
        var user = {
            email: $email.val(),
            username: $username.val(),
            password: $password.val()
        };
        $ajax({
            type: 'POST',
            url: '/newUser',
            data: user,
            succuess: function(newOrder){
                console.log(user)
            },
            error: function(){
                alert('error')
            }
        })
    });
});