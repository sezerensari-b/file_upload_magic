from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .models import Company
from django.core.exceptions import ValidationError


def create_company(request):
    if request.method == 'POST':
        company_data = {}
        for field in Company._meta.fields:
            field_name = field.name
            if field_name in request.POST:
                company_data[field_name] = request.POST[field_name]
            elif field_name in request.FILES:
                company_data[field_name] = request.FILES[field_name]

        company_data['active'] = company_data.get('active') == 'on'

        company = Company(**company_data)

        try:
            company.full_clean()
            company.save()
            return redirect('list_company')
        except ValidationError as e:
            errors = {field: messages for field, messages in e.message_dict.items()}
            return render(request, 'general/create_company.html', {'company': company, 'errors': errors})

    return render(request, 'general/create_company.html')


def list_company(request):
    companies = Company.objects.all()  # Retrieve all Company instances
    for company in companies:
        print(company.logo.url)
    return render(request, 'general/list_company.html', {'companies': companies})
