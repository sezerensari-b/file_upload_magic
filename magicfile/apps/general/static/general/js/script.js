document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("#logo")

    fileInput.addEventListener('input', () => {
        let fileLogo =  $('#file_logo').val();
        if(fileLogo) {
            $.ajax({
                url: '/logo-delete/',
                type: 'POST',
                data: {
                    'file_logo': $('#file_logo').val(),
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    if (response.success) {
                        $('#file_logo').val('');
                        $('#upload-result').html('<div class="alert alert-danger">Logo deleted successfully!</div>');
                        $('#upload-logo').text('Upload Logo').removeClass('btn-danger').addClass('btn-secondary');
                        $('#company-form button[type="submit"]').prop('disabled', true);
                    } else {
                        $('#upload-result').html('<div class="alert alert-danger">Error deleting logo.</div>');
                    }
                },
                error: function(xhr) {
                    $('#upload-result').html('<div class="alert alert-warning">Error deleting logo.</div>');
                    $('#company-form button[type="submit"]').prop('disabled', true);
                }
            });
        }
    })

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
    });

    $('#upload-logo').click(function() {
        var logoFile = $('#logo')[0].files[0];
        let fileLogo =  $('#file_logo').val();
    
        if (!fileLogo) {
            var formData = new FormData();
            formData.append('logo', logoFile);
    
            $.ajax({
                url: '/logo-upload/',
                type: 'POST',
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    $('#file_logo').val(response.file_logo);
                    $('#upload-result').html('<div class="alert alert-success">Logo uploaded successfully!</div>');
                    $('#upload-logo').text('Delete Logo').removeClass('btn-secondary').addClass('btn-danger');
                    $('#company-form button[type="submit"]').prop('disabled', false);
                },
                error: function(xhr) {
                    $('#upload-result').html('<div class="alert alert-danger">Error uploading logo.</div>');
                    $('#company-form button[type="submit"]').prop('disabled', true);
                }
            });
        } else {
            $.ajax({
                url: '/logo-delete/',
                type: 'POST',
                data: {
                    'file_logo': $('#file_logo').val(),
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    if (response.success) {
                        $('#file_logo').val('');
                        $('#logo').val('');
                        $('#upload-result').html('<div class="alert alert-danger">Logo deleted successfully!</div>');
                        $('#upload-logo').text('Upload Logo').removeClass('btn-danger').addClass('btn-secondary');
                        $('#company-form button[type="submit"]').prop('disabled', true);
                    } else {
                        $('#upload-result').html('<div class="alert alert-danger">Error deleting logo.</div>');
                    }
                },
                error: function(xhr) {
                    $('#upload-result').html('<div class="alert alert-warning">Error deleting logo.</div>');
                    $('#company-form button[type="submit"]').prop('disabled', true);
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

});