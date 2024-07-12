from django.db import models

# Create your models here.


class MyFile(models.Model):
    file = models.FileField(upload_to='myfile/')
    file_path = models.CharField(max_length=255)

    def __str__(self):
        return self.file_path  # or format it as needed

    def save(self, *args, **kwargs):
        self.file_path = 'media/myfile/' + self.file.name
        super().save(*args, **kwargs)
