document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("#logo");
    let currentRequest = null;

    function initForm (){
        let fileLogoVal = $('#file_logo').val()
        if(fileLogoVal != ''){
            $(fileInput).hide();
            $('#upload-logo .button-text').text('Delete Logo');
            $('#upload-logo').removeClass('btn-secondary').addClass('btn-danger');
            $('#logo-filename').text(fileLogoVal.split('/').pop());
            $('#company-form button[type="submit"]').prop('disabled', false);
        } else {
            $(fileInput).show();
            $('#upload-logo .button-text').text('Upload Logo');
            $('#upload-logo').removeClass('btn-danger').addClass('btn-secondary');
            $('#logo-filename').text(''); 
        }
    }

    initForm();

    fileInput.addEventListener('change', function () {
        const allowedExtensions = [
            '.jpg', 
            '.jpeg', 
            '.png',
            '.avi'
        ];
        const filePath = fileInput.value;
        const extension = filePath.split('.').pop().toLowerCase();

        if (!allowedExtensions.includes(`.${extension}`)) {
            alert('Invalid file type. Please upload a valid file.');
            fileInput.value = ''; 
        }

        if(currentRequest){
            currentRequest.abort();
            $('#upload-result').html('<div class="alert alert-danger">Logo upload interrupted. Please try again.</div>');
            setLoading('error')
        }

    });

    $('#upload-logo').click(function() {
        var logoFile = $('#logo')[0].files[0];
        let fileLogo = $('#file_logo').val();

        if (!fileLogo) {
            var formData = new FormData();
            formData.append('logo', logoFile);
            formData.append('csrfmiddlewaretoken', $('input[name="csrfmiddlewaretoken"]').val())

            setLoading('start')

            currentRequest = $.ajax({
                url: '/logo-upload/',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    $('#file_logo').val(response.file_logo);
                    setLoading('complete')
                    initForm();
                },
                error: function(xhr) {
                    setLoading('error')
                }
            });
        } else {
            fileToDelete = $('#file_logo').val()
            $('#logo').val('');
            deleteLogoFromView()
           $.ajax({
                url: '/logo-delete/',
                type: 'POST',
                data: {
                    'file_logo': fileToDelete,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success(response){
                    initForm();
                },
                error: function(xhr) {
                    console.log("delete error")
                }
            });
        }
    });
    
    $('#company-form').submit(function(event) {
        if (!$('#file_logo').val()) {
            event.preventDefault();
            $('#upload-result').html('<div class="alert alert-danger">Please upload the logo first.</div>');
        }
    });


    function setLoading(activater){
        if (activater == 'start'){
            $('#upload-logo .spinner-border').removeClass('d-none');
            $('#upload-logo .button-text').text('Uploading...');
            $('#upload-logo').attr('disabled', true);
        }
        else if(activater == 'complete'){
            $('#upload-result').html('<div class="alert alert-success">Logo uploaded successfully!</div>');
            $('#upload-logo .spinner-border').addClass('d-none');
            $('#upload-logo').attr('disabled', false);
            currentRequest = null;
        }
        else if (activater == 'error'){
            $('#upload-logo .spinner-border').addClass('d-none');
            $('#upload-logo').attr('disabled', false);
            currentRequest = null;
            $('#upload-logo .button-text').text('Upload Logo');
        }
    }

    function deleteLogoFromView(){
        $('#file_logo').val('');
        $('#upload-logo').removeClass('btn-danger').addClass('btn-secondary');
        $('#upload-logo .button-text').text('Upload Logo');
        $('#upload-result').html('');
        $('#company-form button[type="submit"]').prop('disabled', true);
    }
});
