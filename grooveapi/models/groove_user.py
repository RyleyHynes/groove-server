from django.db import models
from django.contrib.auth.models import User

# Step 1: Name the model and inherit the django Model class


class GrooveUser(models.Model):
    # Step 2: Add any fields on the erd
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=55)
    profile_image = models.ImageField(
        upload_to='actionimages', height_field=None,
        width_field=None, max_length=None, null=True)
    bio = models.CharField(max_length=250)
