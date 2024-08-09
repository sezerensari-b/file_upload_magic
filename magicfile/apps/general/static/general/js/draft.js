document.addEventListener("DOMContentLoaded", () => {
    const companyForm = document.getElementById('company-form');
    const fileLogo = document.getElementById('file_logo')

    companyForm.addEventListener('input', function () {
        const formData = new FormData(companyForm);
        const data = {};

        formData.forEach((value, key) => {
            if(key != 'logo' && key != 'file_logo'){
                data[key] = value;
            }
        });

        data['active'] = companyForm.querySelector('[name="active"]').checked ? 'on' : '';

        $.ajax({
            url: '/temp-company-edit/',
            type: 'PUT',
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val(),
                'Content-Type': 'application/json'
            },
            data: JSON.stringify(data),
            success: function(response) {
            },
            error: function(xhr) {
            }
        });
    });
});