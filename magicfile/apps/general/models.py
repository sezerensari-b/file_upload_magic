from django.db import models

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

    def __str__(self):
        return self.name
