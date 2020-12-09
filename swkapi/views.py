from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .serializers import newTracksheet
from swk.models import Tracksheet


class tracksheetview(viewsets.ModelViewSet):
    queryset = Tracksheet.objects.all().order_by('track_id')
    serializer_class = newTracksheet
    # def get_queryset(self,*args, **kwargs):
    #             # selectedTab = self.kwargs.get('tab', None)
    #             queryset = Tracksheet.objects.all().order_by('num_houses_giving_mixwaste')
    #             return queryset