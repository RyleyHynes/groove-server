from datetime import datetime
from django.db import models

# Step 1: Name the model and inherit the django Model class


class Show(models.Model):
    # Step 2: Add any fields on the erd
    artist = models.ForeignKey("Artist", on_delete=models.CASCADE, related_name="shows")
    stage = models.ForeignKey("Stage", on_delete=models.CASCADE, related_name="shows")
    datetime = models.DateTimeField()