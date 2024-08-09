from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, CompanyTemp
from .services import CompanyService, S3Service
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json


def index(request):
    return render(request, 'general/base.html')


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'general/login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required
def create_company(request):
    user = request.user
    company_temp = CompanyService.get_or_create_temp_company(user)

    if request.method == 'POST':
        company_data = {field.name: request.POST.get(field.name) for field in Company._meta.fields}
        if 'file_logo' in request.POST:
            company_data['logo'] = request.POST['file_logo']

        company, errors = CompanyService.create_company(user, company_data)
        if errors:
            return render(
                request,
                'general/create_company.html',
                {'company': company, 'errors': errors, 'company_temp': company_temp},
            )
        return redirect('list_company')

    return render(request, 'general/create_company.html', {'company_temp': company_temp})


@login_required
@require_http_methods(['PUT'])
def edit_temp_company(request):
    user = request.user
    company_temp = get_object_or_404(CompanyTemp, user=user)
    data = json.loads(request.body)

    response = CompanyService.update_temp_company(company_temp, data)
    return JsonResponse(response)


@login_required
def list_company(request):
    companies = Company.objects.all()
    return render(request, 'general/list_company.html', {'companies': companies})


@login_required
def upload_logo(request):
    user = request.user
    company_temp = get_object_or_404(CompanyTemp, user=user)

    if request.method == 'POST' and request.FILES.get('logo'):
        file = request.FILES['logo']
        file_logo = S3Service.upload_logo(file)
        setattr(company_temp, 'logo', file_logo)
        company_temp.save()

        return JsonResponse({'file_logo': file_logo})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_logo(request):
    user = request.user
    company_temp = get_object_or_404(CompanyTemp, user=user)

    if request.method == 'POST':
        file_logo = request.POST.get('file_logo')
        if file_logo:
            try:
                S3Service.delete_logo(file_logo)
                setattr(company_temp, 'logo', '')
                company_temp.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
