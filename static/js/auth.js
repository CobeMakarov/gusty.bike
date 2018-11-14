$(document).ready(function() {

    $('#carouselImage').carousel({});

    $('#showRegister').on('click', function(){
        $("#login-layout").fadeOut(1000, function() {
            $('#register-layout').fadeIn(1000);
        })
    });

    $('#showLogin').on('click', function(){
        $("#register-layout").fadeOut(1000, function() {
            $('#login-layout').fadeIn(1000);
        })
    });

    $('#completeLogin').on('click', function() {
        $.post('authenticate', {'username': $("#loginUsername").val(), 'password': $("#loginPassword").val(), 'type': 'l'}, function(response) {
            switch (response) {
                case '0': //fail
                    alertify.error("The username and password do not match.");
                    break;
                case '1': //success
                    window.location.reload();
                    break;
                case '2': //field blank
                    alertify.error("You left something blank.");
                    break;
            }
        })
    });

    $('#completeRegistration').on('click', function() {
        $.post('authenticate', {
            'username': $("#registerUsername").val(),
            'email': $("#registerEmail").val(),
            'password': $("#registerPassword").val(),
            'password2': $("#registerPassword2").val(),
            'type': 'r'}, function(response) {
            switch (response) {
                case '0': //fail
                    alertify.error("A user with that username already exists!");
                    break;
                case '1': //success
                    window.location.reload();
                    break;
                case '2': //field blank
                    alertify.error("You left something blank.");
                    break;
                case '3': //email not formatted correctly
                    alertify.error("Your e-mail is not formatted correctly");
                    break;
                case '4': //passwords don't match
                    alertify.error("Passwords do not match");
                    break;
                case '5': //password not long enough
                    alertify.error("Passwords need to be a minimum of six characters.");
                    break;
                case '6': //username not formatted correctly
                    alertify.error("Your username is not formatted correctly");
                    break;
            }
            console.log(response);
        })
    });
});