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
                        alertify.error("Error creating post!");
                        break;
                    case 'title_fail': //success
                        alertify.error("Post is missing a title!");
                        break;
                    case 'content_fail': //success
                        alertify.error("Post is missing a body!");
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
                        alertify.error("Error uploading file, please make sure you are upload a valid image!");
                        break;
                    case '1': //success
                        alertify.success("Image successfully added to the Homepage Slider!");
                        break;
                    case '2': //order not a number
                        alertify.error("Order submitted is not a number!");
                        break;

                }
            },
        });
    });
});
