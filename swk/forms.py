from django import forms
from .models import Tracksheet,DutyEntry,Zones,Feedback,UploadPicture#, Rating

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
import datetime
# from phonenumber_field.formfields import PhoneNumberField
from django.contrib.gis import forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import timedelta


            
demarcated_lane = [('none','Select Zone'),
        ('Hira Seth Chawl to Waras Lane','Hira Seth Chawl to Waras Lane'),
        ('Navneet Lane to Tare Galli','Navneet Lane to Tare Galli'),
        ('Bhandar Wada to Amar Prem Chowk','Bhandar Wada to Amar Prem Chowk'),
        ('Pakhari Galli','Pakhari Galli'),
        ('Shankar Mandir to Bhagat Galli','Shankar Mandir to Bhagat Galli'),
        ('Gonta Galli to Kranti Galli','Gonta Galli to Kranti Galli'),
        ('Kranti galli to Navjeevan wasahat','Kranti galli to Navjeevan wasahat'),
        ('Bazar Galli to Fish market','Bazar Galli to Fish market'),
        ('Maval Maratha (Payari)', 'Maval Maratha (Payari)'),
        ('Sonapur to Dukkur Galli','Sonapur to Dukkur Galli'),
        ('Dukkur Galli to Taak Galli','Dukkur Galli to Taak Galli'),
        ('Nagobacha Ghumat to Achanak','Nagobacha Ghumat to Achanak'),
        ('Golfadevi','Golfadevi'),
        
    ]
timeslot= [

            ('7:30am - 8:30 am','Morning'),
            ('7:30pm - 8:30 pm','Evening'),
        ]

Fatten_name = [
    ('Amrapali Nikalje','Amrapali Nikalje'),
    ('Kaushalya Maske', 'Kaushalya Maske'),
    ('Asha Sadar','Asha Sadar'),
    ('Kalinda Jogdand', 'Kalinda Jogdand'),
    ('Laxmi Gaoli','Laxmi Gaoli'),
    ('Jana pote','Jana pote'),
    ('Bismillah Saiyad','Bismillah Saiyad'),
    ('Rehana Saikh','Rehana Saikh'),
    ('Aruna Parkhe','Aruna Parkhe'),
    ('Ganga Sonavane','Ganga Sonavane'),
    ('Kavita Binniwale','Kavita Binniwale'),
    ('Sangeeta Gaikwad','Sangeeta Gaikwad'),
    ('Rama Sinde','Rama Sinde'),
    ('Sanjay Ahire','Sanjay Ahire'),
    
    

]

Satten_name = [
    ('Krushna Patekar', 'Krushna Patekar'),
    ('Parvati Yede','Parvati Yede'),
    ('Sakuntala Kahrat','Sakuntala Kahrat'),
    ('Amba Bai Isre', 'Amba Bai Isre'),
    ('Jija BaiMakasare','Jija BaiMakasare'),
    ('Vaishali Gaoli','Vaishali Gaoli'),
    ('Gaya Bai Parkhe','Gaya Bai Parkhe'),
    ('Indu Bai Gade','Indu Bai Gade'),
    ('Farzana Khan','Farzana Khan'),
    ('Santa Sinde','Santa Sinde'),
    ('Durga Ganbas','Durga Ganbas'),
    ('Sheema Sonavane','Sheema Sonavane'),
    ('Vinayak Salve','Vinayak Salve'),
    
]

supervisor_name = [
    ('Akshay Kharat','Akshay Kharat'),
    ('Sanjay Thorat','Sanjay Thorat'),
    ('Ankit Singh','Ankit Singh'),
    ('Umesh Salve','Umesh Salve'),
    ('Savita Sonawane','Savita Sonawane'),
    ('Zaheer','Zaheer'),
    ('Akash','Akash'),
]


