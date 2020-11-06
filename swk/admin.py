from django.contrib import admin

# Register your models here.
# from .models import Drywaste, Tracksheet,Lanedetails,LaneCordinator
from .models import Tracksheet,DutyEntry

admin.site.register(Tracksheet)
admin.site.register(DutyEntry)