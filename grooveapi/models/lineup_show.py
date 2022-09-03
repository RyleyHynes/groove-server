from django.db import models

# Step 1: Name the model and inherit the django Model class


class LineupShow(models.Model):
    # Step 2: Add any fields on the erd
    show = models.ForeignKey("Show", on_delete=models.CASCADE)
    my_lineup = models.ForeignKey("MyLineup", on_delete=models.CASCADE)
