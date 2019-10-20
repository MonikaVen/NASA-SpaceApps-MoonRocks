

document.querySelector('#upload-file').addEventListener( 'click', () => {
    console.log('upload clicked!')
    document.querySelector('#message').innerHTML = '';
    document.querySelector('body').style.backgroundImage = "url('https://www.nasa.gov/sites/default/files/thumbnails/image/astronauts_lunar_craterv2.png')";
})

$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                document.querySelector('#result').innerHTML = data['result'];
                document.querySelector('#message').innerHTML = data['message'];
                if(data['collect']){
                    document.querySelector('body').style.backgroundImage = "url('https://i.ibb.co/2cQkSms/bkg2.png')";
                    console.log('collect!')
                }
                // let percent_data = Array.from(document.querySelectorAll('#result'));
                // percent_data.forEach(el => {
                // })
                // $('#result').text(' Result:  \n' + data);
                console.log('Success!');
            },
        });
    });

});
