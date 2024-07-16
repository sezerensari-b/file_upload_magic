document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("#logo")

    fileInput.addEventListener('change', function () {
        const allowedExtensions = [
            '.jpg', 
            '.jpeg', 
            '.png'
        ];
        const filePath = fileInput.value;
        const extension = filePath.split('.').pop().toLowerCase();

        if (!allowedExtensions.includes(`.${extension}`)) {
            alert('Invalid file type. Please upload a valid file.');
            fileInput.value = ''; 
        }
    });
})
