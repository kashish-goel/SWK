from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.template import loader
from .forms import TracksheetForm, DutyEntryForm, TracksheetForm1,FeedbackForm,UploadPictureForm#,RatingForm
from .models import DutyEntry,Tracksheet,Zones ,SwkAttendants, Rating
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail, get_connection


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
    
    # zone_name = zone_name.split(',')
    # zone_count = zone_name.count(',')
    # print(zone_count)
    # for count in zone_count:
    #     zone_name = 'lane_name='+zone_name[count]

    if(zone_name=='ALL'):
        datas= Tracksheet.objects.filter(date__range=(new_date, new_date1)).order_by('date','lane_name')
    else:
        
        datas= Tracksheet.objects.filter(lane_name__in=(zone_name.split(',')), date__range=(new_date, new_date1)).order_by('date','lane_name')
        # datas= Tracksheet.objects.filter(lane_name=zone_name, date__range=(new_date, new_date1)).order_by('date','lane_name')
        # print(datas.query)
    return render(request,'download_data_zone.html',{'datas':datas})

def edit(request, id):  
    data = Tracksheet.objects.get(track_id=id)
    # docdata  = doctor.objects.get(id=id)  
    print(data.date)
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
            # print(request.POST['username'])
            laneName = form.cleaned_data['lane_name']
            print(laneName)
            if laneName =="none":
                messages.warning(request, _(u'Please select Zone'))
                

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


def TrackformPageDetail(request):
    form = TracksheetForm1(request.POST or None)
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

    if request.method == "POST":
         
        form = TracksheetForm1(request.POST or None)
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
            # print(request.POST['username'])
            laneName = form.cleaned_data['lane_name']
            print(laneName)
            if laneName =="none":
                messages.warning(request, _(u'Please select Zone'))
                

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

    return render(request,'TrackformPageDetail.html',context)



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
        return HttpResponseRedirect('/report_builder/report/9')

def FAQ(request):
        return render(request,"faq.html")

def Contact(request):
        return render(request,"contact.html")

def RatingView(request):
        print(request.method)
        if request.method == 'POST':
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            service_swk = request.POST.get('rating1')
            timing_swk = request.POST.get('rating2')
            mobile_swk = request.POST.get('rating3')
            compost_kit_garden = request.POST.get('rating4')
            communicate_swk = request.POST.get('rating5')
            food_bin =request.POST.get('yes_no')
            paper_bin = request.POST.get('yes_no1')
            ewaste_bin =request.POST.get('yes_no2')
            pads_bin = request.POST.get('yes_no3')
            epr_bin= request.POST.get('yes_no4')
            print(food_bin)
            print(paper_bin)
            print(ewaste_bin)
            print(pads_bin)
            print(epr_bin)


        
            sub=Rating(name=name,mobile=mobile,email=email,service_swk=service_swk,timing_swk=timing_swk,mobile_swk=mobile_swk,compost_kit_garden=compost_kit_garden,communicate_swk=communicate_swk,food_bin=food_bin,paper_bin=paper_bin, ewaste_bin=ewaste_bin, epr_bin=epr_bin,pads_bin=pads_bin)
            # if sub.save():
                # print(sub.save)
            sub.save()
            messages.success(request, _(u' Your feedback is saved. '))
            return HttpResponseRedirect(request.path_info)
            # else:
            #     messages.warning(request, _(u'Please check your form'))
       

        return render(request,"rating.html")  

def Feedback(request):
    # form_class = FeedbackForm
    # return render(request,"feedback_form.html", { 'form': form_class,})

    form = FeedbackForm(request.POST or None)
    if request.method == 'POST':
        form = FeedbackForm(request.POST or None)
        if form.is_valid():
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            cd = form.cleaned_data
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            grievance = form.cleaned_data['grievance']
            # fw_once =form.cleaned_data['fw_once']
            # fw_twice = form.cleaned_data['fw_twice']
            # fw_container = form.cleaned_data['fw_container']
            # dw_container = form.cleaned_data['dw_container']
            # mw_container = form.cleaned_data['mw_container']
            # ew_container = form.cleaned_data['ew_container']
            print("feedabck is"+cd['feedback'])
            print("email is"+ cd['email'])
            from_email = form.cleaned_data['email']
            message_mail = 'Senders Name -  '+ name + "\n" + 'Senders Mobile - '+ str(mobile) + "\n" + 'Senders Email Id - ' +from_email + "\n" + 'Feedback Received - '+ feedback
            # message_mail = 'Senders Name -  '+ name + "\n" + 'Senders Mobile - '+ str(mobile) + "\n" + 'Senders Email Id - ' +from_email + "\n" 
            # + 'Is collecting food waste once a day enough? - '+ fw_once + "\n"
            # + 'Would you like to collect food waste twice a day enough? - '+ str(fw_twice) + "\n"
            # + 'Do you have container for food waste? - '+ str(fw_container) + "\n"
            # + 'Do you have container for dry waste? - '+ str(dw_container) + "\n"
            # + 'Do you have container for menstrual waste? - '+ str(mw_container) + "\n"
            # + 'Do you have container for e-waste waste? - '+ str(ew_container) + "\n"
            # + 'Feedback Received - '+ feedback

            # print(latitude)
            # print(request.POST.get('lat'))
            print(from_email)
            print(request.POST)
            form.save()
            

            # con = get_connection('django.core.mail.backends.console.EmailBackend')
            con = get_connection('django.core.mail.backends.smtp.EmailBackend')
            # if (send_mail('Feedback (SWK)', cd['feedback'],cd.get('email', 'noreply@example.com'),
            # ['monikapatira@gmail.com'],connection=con)):
            if(send_mail('Feedback received for swk.communitygis.net', message_mail,from_email,['sms.swk@gmail.com'],fail_silently=False,)):
            # if(send_mail('Feedback (SWK)', message_mail,from_email,['monikapatira@gmail.com'],fail_silently=False,)):
                print("message sent")
            else :
                console.log(message_mail)
                print("Failure")
            messages.success(request, 'Your feedback is saved and email is sent.') 
            return HttpResponseRedirect(request.path_info)
        else:
            # latitude = request.POST.get('latitude')
            # longitude = request.POST.get('longitude','')
            # print(latitude)
            # print(longitude)
            # print(request.POST.get('lat'))
            # print(request.POST)
            cd = form.cleaned_data
            print(cd)
            print(form.errors)
            messages.warning(request, 'Please check your form') 
            return render(request, 'feedback_form.html',{'form': FeedbackForm})
    else: 
        form_class = FeedbackForm
        return render(request,"feedback_form.html", { 'form': form_class,})



def UploadImage(request):
    form = UploadPictureForm()
    global datauri
    if request.is_ajax():
        datauri = request.POST['picture']
    

    if request.method == 'POST' and not request.is_ajax():
        form = UploadPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        # lat = request.POST.get('lat')
        # lng = request.POST.get('lng')

        # try:
        #     imgstr = re.search(r'base64,(.*)', datauri).group(1)
        #     data = ContentFile(base64.b64decode(imgstr))
        #     myfile = "profile-"+time.strftime("%Y%m%d-%H%M%S")+".png"
        #     fs = FileSystemStorage()
        #     filename = fs.save(myfile, data)
        #     picLocation = PictureLocation.objects.create(user=request.user,picture_name=filename,lat=lat,lng=lng)
        #     picLocation.save()
        #     datauri = False
        #     del datauri
        # except NameError:
        #     print("Image is not captured")
       
        

    return render(request,"upload_image.html",{'form':form})
