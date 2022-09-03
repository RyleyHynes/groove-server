from django.db import models
from django.contrib.auth.models import User

# Step 1: Name the model and inherit the django Model class


class GrooveUser(models.Model):
    # Step 2: Add any fields on the erd
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=55)
    image = models.URLField()
