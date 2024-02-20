from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='kzpl/final/temp/input/')


    def __str__(self):
        return self.file.name

