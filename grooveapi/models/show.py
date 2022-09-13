from datetime import datetime, timedelta, date, time
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

    @property
    def end_time(self):
        et = datetime.combine(date.today(), datetime.datetime.strptime(self.start_time,"%H:%M")) + timedelta(hours=1)
        return et.time()
    
    @property
    def get_lineup_day(self):
        if self.start_time.hour in (0,1,2):
            return self.date-timedelta(days=1)
        return self.date

    @property
    def readable_start_time(self):
        return self.start_time.strftime("%I:%M %p")

    @property
    def readable_end_time(self):
        return self.end_time.strftime("%I:%M %p")