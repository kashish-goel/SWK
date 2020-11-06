from django.db import models
from django import forms
from django.forms import ModelForm

from wagtail.core.models import Page


class HomePage(Page):

    template = "HomePage.html"



class TracksheetModel(Page):

    template = "TracksheetForm.html"

class Tracksheet(models.Model):
    date =models.DateField()
    num_houses_reached = models.IntegerField(default= 20)
    num_houses_doing_segg = models.IntegerField()
    num_houses_giving_mixwaste = models.IntegerField()
    drywaste_bf = models.IntegerField()
    drywaste_af = models.IntegerField()
    wetwaste_bf = models.IntegerField()
    wetwaste_af = models.IntegerField()
    lane_name = models.CharField(max_length=200, blank = False)
    num_attendants = models.IntegerField(default = 2 )
    first_attendants_name = models.CharField(max_length=100)
    second_attendants_name = models.CharField(max_length=100)
    time_of_visit = models.CharField(max_length=100)
    track_id = models.AutoField(primary_key=True)
    rejected = models.IntegerField()

    def __str__(self):
        return self.lane_name

class DutyEntry(models.Model):
    lane_name = models.CharField(primary_key = True, max_length=200, blank = False)
    first_attendants_name = models.CharField(max_length=100)
    second_attendants_name = models.CharField(max_length=100)
    num_houses_lane = models.IntegerField()
   
    def __str__(self):
        return self.lane_name
