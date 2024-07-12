from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .models import MyFile


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.mp3', '.mp4', '.wav']
        ext = uploaded_file.name.split('.')[-1].lower()

        if f'.{ext}' not in valid_extensions:
            return render(request, 'general/upload.html', {'error': 'Invalid file type.'})

        my_file = MyFile(file=uploaded_file)
        my_file.save()
        return redirect('success')

    return render(request, 'general/upload.html')


def succes(request):
    return render(request, 'general/succes.html')
