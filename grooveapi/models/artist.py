from django.db import models

# Step 1: Name the model and inherit the django Model class


class Artist(models.Model):
    # Step 2: Add any fields on the erd
    artist_name = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    artist_description = models.CharField(max_length=250)
    artist_image = models.URLField()

