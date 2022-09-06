from django.db import models

# Step 1: Name the model and inherit the django Model class


class Stage(models.Model):
    # Step 2: Add any fields on the erd
    stage_name= models.CharField(max_length=55)
