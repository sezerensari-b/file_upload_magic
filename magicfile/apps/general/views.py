from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .models import Company, CompanyTemp
from django.core.exceptions import ValidationError

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import boto3
import os
import json
from datetime import datetime
from dotenv import load_dotenv

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCES_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_S3_REGION_NAME'),
)

load_dotenv()


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

    try:
        company_temp = CompanyTemp.objects.get(user=user)
    except CompanyTemp.DoesNotExist:
        company_temp = CompanyTemp.objects.create(user=user)

    if request.method == 'POST':
        company_data = {}
        for field in Company._meta.fields:
            field_name = field.name
            if field_name in request.POST:
                company_data[field_name] = request.POST[field_name]
            elif 'file_logo' in request.POST:
                company_data['logo'] = request.POST['file_logo']

        company_data['user'] = user
        company_data['active'] = company_data.get('active') == 'on'

        company = Company(**company_data)

        try:
            company.full_clean()
            company.save()
            return redirect('list_company')
        except ValidationError as e:
            print('buraya dustum')
            errors = {field: messages for field, messages in e.message_dict.items()}
            return render(
                request,
                'general/create_company.html',
                {'company': company, 'errors': errors, 'company_temp': company_temp},
            )

    return render(request, 'general/create_company.html', {'company_temp': company_temp})


@login_required
@require_http_methods(['PUT'])
def edit_temp_company(request):
    user = request.user
    company_temp = get_object_or_404(CompanyTemp, user=user)

    data = json.loads(request.body)
    for field in CompanyTemp._meta.fields:
        field_name = field.name
        if field_name in data:
            if field_name == 'active':
                setattr(company_temp, field_name, data[field_name] == 'on')
            elif field_name == 'founded_date':
                if data[field_name]:  # Check if the field is not empty
                    try:
                        # Validate and convert the date format
                        date_obj = datetime.strptime(data[field_name], '%Y-%m-%d').date()
                        setattr(company_temp, field_name, date_obj)
                    except ValueError:
                        return JsonResponse(
                            {'status': 'error', 'message': 'Invalid date format. Must be YYYY-MM-DD.'}, status=400
                        )
            else:
                setattr(company_temp, field_name, data[field_name])

    company_temp.save()
    return JsonResponse({'status': 'success'})


@login_required
def list_company(request):
    companies = Company.objects.all()
    return render(request, 'general/list_company.html', {'companies': companies})


@login_required
def upload_logo(request):
    global s3_client
    user = request.user
    company_temp = get_object_or_404(CompanyTemp, user=user)
    if request.method == 'POST' and request.FILES.get('logo'):
        file = request.FILES['logo']

        # Upload the file
        s3_client.put_object(
            Bucket=os.getenv('AWS_STORAGE_BUCKET_NAME'),
            Key=f'logos/{file.name}',
            Body=file,
            ContentType=file.content_type,
        )

        setattr(company_temp, 'logo', f'logos/{file.name}')
        company_temp.save()

        return JsonResponse({'file_logo': f'logos/{file.name}'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def delete_logo(request):
    global s3_client
    user = request.user
    company_temp = get_object_or_404(CompanyTemp, user=user)
    if request.method == 'POST':
        file_logo = request.POST.get('file_logo')
        print(file_logo)
        if file_logo:
            try:
                # Delete the file from S3
                s3_client.delete_object(Bucket=os.getenv('AWS_STORAGE_BUCKET_NAME'), Key=file_logo)
                setattr(company_temp, 'logo', '')
                company_temp.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
