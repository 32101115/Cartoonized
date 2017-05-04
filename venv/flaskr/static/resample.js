var imagedata; 

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#img').attr('src', e.target.result)
                .width(500)
                .height(500);
            imagedata = e.target.result;

        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(function() {
  $('#readyImg').bind('click', function() {
    $.getJSON('/get_img', {
          imgdata: imagedata ,
          }, function(data) {
              if (data.result != null) {
                alert("The image is ready");

              }
          });
          return false;    
    });
});

$(function() {
  $('#toonify').bind('click', function() {
    var $btn = $(this);
    $btn.button('loading');

    $.getJSON('/toonify', {
          }, function(data) {
              if (data.result != null) {
                alert(data.result);
                $btn.button('reset');
                document.getElementById("btn3").disabled = false;
              }
          });
          return false;    
    });
});

$(function() {
  $('#display').bind('click', function() {
    $.getJSON('/display.html', {
          }, function(data) {
          });
		var loadUrl = "http://127.0.0.1:5000/display.html";

    	var ajax_load = "<img src='{{url_for('static', filename='output.png')}}' alt='toonified Image'/>";
        $("#img").html(ajax_load).load(loadUrl);
        window.open("display.html");

        return false;    

    });
});