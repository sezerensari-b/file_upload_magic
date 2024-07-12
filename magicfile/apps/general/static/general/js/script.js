const fileInput = document.querySelector("#file_input")

fileInput.addEventListener('change', function () {
    const allowedExtensions = [
        '.jpg', 
        '.jpeg', 
        '.png', 
        '.gif', 
        '.pdf', 
        '.mp3', 
        '.mp4', 
        '.wav'];
    const filePath = fileInput.value;
    const extension = filePath.split('.').pop().toLowerCase();

    if (!allowedExtensions.includes(`.${extension}`)) {
        alert('Invalid file type. Please upload a valid file.');
        fileInput.value = ''; 
    }
});