class TracksheetForm(forms.ModelForm):
    
    date= forms.DateField(label = _(u'Date'),required=True,widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    lane_name = forms.CharField(label = _(u'Zone'),widget=forms.Select(choices=demarcated_lane), localize=True)
    num_attendants = forms.CharField(label = _(u'Attendants Number'),widget=forms.HiddenInput(),required=False)
    first_attendants_name = forms.CharField(label = _(u'First Attendant'),widget=forms.HiddenInput(),required=False)
    second_attendants_name = forms.CharField(label = _(u'Second Attendant'),widget=forms.HiddenInput(),required=False)
    supervisor_name = forms.CharField(label = _(u'Supervisor'))
    num_houses_reached = forms.IntegerField(label = _(u'Houses Reached'))
    # time_of_visit = forms.CharField(label = _(u'Time of Visit'),widget=forms.Select(choices=timeslot))
    time_of_visit = forms.CharField(label = _(u'Time of Visit'),widget=forms.HiddenInput(),required=False)
    drywaste_bf = forms.IntegerField(label = _(u"Dry waste before(kgs)"))
    drywaste_af = forms.IntegerField(label = _(u"Dry waste after(kgs)"))
    wetwaste_bf = forms.IntegerField(label = _(u"Wet waste before(kgs)"))
    wetwaste_af = forms.IntegerField(label = _(u"Wet waste after(kgs)"))
    num_houses_doing_segg = forms.IntegerField(label = _(u"Houses doing segregation"))
    num_houses_giving_mixwaste = forms.IntegerField(label = _(u"Houses giving mixed waste"),widget=forms.HiddenInput(),required=False)
    rejected = forms.IntegerField(label=_(u"Rejected Waste"),widget=forms.HiddenInput(),required=False)
    zone_id_id=forms.CharField(max_length=10, label=_(u"Zone ID"),widget=forms.HiddenInput(),required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['date'].localize = True
        # self.fields['zone_id']=forms.ModelChoiceField(queryset=Zones.objects.filter(zone_name=user))

    def clean(self):
        my_date = self.cleaned_data['date']
        today = datetime.date.today()
        yesterday = today - timedelta(days = 1)
        # my_time = self.cleaned_data['my_time']
        # my_date_time = (my_date + ' ' + my_time + ':00')
        # my_date_time = datetime.strptime(my_date_time, '%m/%d/%Y %H:%M:%S')
        # console.log(date.today())
        if my_date > datetime.date.today():
            raise forms.ValidationError('Future Dates are not allowed.!!')
        if my_date < yesterday:
            raise forms.ValidationError('You can only enter todays and yesterdays date.!!')
            return my_date
        

    class Meta:

        model = Tracksheet
        fields = '__all__'
        exclude = ['zone_id']

class TracksheetForm1(forms.ModelForm):
    
    date= forms.DateField(label = _(u'Date'),required=True,widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    lane_name = forms.CharField(label = _(u'Zone'),widget=forms.Select(choices=demarcated_lane), localize=True)
    num_attendants = forms.CharField(label = _(u'Attendants Number'),widget=forms.HiddenInput(),required=False)
    first_attendants_name = forms.CharField(label = _(u'First Attendant'),widget=forms.HiddenInput(),required=False)
    second_attendants_name = forms.CharField(label = _(u'Second Attendant'),widget=forms.HiddenInput(),required=False)
    supervisor_name = forms.CharField(label = _(u'Supervisor'))
    num_houses_reached = forms.IntegerField(label = _(u'Houses Reached'))
    # time_of_visit = forms.CharField(label = _(u'Time of Visit'),widget=forms.Select(choices=timeslot))
    time_of_visit = forms.CharField(label = _(u'Time of Visit'),widget=forms.HiddenInput(),required=False)
    drywaste_bf = forms.IntegerField(label = _(u"Dry waste before(kgs)"))
    drywaste_af = forms.IntegerField(label = _(u"Dry waste after(kgs)"))
    wetwaste_bf = forms.IntegerField(label = _(u"Wet waste before(kgs)"))
    wetwaste_af = forms.IntegerField(label = _(u"Wet waste after(kgs)"))
    num_houses_doing_segg = forms.IntegerField(label = _(u"Houses doing segregation"))
    num_houses_giving_mixwaste = forms.IntegerField(label = _(u"Houses giving mixed waste"),widget=forms.HiddenInput(),required=False)
    rejected = forms.IntegerField(label=_(u"Rejected Waste"),widget=forms.HiddenInput(),required=False)
    zone_id_id=forms.CharField(max_length=10, label=_(u"Zone ID"),widget=forms.HiddenInput(),required=False)
    
    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user',None)
        # super(TracksheetForm, self).__init__(*args, **kwargs)

        super().__init__(*args, **kwargs)

        # self.fields['date'].localize = True
        # self.fields['zone_id']=forms.ModelChoiceField(queryset=Zones.objects.filter(zone_name=user))
     

    class Meta:

        model = Tracksheet
        fields = '__all__'
        exclude = ['zone_id']


class DutyEntryForm(forms.ModelForm):
    lane_name = forms.CharField(label = 'Name of the Route',widget=forms.Select(choices=demarcated_lane))
    first_attendants_name = forms.CharField(label = 'Name of First Attendant',widget=forms.Select(choices=Fatten_name))
    second_attendants_name = forms.CharField(label = 'Name of Second Attendant',widget=forms.Select(choices=Satten_name))
    num_houses_lane = forms.IntegerField(label = 'Houses in Lane')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            
            Row(
                Column('lane_name', css_class='form-group col-md-5 mb-0'),
                Column('num_houses_lane', css_class='form-group col-md-5 mb-0'),                
                css_class='form-row'
            ),
            
            Row(
                Column('first_attendants_name', css_class='form-group col-md-5 mb-0'),
                Column('second_attendants_name', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )

    class Meta:
        model = DutyEntry
        fields = '__all__'


class FeedbackForm(forms.ModelForm):
    # latitude = forms.CharField()
    # longitude = forms.CharField()
    YESNO_CHOICES = ((0, 'No'), (1, 'Yes'))
    name= forms.CharField()
    email = forms.CharField()
    mobile = forms.IntegerField()
    # q1 = forms.CharField(label ="how do you find overall  daily collection service of SWK ?")
    # fw_once =forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Is collecting food waste once a day enough?")
    # fw_twice =forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Would you like to collect food waste twice a day enough?")
    # fw_container = forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Do you have container for food waste?")
    # dw_container = forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Do you have container for dry waste?")
    # mw_container = forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Do you have container for menstrual waste?")
    # ew_container = forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Do you have container for e-waste waste?")
    # req_dw_cont = forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Do you like container for food waste?")
    # req_ww_cont = forms.ChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect,label ="Do you have container for food waste?")
    feedback = forms.CharField(widget=forms.Textarea(attrs={"rows":15, "cols":50}))
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Feedback
        fields = '__all__'
        exclude = ['latitude','longitude','id']

class UploadPictureForm(forms.ModelForm):
    picture = forms.ImageField(label='')
    date = forms.DateField(label = 'Date')
    class Meta:
            model = UploadPicture
            fields = '__all__'

# class RatingForm(forms.Form):
#     name = forms.CharField(label='Your name', max_length=100)
# class RatingForm(forms.ModelForm):
#     name = forms.CharField(label='Your name', max_length=100)
#     mobile = forms.IntegerField(label = "Contact Number")
#     email = forms.CharField(label = "Email Id")
#     service_swk = forms.IntegerField(label = "How do you find service of SWK?")
#     class Meta:
#         model = Rating
#         fields = '__all__'
