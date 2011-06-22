/* Adds CSRF token to AJAX POST requests done with JQuery.
 * From https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
 */
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

/* Signup form
 */

function validEmail(string) {
    // refine this regex for basic email validation
    // use DNS-check or similar method for validation
    var checkEmail = /[\w-.]+@[\w-.]+\.\w{2,8}/;
    return checkEmail.test(string);
}

$(function () {     // when the DOM is ready
    $('.error').hide();     // hide notifications

    $('#submit_button').click(function (e) {
        e.preventDefault();

        // validate and process form
        var email = $('input#email').val();
        if (validEmail(email)) {
            // make sure the error is hidden
            $("label#email_error").hide();
        } else {
            // nope
            $("label#email_error").show();
            $("input#email").focus();
            return false;   // don't submit the form
        }

        // submit form
        var dataString = 'email=' + email;
        $.ajax({
            type:'POST',
            url:'signup',
            data: dataString,
            success: function (data) {
                $('#signup_form').html("<div id='message'></div>");
                $('#message').html(data).hide().fadeIn(1500, function () {} );
            }
        });
        return false;
    });
});

