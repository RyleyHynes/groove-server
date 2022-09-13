from datetime import datetime, timedelta
from django.db import models

# Step 1: Name the model and inherit the django Model class


class MyLineup(models.Model):
    # Step 2: Add any fields on the erd
    groove_user = models.ForeignKey("GrooveUser", on_delete=models.CASCADE, related_name="lineupshows" )
    shows= models.ManyToManyField("Show", related_name="lineups")



    @property
    def end_time(self):
        et = datetime.combine(self.show.date.today(), self.show.start_time) + timedelta(hours=1)
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
