from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Company(models.Model):
    SECTOR_CHOICES = [('tech', 'Technology'), ('finance', 'Finance'), ('health', 'Health'), ('education', 'Education')]

    name = models.CharField(max_length=255)
    logo = models.FileField(upload_to='logos/')
    founded_date = models.DateField()
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CompanyTemp(models.Model):
    SECTOR_CHOICES = [('tech', 'Technology'), ('finance', 'Finance'), ('health', 'Health'), ('education', 'Education')]

    name = models.CharField(max_length=255, blank=True)
    logo = models.FileField(upload_to='logos/', null=True, blank=True)
    founded_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    active = models.BooleanField(default=True, null=True, blank=True)
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name if self.name else 'Unnamed Company'
