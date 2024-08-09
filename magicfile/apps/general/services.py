from .models import Company, CompanyTemp
from django.core.exceptions import ValidationError
import boto3
import os
from datetime import datetime


class CompanyService:
    @staticmethod
    def get_or_create_temp_company(user):
        try:
            return CompanyTemp.objects.get(user=user)
        except CompanyTemp.DoesNotExist:
            return CompanyTemp.objects.create(user=user)

    @staticmethod
    def create_company(user, company_data):
        company_data['user'] = user
        company_data['active'] = company_data.get('active') == 'on'
        company = Company(**company_data)

        try:
            company.full_clean()
            company.save()
            return company
        except ValidationError as e:
            return None, e.message_dict

    @staticmethod
    def update_temp_company(company_temp, data):
        for field in CompanyTemp._meta.fields:
            field_name = field.name
            if field_name in data:
                if field_name == 'active':
                    setattr(company_temp, field_name, data[field_name] == 'on')
                elif field_name == 'founded_date':
                    if data[field_name]:
                        try:
                            date_obj = datetime.strptime(data[field_name], '%Y-%m-%d').date()
                            setattr(company_temp, field_name, date_obj)
                        except ValueError:
                            return {'status': 'error', 'message': 'Invalid date format. Must be YYYY-MM-DD.'}
                else:
                    setattr(company_temp, field_name, data[field_name])

        company_temp.save()
        return {'status': 'success'}


class S3Service:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCES_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_S3_REGION_NAME'),
    )

    @classmethod
    def upload_logo(cls, file):
        cls.s3_client.put_object(
            Bucket=os.getenv('AWS_STORAGE_BUCKET_NAME'),
            Key=f'logos/{file.name}',
            Body=file,
            ContentType=file.content_type,
        )
        return f'logos/{file.name}'

    @classmethod
    def delete_logo(cls, file_logo):
        cls.s3_client.delete_object(Bucket=os.getenv('AWS_STORAGE_BUCKET_NAME'), Key=file_logo)
