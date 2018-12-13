$(document).ready(function() {
    //new post
    $('#newPostBody').summernote({
        height: 150,
        callbacks: {
            onKeyup: function(e) {
                $('#postBodyPreview').html(filterXSS($(this).summernote('code')));
            }
        }
    });

    $('#newPostTitle').keyup(function(e) {
        $('#postTitlePreview').text($(this).val());
    });

    $('#newPostImage').change(function(event) {
        $("#postImagePreview").fadeOut('slow', function() {
            $(this).fadeIn('slow').attr('src', URL.createObjectURL(event.target.files[0]));
        })
    });

    $('#addNewPost').on('click', function() {
        var data = new FormData($('#postForm')[0]);

        data.append('title', $('#newPostTitle').val());
        //data.append('image', $('#newPostImage')[0].files[0]);
        data.append('safe_content', filterXSS($('#newPostBody').summernote('code')));

        $.ajax({
            url: '/admin/api/posts/new',
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                switch (response) {
                    case 'admin_fail': //fail
                        alertify.error("Error creating post");
                        break;
                    case 'title_fail': //success
                        alertify.error("Post is missing a title");
                        break;
                    case 'content_fail': //success
                        alertify.error("Post is missing a body");
                        break;
                    default:
                        window.location.href = "/post/" + response; //send user to the new post
                }
            }
        });
    });

    //new slider
    $('#newSliderImage').change(function(event) {
        $("#sliderPreview").fadeOut('slow', function() {
            $(this).fadeIn('slow').attr('src', URL.createObjectURL(event.target.files[0]));
        })
    });

    $('#addNewSlider').on('click', function() {
        var data = new FormData($('#sliderForm')[0]);

        $.ajax({
            url: '/admin/api/sliders/new',
            type: 'POST',
            data: data,
            cache: false,
            processData: false,
            contentType: false,
            success: function(response) {
                switch (response) {
                    case '0': //fail
                        alertify.error("Error uploading file, please make sure you are upload a valid image");
                        break;
                    case '1': //success
                        alertify.success("Image successfully added to the homepage slider");
                        break;
                    case '2': //order not a number
                        alertify.error("Order submitted is not a number");
                        break;

                }
            },
        });
    });

    //edit post
    $('.modifyPost').on('click', function() {
        let id = $(this).attr("post");

        $.post('/admin/api/posts/grab', {'post_id': id}, function(response) {
            if (response !== '0') {
                let js = $.parseJSON(response);

                let post_id = js["id"];
                let title = js["title"];
                let content = js["content"];
                let path = js["image_path"];

                $('#modifyPostPane').fadeOut('slow', function() {
                    $("#editPostTitle").val(title);

                    $('#editPostBody').summernote({
                        height: 150,
                        callbacks: {
                            onKeyup: function(e) {
                                $('#postBodyPreview').html(filterXSS($(this).summernote('code')));
                            }
                        }
                    });

                    $('#editPostBody').summernote('code', content);

                    $('#postTitlePreview').text(title);
                    $("#postImagePreview").attr('src', path);
                    $('#submitModifyPost').attr('post', post_id);

                    $(this).fadeIn('slow');
                    $('#editPostExtra').fadeIn('slow');
                });

            }

        })
    });

    $('.deletePost').on('click', function() {
        let post_id = $(this).attr('post');

        alertify.confirm("Delete Post?", "Are you sure you want to delete this post?", function() {
           $.post('/admin/api/posts/delete', {'post_id': post_id}, function(response) {
               switch(response) {
                    case 'admin_fail': //fail
                        alertify.error("Error removing post");
                        break;
                    default:
                        alertify.success("Post successfully removed");
                        window.location.reload();
                        break;
                }
           })
        }, function() { })
    });

    $(document).on('click', '.deleteSlider', function() {
        let slider_id = $(this).attr('slider');

        alertify.confirm("Delete Slider Image?", "Are you sure you want to delete this image?", function() {
           $.post('/admin/api/sliders/delete', {'slider_id': slider_id}, function(response) {
               switch(response) {
                    case 'admin_fail': //fail
                        alertify.error("Error removing image");
                        break;
                    default:
                        alertify.success("Image successfully removed");
                        window.location.reload();
                        break;
                }
           })
        }, function() { })
    });

    $('#submitModifyPost').on('click', function() {
        let post_id = $(this).attr('post');
        let title = $('#editPostTitle').val();
        let content = filterXSS($('#editPostBody').summernote('code'));

        $.post('/admin/api/posts/modify', {
            'post_id': post_id,
            'title': title,
            'content': content}, function(response) {
            switch(response) {
                case 'admin_fail': //fail
                    alertify.error("Error modifying post");
                    break;
                case 'title_fail': //fail
                    alertify.error("Post is missing a title");
                    break;
                case 'content_fail': //fail
                    alertify.error("Post is missing a body");
                    break;
                default:
                    alertify.success("Post successfully modified");
                    window.location.reload();
                    break;
            }
        });
    });

    $('#completeRegistration').on('click', function() {
        $.post('/authenticate', {
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
                    //window.location.reload();
                    alertify.success("User successfully created!");
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
