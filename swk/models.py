from django.db import models
from django import forms
from django.forms import ModelForm

from wagtail.core.models import Page
from django.utils.translation import gettext_lazy as _

class DutyEntry(models.Model):
    lane_name = models.CharField(primary_key = True, max_length=200, blank = False)
    first_attendants_name = models.CharField(max_length=100)
    second_attendants_name = models.CharField(max_length=100)
    num_houses_lane = models.IntegerField()
   
    def __str__(self):
        return self.lane_name

class HomePage(Page):

    template = "HomePage.html"


class Zones(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    zone_name = models.CharField(max_length=100, blank=True, null=True)
    zone_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'zones'

class TracksheetModel(Page):

    template = "TracksheetForm.html"
class SwkAttendants(models.Model):
    attendant1 = models.CharField(max_length=50, blank=True, null=True)
    attendant2 = models.CharField(max_length=50, blank=True, null=True)
    supervisor = models.CharField(max_length=50, blank=True, null=True)
    zone_name = models.CharField(max_length=100, blank=True, null=True)
    zone_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'swk_attendants'

class Tracksheet(models.Model):
    # date =models.DateField()
    date =models.DateField(help_text=_('Enter Date'))
    lane_name = models.CharField(max_length=200, blank = False)
    # lane_name = models.ForeignKey(DutyEntry,default = 1, on_delete=models.SET_DEFAULT)
    num_attendants = models.CharField(default = 2,max_length= 10 )
    first_attendants_name = models.CharField(max_length=100)
    second_attendants_name = models.CharField(max_length=100)
    supervisor_name = models.CharField(max_length=100,default = 'Zaheer')
    num_houses_reached = models.IntegerField(default= 20,help_text=_('Enter Houses Reached'))
    num_houses_doing_segg = models.IntegerField()
    num_houses_giving_mixwaste = models.IntegerField()
    drywaste_bf = models.IntegerField()
    drywaste_af = models.IntegerField()
    wetwaste_bf = models.IntegerField()
    wetwaste_af = models.IntegerField()
    time_of_visit = models.CharField(max_length=100)
    track_id = models.AutoField(primary_key=True)
    rejected = models.IntegerField()
    zone_id=models.ForeignKey(Zones, on_delete=models.CASCADE)

    def __str__(self):
        return self.lane_name




class SwkTracksheetReport(models.Model):
    num_houses_reached = models.IntegerField()
    num_houses_doing_segg = models.IntegerField()
    num_houses_giving_mixwaste = models.IntegerField()
    drywaste_bf = models.IntegerField()
    drywaste_af = models.IntegerField()
    wetwaste_bf = models.IntegerField()
    wetwaste_af = models.IntegerField()
    lane_name = models.CharField(max_length=200)
    num_attendants = models.IntegerField()
    first_attendants_name = models.CharField(max_length=100)
    second_attendants_name = models.CharField(max_length=100)
    time_of_visit = models.CharField(max_length=100)
    track_id = models.AutoField(primary_key=True)
    date = models.DateField()
    supervisor_name = models.CharField(max_length=100)
    num_houses = models.IntegerField(blank=True, null=True)
    rejected_total = models.IntegerField(blank=True, null=True)
    rejected_dry = models.IntegerField(blank=True, null=True)
    rejected_wet = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'swk_tracksheet_report'

class Feedback(models.Model):
    # location = models.PointField(geography=True, default=Point(0.0, 0.0))
    # position = GeopositionField()
    # latitude = models.DecimalField(max_digits=11, decimal_places=8)
    # longitude = models.DecimalField(max_digits=11, decimal_places=8)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    mobile = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'swk_feedback'

class UploadPicture(models.Model):
    picture = models.FileField(upload_to='uploadPics/', blank=True, null=True)
    date = models.DateField()

class SwkBubblePopulation(models.Model):
    zone_id = models.CharField(max_length=50, blank=True, null=True)
    bubble_id = models.IntegerField(blank=True, null=True)
    spot_id = models.IntegerField(blank=True, null=True)
    bubble_population = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'swk_bubble_population'