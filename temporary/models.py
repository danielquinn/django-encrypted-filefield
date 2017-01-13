from django.db import models
from django_encrypted_filefield.fields import (
    EncryptedFileField,
    EncryptedImageField
)


class MyModel(models.Model):

    name = models.CharField(max_length=128)
    attachment = EncryptedFileField(upload_to="attachments")
    image = EncryptedImageField(
        upload_to="images",
        width_field="image_width",
        height_field="image_height"
    )
    image_width = models.PositiveIntegerField()
    image_height = models.PositiveIntegerField()
