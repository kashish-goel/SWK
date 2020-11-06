from django.shortcuts import render

# Create your views here.

def Map(request):
   return render(request,"map/map.html")