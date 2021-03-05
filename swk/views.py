from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import TracksheetForm, DutyEntryForm
from .models import DutyEntry,Tracksheet,Zones ,SwkAttendants
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


# Create your views here.form


def show(request):
    datas= Tracksheet.objects.all().order_by('-date')
    print(datas[0])
    # datas1= Tracksheet.objects.all().order_by('-lane_name')
    wardetail= DutyEntry.objects.all()
    # data= User.objects.all()
    return render(request,'show_data.html',{'datas':datas})

def download(request,year,month,day):
    print(year)
    print(month)
    print(day)
    new_date=year+'-'+ month +'-'+day
    datas= Tracksheet.objects.filter(date=new_date)
    # print(datas)
    return render(request,'download_data.html',{'datas':datas})

def downloadzone(request,year,month,day,year1,month1,day1,zone_name):
    print(zone_name) 
    print(year)
    print(month)
    print(day)  
    print(year1)
    print(month1)
    print(day1)
    new_date=year+'-'+ month +'-'+day
    new_date1=year1+'-'+ month1 +'-'+day1
    
    # zone_name = lane_name.split(',')
    # zone_count = lane_name.count(',')
    # print(zone_name)
    # for count in zone_count:
    #     zone_name = 'lane_name='+zone_name[count]

    if(zone_name=='ALL'):
        datas= Tracksheet.objects.filter(date__range=(new_date, new_date1)).order_by('date','lane_name')
    else:
        # datas= Tracksheet.objects.filter(lane_name__in=zone_name, date__range=(new_date, new_date1))
        datas= Tracksheet.objects.filter(lane_name=zone_name, date__range=(new_date, new_date1).order_by('date'))
        print(datas)
    return render(request,'download_data_zone.html',{'datas':datas})

def edit(request, id):  
    data = Tracksheet.objects.get(track_id=id)
    # docdata  = doctor.objects.get(id=id)  
    return render(request,'edit.html', {'data':data}) 

def update(request, id):
    # print(id)
    data = Tracksheet.objects.get(track_id=id) 
    print(data) 
    form = TracksheetForm(request.POST, instance = data)  
    print(form)
    if form.is_valid(): 
        print("success") 
        form.save()  
        return redirect("/show/")  
    else:
        print("fail")
    return render(request, 'edit.html', {'data': data}) 


def destroy(request, id):  
    data = Tracksheet.objects.get(track_id=id)  
    data.delete()  
    return redirect("/show/")  
 
def user_login(request):
    # context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
                if user.is_active:
                    login(request, user)
                    # Redirect to index page.
                    # messages.info(request,"login sucessfully")
                    messages.info(request,_(u"loggedin sucessfully. Please check navigation bar on top to fill required forms."))
                    return render(request,"HomePage.html")
                else:
                    # Return a 'disabled account' error message
                    messages.info(request,_(u"Your account is disabled"))
                    return HttpResponseRedirect_(u"Your account is disabled.")
        else:
                # Return an 'invalid login' error message.
                print (_(u"invalid login details for " + username))
                # messages.info(request,"Invalid login details"+ username )
                messages.error(request, _(u"Invalid username or password."))
                return render(request,'adminlogin.html')
    else:
        # the login is a  GET request, so just show the user the login form.
        return render(request,'adminlogin.html')

def formLayout(request):
    return render(request,"formlayout.html")
def HomePage(request):
        return render(request,"HomePage.html")

def logout_request(request):
    logout(request)
    messages.info(request, _(u"Logged out successfully!"))
    return render(request,"HomePage.html")

def DutyEntryPage(request):
    if request.method == "POST":
         
        # num_houses = request.POST.get("")
        form = DutyEntryForm(request.POST or None)       
        if form.is_valid():
            form.save()
            messages.success(request, _(u'Your data is saved'))
        return HttpResponseRedirect(request.path_info)
    else:
        form = DutyEntryForm(request.POST or None)
        context= {
            'form': form,
            'test': 'test',
        }

    return render(request,'DutyEntryForm.html',context)

def TracksheetPage(request):
    form = TracksheetForm(request.POST or None)
    if request.is_ajax():
        selected_field = request.GET['name']
        print(selected_field)
        docinfo = list(SwkAttendants.objects.filter(zone_name=selected_field).values()); 
        print(docinfo)
        jsondata =docinfo[0]
        # field=docinfo[0]["zone_id"]
        # print(field)
        # docinfo1 = list(SwkAttendants.objects.filter(zone_id=field).values()); 
        # jsondata1=docinfo1[0]
        return JsonResponse(jsondata)

    # if request.is_ajax():
    #     selected_drywaste_bf = request.GET['drywaste_bf']
    #     selected_wetwaste_bf = request.GET['wetwaste_bf']
    #     selected_drywaste_af = request.GET['drywaste_af']
    #     selected_wetwaste_af = request.GET['wetwaste_af']
    #     selcted_lane_name = request.GET['lane_name']
        
    #     rejected_waste = ((selected_drywaste_bf + selected_wetwaste_bf) - (selected_drywaste_af + selected_wetwaste_af))
    #     num_houses = DutyEntry.objects.raw('select  num_houses_lane from DutyEntry'.format(selcted_lane_name))
    #     # min = Corporatorward.objects.raw('select 1 as id,min({}) from corporatorward'.format(selected_field))[0].min

    #     jsondata = {
    #         'num_houses': num_houses, 'rejected_waste': rejected_waste
    #     }
    #     return JsonResponse(jsondata)
        
    if request.method == "POST":
                 
        form = TracksheetForm(request.POST or None)
        print(form)
        if form.is_valid():
            query_column = form.cleaned_data['lane_name']
            # operator = form.cleaned_data['operator']
            # value = form.cleaned_data['value']
            query="""select num_houses_lane from DutyEntry where lane_name = '{}'""".format(query_column)
            raw = DutyEntry.objects.raw(query)
            context = {'form':form,'data':raw}
            date = form.cleaned_data['date']
            zone = form.cleaned_data['zone_id_id']
            print(zone)
            laneName = form.cleaned_data['lane_name']
            if  Tracksheet.objects.filter(date=date, lane_name=laneName).exists():
                messages.warning(request, _(u'Data already exists'))
            else:

                instance = form.save(commit=False)
                instance.num_houses_lane = 100
                instance.rejected = ((instance.drywaste_bf +instance.wetwaste_bf) - (instance.drywaste_af + instance.wetwaste_af))
                instance.num_houses_giving_mixwaste = (instance.num_houses_reached - instance.num_houses_doing_segg)
                print(instance.num_houses_giving_mixwaste)
                instance.zone_id_id=zone
                print(instance.zone_id_id)

                instance.save()
                messages.success(request, _(u'Your data is saved for {} dated {}').format(laneName,date))
                # form.save()
                # messages.success(request, 'Your data is saved')
                return HttpResponseRedirect(request.path_info)
     
        else:
            messages.warning(request, _(u'Please check your form'))
    else:
        
        form = TracksheetForm(request.POST or None)
    context= {
        'form': form,
               
        'test': 'test',
    }

    return render(request,'TracksheetForm.html',context)


def MapPage(request):
    return render(request,"map_fromFGIS.html")

# def TracksheetPage(request):
#     form = TracksheetForm(request.POST or None)
#     if form.is_valid():
#         form.save()

#     context= {
#         'form': form,
#         'test': 'test',
#     }

#     return render(request,'TracksheetForm.html',context)

def AboutUs(request):
    return render(request,"aboutus.html")

def report(request):
        return HttpResponseRedirect('/report_builder/report/5')

        