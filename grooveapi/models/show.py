from datetime import datetime, timedelta
from django.db import models


# Step 1: Name the model and inherit the django Model class


class Show(models.Model):
    # Step 2: Add any fields on the erd
    artist = models.ForeignKey(
        "Artist", on_delete=models.CASCADE, related_name="shows")
    stage = models.ForeignKey(
        "Stage", on_delete=models.CASCADE, related_name="shows")
    date = models.DateField(null=True)
    start_time = models.TimeField()

    def end_time(self):
        return self.start_time + timedelta(hours=1)
    
    def get_lineup_day(self):
        if self.start_time.hour in (1,2):
            return self.date-timedelta(days=1)
        return self.date