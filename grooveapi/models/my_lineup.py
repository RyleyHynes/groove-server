from django.db import models

# Step 1: Name the model and inherit the django Model class


class MyLineup(models.Model):
    # Step 2: Add any fields on the erd
    groove_user = models.ForeignKey("GrooveUser", on_delete=models.CASCADE, related_name="lineupshows" )
